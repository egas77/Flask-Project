console.log('Complete connect script user');
$(document).ready(function () {
    let reader = new FileReader();
    let imageInput = $('#input-image');
    let image = $('.user-avatar');
    imageInput.change(function (event) {
        let file = event.target.files[0];
        reader.readAsDataURL(file);
        reader.onload = function () {
            image.attr('src', reader.result);
        };
        reader.onerror = function () {
            console.log(reader.error);
        };
    });

    let activateButton = $('#activate-button');
    activateButton.bind('click', function () {
        activateButton.addClass('disable-button');
        activateButton.attr('disabled', true);
        $.ajax({
            'type': 'GET',
            'url': '/activate-email'
        }).done(function (data) {
            let message = data.message;
            createFlash('warning', message);
        }).fail(function (data) {
            let message = data.message;
            createFlash('error', message);
        }).always(function () {
            activateButton.removeClass('disable-button');
            activateButton.attr('disabled', false);
        });
    });

    let subscribeBlock = $('#sub-block');
    let subscribeButton = $('#subscribe-button');
    let subOnTemplate = $('template#subscribe-on');
    let subOffTemplate = $('template#subscribe-off');
    function subscribe () {
        $.ajax({
            url: '/subscribe',
            method: 'GET'
        }).done(function (data) {
            let subscribeStatus = data.subscribe_status;
            subscribeBlock.empty();
            if (subscribeStatus) {
                subscribeBlock.append(subOnTemplate.html());
            } else {
                subscribeBlock.append(subOffTemplate.html());
            }
            let subscribeButton = $('#subscribe-button');
            subscribeButton.bind('click', subscribe);
        }).fail(function () {
            console.log('Fail subscribe');
        });
    }
    subscribeButton.bind('click', subscribe);
});