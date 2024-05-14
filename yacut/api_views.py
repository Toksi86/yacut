import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from .constants import SHORT_ID_LENGTH, AUTO_GENERATED_SHORT_ID_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """
    Получение оригинального URL по короткому идентификатору.

    Метод позволяет получить оригинальный URL,
    используя короткий идентификатор.
    Если короткий идентификатор не найден в базе данных,
    метод возвращает ошибку с сообщением.
    """
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def post_url_map():
    """
    Добавляет новую запись в базу данных для короткой ссылки.

    Эта функция принимает POST-запрос с JSON-телом, содержащим оригинальный URL
    и (опционально) пользовательский короткий идентификатор.
    Если пользовательский короткий идентификатор не предоставлен,
    генерируется уникальный.
    """
    request_data = request.get_json()

    if not request_data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    original_url = request_data.get('url')
    if not original_url:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_short_id = request_data.get('custom_id')

    if custom_short_id:
        if len(custom_short_id) > SHORT_ID_LENGTH:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if re.match(r"^[A-Za-z0-9]+$", custom_short_id) is None:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=custom_short_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_short_id = URLMap.creating_unique_id(
            AUTO_GENERATED_SHORT_ID_LENGTH)

    url_map = URLMap(
        original=original_url,
        short=custom_short_id
    )

    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
