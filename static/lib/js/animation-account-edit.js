function cancel_following(idAccount) {
  $.ajax({
        url: "/account/getNotifications/" + idAccount + "/",

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
