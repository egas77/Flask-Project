function createFlash(type, message) {
    let flashItem = $(
        document.querySelector('template#flash-item').content).children('li').clone();
    flashItem.addClass(type);
    flashItem.children('.message-flash').text(message);
    $('ul.flashes').append(flashItem);
    bindCloseButton(flashItem);
}


function bindCloseButton(flashItem) {
    let closeButton = flashItem.children('button.close-flash');
    closeButton.bind('click', function () {
        $(this).parent().remove();
    });
}


$(document).ready(function () {
    let flashesItems = $('.flashes li');
    for (let flashItem of flashesItems) {
        bindCloseButton($(flashItem));
    }
});