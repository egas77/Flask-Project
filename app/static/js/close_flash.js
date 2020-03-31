$(document).ready(function () {
   let flashesItems = $('.flashes li');
   for (let flashItem of flashesItems) {
      let closeButton = $(flashItem).children('button');
      closeButton.bind('click', function () {
         $(this).parent().remove();
      })
   }
});