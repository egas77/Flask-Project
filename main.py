from flask import render_template, flash

import os

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    flash(error, 'error')
    return render_template('index.html'), 404


@app.errorhandler(401)
def login_error(error):
    flash(error, 'error')
    return render_template('index.html'), 401


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run()
