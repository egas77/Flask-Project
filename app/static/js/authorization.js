console.log('Complete connect script authorization');
$(document).ready(function () {
   let loginForm = $('.login-form');
   console.log(loginForm);
   loginForm.submit(function (event) {
      event.preventDefault();
      $.ajax({
         type: 'POST',
         url: '/login',
         data: loginForm.serialize()
      }).fail(function (error) {
         for (let key in error.responseJSON.message) {
            let message = key + ': ' + error.responseJSON.message[key];
            createFlash('error', message);
         }
      }).done(function (data) {
         if (data.redirect) {
            window.location.href = data.redirect_url;
         }
      });
   });
});