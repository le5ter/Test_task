import requests
import base58
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import Transaction, User
from celery_main import celery_worker


url_base = "https://api.shasta.trongrid.io"
TRON_USDT_CONTRACT = "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"


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


def address_to_parameter(addr):
    return "0" * 24 + base58.b58decode_check(addr)[1:].hex()


@celery_worker.task
def check_user_usdt_balance(user_id: int):
    user = db.session.query(User).filter_by(id=user_id).one_or_none()

    if not user:
        return

    method_balance_of = 'balanceOf(address)'
    url = url_base + '/wallet/triggerconstantcontract'
    payload = {
        'owner_address': base58.b58decode_check(user.usdt_public_key).hex(),
        'contract_address': base58.b58decode_check(TRON_USDT_CONTRACT).hex(),
        'function_selector': method_balance_of,
        'parameter': address_to_parameter(user.usdt_public_key),
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if data['result'].get('result', None):
        val = data['constant_result'][0]
        return int(val, 16) / 1000000
    else:
        raise Exception('error:', bytes.fromhex(data['result']['message']).decode())
