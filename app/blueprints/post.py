from flask import Blueprint, render_template, request, make_response, jsonify
from flask_login import login_required

from app import get_session
from app.models import Post

blueprint_post = Blueprint('post', __name__, template_folder='templates')


@blueprint_post.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        post = Post()
        title = request.form.get('title-post')
        content = request.form.get('content', None)
        post.title = title
        post.content = content
        session = get_session()
        session.add(post)
        session.commit()
    return render_template('new_post.html')


@blueprint_post.route('/upload-image', methods=['POST'])
@login_required
def upload_image_creator():
    image = request.files.get('upload')
    url_image = 'static/img/' + image.filename
    image.save('app/' + url_image)
    print(request.files)
    return make_response(jsonify({
        'uploaded': 1,
        'fileName': image.filename,
        'url': url_image
    }))
