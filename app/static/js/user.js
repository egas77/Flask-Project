console.log('Complete connect script user');
$(document).ready(function () {
    let reader = new FileReader();
    let imageInput = $('#input-image');
    let image = $('.user-avatar');
    imageInput.change(function (event) {
        let file = event.target.files[0];
        reader.readAsDataURL(file);
        reader.onload = function() {
            image.attr('src', reader.result);
        };
        reader.onerror = function() {
            console.log(reader.error);
        };
    })
});