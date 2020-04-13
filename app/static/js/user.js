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
            $.ajax({
                'url': '/user-image',
                'type': 'POST',
                'data': {'image': reader.result}
            }).done(function () {
                console.log('DONE IMAGE');
            }).fail(function (error) {
                console.log(error);
            });
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

    function subscribe() {
        $.ajax({
            url: '/subscribe',
            type: 'GET'
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

    let nicknameModal = $('#nickname-modal');
    let nicknameModalCloseButton = nicknameModal.find('.close-model');
    let nicknameModalForm = nicknameModal.find('form');
    let nicknameOpenModelButton = $('#open-model-nickname');
    let nicknameString = $('#nickname');
    nicknameOpenModelButton.bind('click', function () {
        nicknameModal.addClass('modal-visible');
    });
    nicknameModalCloseButton.bind('click', function () {
        nicknameModal.removeClass('modal-visible');
    });
    nicknameModalForm.bind('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: '/edit-user',
            type: 'POST',
            data: nicknameModalForm.serialize()
        }).done(function () {
            let newNickname = nicknameModalForm.serializeArray()[0].value;
            nicknameString.text('Никнейм: ' + newNickname);
            nicknameModal.removeClass('modal-visible');
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        });
    });

    let emailModal = $('#email-modal');
    let emailModalCloseButton = emailModal.find('.close-model');
    let emailModalForm = emailModal.find('form');
    let emailOpenModelButton = $('#open-model-email');
    let emailString = $('#email');
    emailOpenModelButton.bind('click', function () {
        emailModal.addClass('modal-visible');
    });
    emailModalCloseButton.bind('click', function () {
        emailModal.removeClass('modal-visible');
    });
    emailModalForm.bind('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: '/edit-user',
            type: 'POST',
            data: emailModalForm.serialize()
        }).done(function () {
            let newEmail = emailModalForm.serializeArray()[0].value;
            emailString.text('Почта: ' + newEmail);
            emailModal.removeClass('modal-visible');
            document.location.href = '/logout';
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        });
    });

    let passwordModal = $('#password-modal');
    let passwordModalCloseButton = passwordModal.find('.close-model');
    let passwordModalForm = passwordModal.find('form');
    let passwordOpenModelButton = $('#open-model-password');
    passwordOpenModelButton.bind('click', function () {
        passwordModal.addClass('modal-visible');
    });
    passwordModalCloseButton.bind('click', function () {
        passwordModal.removeClass('modal-visible');
    });
    passwordModalForm.bind('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: '/edit-user',
            type: 'POST',
            data: passwordModalForm.serialize()
        }).done(function () {
            passwordModal.removeClass('modal-visible');
            createFlash('success', 'Пароль успешно изменен');
        }).fail(function (error) {
            for (let key in error.responseJSON.message) {
                let message = key + ': ' + error.responseJSON.message[key];
                createFlash('error', message);
            }
        });
    });

    let importanceButton = $('#importance-button');
    let importanceSelect = $('select#importance');
    let userId = $('#user-id').val();
    importanceButton.click(function () {
        let optionImportanceSelect = $('select#importance option:selected');
        let text = optionImportanceSelect.text();
        let importanceValue = importanceSelect.val();
        $.ajax({
            url: '/edit-importance',
            type: 'POST',
            data: {
                importance: importanceValue,
                user_id: userId
            }
        }).done(function () {
            document.location.href = `/user/${userId}`;
        }).fail(function () {

        });
    });
});