console.log('Complete connect script registration');
$(document).ready(function () {
    let registrationForm = $('.registration-form');
    let submitButton = $('#submit');
    console.log(submitButton);
    registrationForm.submit(function (event) {
        submitButton.addClass('disable-button');
        submitButton.attr('disabled', true);
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/registration',
            data: registrationForm.serialize()
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        }).done(function (data) {
            if (data.redirect) {
                window.location.href = data.redirect_url;
            }
        }).always(function () {
            submitButton.removeClass('disable-button');
            submitButton.attr('disabled', false);
        });
    });
});