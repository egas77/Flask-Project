$(document).ready(function () {
    InlineEditor
        .create(document.querySelector('#editor'), {

            toolbar: {
                items: [
                    '|',
                    'bold',
                    'italic',
                    'link',
                    'bulletedList',
                    'numberedList',
                    '|',
                    'indent',
                    'outdent',
                    '|',
                    'blockQuote',
                    'undo',
                    'redo'
                ]
            },
            language: 'ru',
            licenseKey: '',

        })
        .then(editor => {
            window.editor = editor;


        })
        .catch(error => {
            console.error('Oops, something gone wrong!');
            console.error('Please, report the following error in the https://github.com/ckeditor/ckeditor5 with the build id and the error stack trace:');
            console.warn('Build id: ytvryc82pkf4-171lbhbpe7s4');
            console.error(error);
        });
    let commentForm = $('#comment-form');
    let userId = commentForm.children('#user-id').val();
    let postId = commentForm.children('#post-id').val();
    commentForm.submit(function (event) {
        event.preventDefault();
        let content = editor.getData();
        if (!content) {
            createFlash('error', 'Текст комментария пустой');
        }
        else {
            $.ajax({
                'url': '/create_comment',
                'type': 'POST',
                'data': {
                    'user_id': userId,
                    'post_id': postId,
                    'content': content
                }
            }).done(function () {
                editor.setData('');
                document.location.href = `/post/${postId}`;
            });
        }
    });
});