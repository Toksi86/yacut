from flask import render_template

from yacut import app


@app.route('/')
def index_view():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
