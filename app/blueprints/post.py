from flask import Blueprint, render_template, request, make_response, jsonify
from flask_login import login_required

blueprint_post = Blueprint('post', __name__, template_folder='templates')


@blueprint_post.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
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
