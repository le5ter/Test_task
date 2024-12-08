import requests
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import Transaction
from celery_main import celery_worker


def get_transactions():
    batch_size = 10
    offset = 0

    while True:
        transactions = (
            db.session.query(Transaction)
            .options(selectinload(Transaction.user))
            .filter(Transaction.status == 'waiting')
            .limit(batch_size)
            .offset(offset)
            .all()
        )
        if not transactions:
            break

        yield from transactions
        offset += batch_size


@celery_worker.task
def check_transaction_status():
    current_time = datetime.now(timezone.utc)
    for transaction in get_transactions():
        transaction_time: datetime = transaction.created_at.astimezone(timezone.utc)
        if current_time - transaction_time > timedelta(minutes=15):
            transaction.status = 'expired'
            db.session.commit()

            webhook_data = {
                'transaction_id': transaction.id,
                'status': transaction.status
            }

            try:
                response = requests.post(transaction.user.webhook_url, json=webhook_data)
                if response.status_code == 200:
                    print(f"Webhook отправлен для транзакции {transaction.id}")
                else:
                    print(f"Ошибка при отправке вебхука для транзакции {transaction.id}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при отправке вебхука для транзакции {transaction.id}: {e}")
