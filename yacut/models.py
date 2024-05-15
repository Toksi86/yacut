from datetime import datetime
from random import choice
from string import ascii_letters, digits

from yacut import db
from .constants import SHORT_ID_LENGTH, ORIGINAL_LINK_LENGTH, BASE_URL


class URLMap(db.Model):
    """Модель для хранения сопоставления между
    оригинальными и сокращенными URL."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def to_dict(self):
        return {'url': self.original,
                'short_link': f'{BASE_URL}{self.short}'
                }

    @staticmethod
    def generating_unique_short_id(short_id_length):
        """Генерирует уникальный сокращенный ID заданной длины."""
        chars = ascii_letters + digits
        short_id = ''
        for _ in range(short_id_length):
            short_id += choice(chars)
        return short_id

    @classmethod
    def checking_uniqueness_short_id(cls, short_id):
        """Проверяет сокращённый ID на уникальность в базе данных."""
        return cls.query.filter_by(short=short_id).first() is None

    @classmethod
    def creating_unique_id(cls, length=SHORT_ID_LENGTH) -> str:
        """Создает уникальный сокращенный ID."""
        while True:
            short_id = cls.generating_unique_short_id(length)
            if cls.checking_uniqueness_short_id(short_id):
                break
        return short_id
