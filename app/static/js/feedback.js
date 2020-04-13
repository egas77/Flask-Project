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
    let feedbackForm = $('#feedback-form');
    let submitButton = $('input[type=submit]');
    feedbackForm.submit(function (event) {
        event.preventDefault();
        let content = editor.getData();
        if (!content) {
            createFlash('error', 'Текст сообщения пустой');
        } else {
            submitButton.addClass('disable-button');
            submitButton.attr('disabled', true);
            $.ajax({
                url: '/feedback',
                type: 'POST',
                data: {content: content}
            }).done(function () {
                createFlash('success', 'Сообщение отправлено')
            }).fail(function () {
                createFlash('error', 'Сообщение не доставлено')
            }).always(function () {
                submitButton.removeClass('disable-button');
                submitButton.attr('disabled', false);
            });
        }
    });
});