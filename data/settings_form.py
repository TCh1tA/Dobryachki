from flask_wtf import FlaskForm
from wtforms.fields.simple import BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    p_time = TextAreaField('Время для поддержки в формате Ч: 21 M: 30', validators=[DataRequired()])
    custom_podd = TextAreaField('Кастомная поддержка (необязательно)')
    prem_image = BooleanField('Использовать картинку при поддержке?')
    submit = SubmitField('Сохранить')
