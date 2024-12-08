from flask_wtf import FlaskForm
from wtforms import SelectField, ValidationError
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
