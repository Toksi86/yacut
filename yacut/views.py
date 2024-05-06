import logging

from flask import render_template

from yacut import app
from .forms import UrlForm

logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        logging.debug(f"original_link: {original_link}")
        logging.info(f"custom_id: {custom_id}")

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
