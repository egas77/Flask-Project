$(document).ready(function () {
    let deleteButtons = $('.delete-post-button');
    for (let button of deleteButtons) {
        deletePostHandler(button);
    }
})

let deletePostHandler = function (button) {
    let postId = button.getAttribute('id');
    let modalWindow = $('.modal-window' + '.' + postId);
    let closeButton = modalWindow.find('.close-model');
    let removeForm = modalWindow.find('form');
    closeButton.bind('click', function () {
        modalWindow.removeClass('modal-visible');
    })
    button.addEventListener('click', function () {
        modalWindow.addClass('modal-visible');
    })
    removeForm.bind('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: `/post-api/${postId}`,
            type: 'DELETE'
        }).done(function () {
            document.location.href = '/';
        }).fail(function (error) {
            console.log(error);
        })
    });
}


