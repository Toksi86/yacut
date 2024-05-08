from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, URL, Regexp

from .constants import REGEXP_FOR_VALID_CHARACTERS


class UrlForm(FlaskForm):
    """Форма для создания экземпляра модели URLMap"""
    original_link = URLField(
        'Оригинальная ссылка',
        validators=(DataRequired(message='Обязательное поле'),
                    URL(message="Некорректный адрес URL.")),
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(
                max=16,
                message="Длина поля не должна превышать 16 символов.",
            ),
            Regexp(
                REGEXP_FOR_VALID_CHARACTERS,
                message=(
                    "Указано недопустимое имя для короткой ссылки"
                ),
            )
        )
    )

    submit = SubmitField('Добавить')
