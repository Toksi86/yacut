from yacut import app


@app.route('/')
def the_view(): return 'ok'


if __name__ == '__main__':
    app.run()
