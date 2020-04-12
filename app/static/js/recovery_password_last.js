$(document).ready(function () {
    let recoveryPasswordForm = $('#recovery-password-form');
    let submitButton = $('#submit');
    let token = $('#token').val();
    recoveryPasswordForm.submit(function (event) {
        event.preventDefault();
        submitButton.addClass('disable-button');
        submitButton.attr('disabled', true);
        $.ajax({
            'url': `/recovery-password-last/${token}`,
            'type': 'POST',
            'data': recoveryPasswordForm.serialize()
        }).done(function (data) {
            if (data.redirect) {
                window.location.href = data.redirect_url;
            }
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        }).always(function () {
            submitButton.removeClass('disable-button');
            submitButton.attr('disabled', false);
        });
    });
});