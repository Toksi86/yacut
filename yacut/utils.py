from .models import URLMap


def checking_the_link_for_uniqueness(custom_id):
    """
     Проверяет уникальность идентификатора короткой ссылки в базе данных.
     Если он уже существует, функция возвращает этот идентификатор.
     В противном случае, возвращает None.
    """
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None
