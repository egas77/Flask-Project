from flask import render_template
from flask_login import login_required

from app import app, login_manager
from app.forms import RegisterForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_required
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm


if __name__ == '__main__':
    app.run()
