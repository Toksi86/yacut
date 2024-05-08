import logging

from flask import render_template, flash, redirect

from yacut import app, db
from .constants import BASE_URL
from .forms import UrlForm
from .models import URLMap

logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w")


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Обрабатывает главную страницу приложения.
    Если форма отправлена и прошла валидацию, создает новую запись в базе данных.
    Если форма не прошла валидацию, возвращает страницу с ошибками.
    """
    form = UrlForm()

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    if not form.custom_id.data:
        form.custom_id.data = URLMap.creating_unique_id()

    if not URLMap.checking_uniqueness_short_id(form.custom_id.data):
        flash(f'Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)

    logging.debug(f"original_link: {form.original_link.data}")
    logging.debug(f"custom_id: {form.custom_id.data}")

    link = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data,
    )

    db.session.add(link)
    db.session.commit()

    return render_template('index.html',
                           form=form,
                           short_url=BASE_URL + link.short,
                           original_link=link.original)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url_view(short):
    """
    Перенаправляет пользователя на оригинальный URL по короткому идентификатору.
    Если короткий идентификатор не найден, возвращает 404 ошибку.
    """
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)


if __name__ == '__main__':
    app.run()
