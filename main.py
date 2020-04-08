from flask import render_template, flash
from sqlalchemy import desc

import os

from app import app
from app.models import Post


@app.route('/')
@app.route('/index')
def index():
    posts = Post.get_query().order_by(desc(Post.id)).all()

    return render_template('index.html', posts=posts)


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
