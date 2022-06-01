
function cancel_following(idAccount) {
  $.ajax({
        url: "/account/" + idAccount + "/toggleNotifications/",

        success: function (data) {
            if (data.result == 0) {
              $('.user_one#'+idAccount+' .cancel_following').addClass('dont_cancel');
              $('.user_one#'+idAccount+' .cancel_following').html('Подписаться');
              console.log("Прекратилось получение уведомлений");
            }
            if (data.result == 1) {
              $('.user_one#'+idAccount+' .cancel_following').removeClass('dont_cancel');
              $('.user_one#'+idAccount+' .cancel_following').html('Отписаться');
              console.log("Началось получение уведомлений");
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function deleteTheUser() {
  $('.additional_functions_bg, .delete_the_user').addClass('show');
}

function close_additional_functions() {
  $('.additional_functions_bg, .delete_the_user').removeClass('show');
  console.log("Закрылись дополнительные действия с публикацией с ID ");
}

$(document).on('click', function(e) {
  if ($(e.target).hasClass('additional_functions_bg') || $(e.target).hasClass('cancel')) {
    console.log("additional_functions_bg closed");
    close_additional_functions();
  }
});
