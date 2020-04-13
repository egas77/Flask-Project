from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from sqlalchemy import desc

import os
import flask_ngrok

from app import app
from app.models import Post


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    posts = Post.get_query().order_by(desc(Post.publication_date)
                                      ).paginate(page, app.config.get('POSTS_ON_PAGE', 5), True)
    return render_template('index.html', posts=posts)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if not current_user.is_authenticated:
        flash('Авторизуйтесь для использования обратной связи', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        pass
    return render_template('feedback.html')


@app.errorhandler(404)
def page_not_found(error):
    flash(error, 'error')
    return render_template('errorhandler.html', error=error), 404


@app.errorhandler(401)
def login_error(error):
    flash(error, 'error')
    return render_template('errorhandler.html', error=error), 401


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
