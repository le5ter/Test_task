from flask_restx import Namespace, Resource, fields
from flask import request

from app.extensions import db
from app.models import User, Transaction


api = Namespace('transactions', description='Операции с транзакциями')

transaction_request = api.model('CreateTransaction', {
    'user_id': fields.Integer(description='ID пользователя (необязательно)', required=False),
    'amount': fields.Float(description='Сумма транзакции', required=True)
})

transaction_response = api.model('Transaction', {
    'id': fields.Integer(description='ID транзакции'),
    'amount': fields.Float(description='Сумма'),
    'commission': fields.Float(description='Комиссия'),
    'status': fields.String(description='Статус транзакции'),
    'created_at': fields.String(description='Время создания'),
    'user_id': fields.Integer(description='ID пользователя')
})

cancel_transaction_request = api.model('CancelTransaction', {
    'transaction_id': fields.Integer(description='ID транзакции', required=True)
})


@api.route('/create_transaction')
class CreateTransaction(Resource):
    @api.expect(transaction_request, validate=True)
    @api.response(201, 'Транзакция успешно создана', model=transaction_response)
    @api.response(400, 'Неверные входные данные')
    @api.response(404, 'Пользователь не найден')
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        amount = data.get('amount')

        if not amount or amount <= 0:
            return {'error': 'Сумма должна быть положительным числом'}, 400

        user = None
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'Пользователь с указанным ID не найден'}, 404

        if not user:
            user = User(balance=0.0, commission_rate=0.1)
            db.session.add(user)
            db.session.flush()

        commission = amount * user.commission_rate

        new_transaction = Transaction(
            amount=amount,
            commission=commission,
            status='waiting',
            user_id=user.id
        )
        db.session.add(new_transaction)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return {
            'id': new_transaction.id,
            'amount': new_transaction.amount,
            'commission': new_transaction.commission,
            'status': new_transaction.status,
            'created_at': str(new_transaction.created_at),
            'user_id': new_transaction.user_id
        }, 201


@api.route('/cancel_transaction')
class CancelTransaction(Resource):
    @api.expect(cancel_transaction_request, validate=True)
    @api.response(200, 'Транзакция успешно отменена')
    @api.response(404, 'Транзакция не найдена')
    @api.response(400, 'Транзакцию нельзя отменить')
    def post(self):
        data = request.json
        transaction_id = data.get('transaction_id')
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return {'error': 'Транзакция с указанным ID не найдена'}, 404

        if transaction.status != 'waiting':
            return {'error': 'Транзакцию можно отменить только в статусе "waiting"'}, 400

        transaction.status = 'canceled'

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return {'message': f'Транзакция {transaction_id} успешно отменена'}, 200


@api.route('/check_transaction/<int:transaction_id>')
class CheckTransaction(Resource):
    @api.response(200, 'Информация о транзакции', model=transaction_response)
    @api.response(404, 'Транзакция не найдена')
    def get(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return {'error': 'Транзакция с указанным ID не найдена'}, 404

        return {
            'id': transaction.id,
            'amount': transaction.amount,
            'commission': transaction.commission,
            'status': transaction.status,
            'created_at': str(transaction.created_at),
            'user_id': transaction.user_id
        }, 200
