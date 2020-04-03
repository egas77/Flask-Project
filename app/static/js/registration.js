console.log('Complete connect script registration');
$(document).ready(function () {
    let registrationForm = $('.registration-form');
    registrationForm.submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/registration',
            data: registrationForm.serialize(),
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        }).done(function (data) {
            console.log(data);
            if (data.redirect) {
                window.location.href = data.redirect_url;
            }
        });
    });
});