from flask_wtf import FlaskForm
from wtforms import SelectField, ValidationError, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired
from app.models import Transaction


class TransactionForm(FlaskForm):
    status = SelectField(
        'Status',
        choices=[choice for choice in Transaction.STATUS_CHOICES],
        validators=[DataRequired()]
    )

    def validate_status(self, field):
        if field.data not in ['waiting', 'confirmed', 'cancelled']:
            raise ValidationError("Неверный статус!")


class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    role = SelectField(
        'Role',
        choices=['user', 'admin'],
        validators=[DataRequired()]
    )
    balance = FloatField("Balance", default=0)
    commission_rate = FloatField("Balance", default=0.2)
    webhook_url = StringField("WebHook")


class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    role = SelectField(
        'Role',
        choices=['user', 'admin'],
        validators=[DataRequired()]
    )
    balance = FloatField("Balance", default=0)
    commission_rate = FloatField("Balance", default=0.2)
    webhook_url = StringField("WebHook")
