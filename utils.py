from app import create_app
from app.extensions import db
from app.models import Transaction
from app.models.user import generate_trc20_wallet, User

app = create_app()


def create_transaction(user_id, amount, commission, status='waiting'):
    new_transaction = Transaction(
        user_id=user_id,
        amount=amount,
        commission=commission,
        status=status
    )

    with app.app_context():
        with db.session.begin():
            db.session.add(new_transaction)
            db.session.flush()

        db.session.commit()
        print(f"Транзакция {new_transaction.id} успешно добавлена!")
    return new_transaction


def fill_users_public_keys():
    with app.app_context():
        with db.session.begin():
            users = User.query.all()
            for user in users:
                if user.usdt_public_key is None:
                    public_key = generate_trc20_wallet()
                    user.usdt_public_key = public_key
                    print(f"Пользователю {user.id} добавлен адрес {public_key}")


if __name__ == "__main__":
    # create_transaction(user_id=6, amount=100.0, commission=10.0)
    fill_users_public_keys()
