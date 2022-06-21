let $avatar_wrap = $('.avatar_btn');
let $notifications_wrap = $('.notifications_btn');
let $filter_button = $('.filter_button');
var $is_opened_avatar = $is_opened_notifications = $is_opened_filter_panel = $is_opened_reg_auth_form = 0;

$avatar_wrap.on('click', function () {
    $('.avatar_container').toggleClass('show_avtr_optns');
    if ($is_opened_avatar == 0) {
      $is_opened_avatar = 1;
    } else {
      $is_opened_avatar = 0;
    }
});

function open_noti(idAccount) {
    $('.notifications_mini .notifications_mini_p').css('display', 'none');
    $('.notifications_container').toggleClass('show_ntfctns_more');
    if ($is_opened_notifications == 0) {
      $is_opened_notifications = 1;
    } else {
      $is_opened_notifications = 0;
    }
    if ($('.noti_new').length) {
      $.ajax({
        url: "/account/" + idAccount + "/NewNotiWereSeen/",

        success: function (data) {
          if (data.result == 0) {
            console.log("НЕт новых уведомлений");
          }
          if (data.result == 1) {
            console.log("Все новые уведомления теперь прочитаны");
          }
        },
        error: function (data) {
          console.log("ошибка какая-то с уведомлениями");
        }
      });
    }
};

$filter_button.on('click', function () {
    $('.opened_filter_big_bg').toggleClass('opened_filter_big_bg_opened');
    if ($is_opened_filter_panel == 0) {
      $is_opened_filter_panel = 1;
    } else {
      $is_opened_filter_panel = 0;
    }
});


$(document).click( function(event) {
  if ($is_opened_avatar == 1 &&
      !event.target.classList.contains("avatar_container") &&
      !event.target.classList.contains("avatar_options_mini") &&
      !event.target.classList.contains("avatar_btn") &&
      !event.target.classList.contains("account_img") &&
      !event.target.classList.contains("avatar_options_mini_p") &&
      !event.target.classList.contains("avatar_triangle") &&
      (!$('.avatar_options').is(":hover")) ) {

    $('.avatar_container').removeClass('show_avtr_optns');
    $is_opened_avatar = 0;
    console.log('$is_opened_avatar = 0;');
  }

  if ($is_opened_notifications == 1 &&
      !event.target.classList.contains("notifications_container") &&
      !event.target.classList.contains("notifications_mini") &&
      !event.target.classList.contains("notifications_btn") &&
      !event.target.classList.contains("noti_logo") &&
      !event.target.classList.contains("notifications_mini_p") &&
      !event.target.classList.contains("to_notifications") &&
      (!$('.notifications_opened').is(":hover")) ) {

    $('.notifications_container').removeClass('show_ntfctns_more');
    $is_opened_notifications = 0;
    console.log('$is_opened_notifications = 0;');
  }

  if ($is_opened_filter_panel == 1 &&
    !event.target.classList.contains("filter_btn") &&
    !event.target.classList.contains("dont_close_on_click") &&
    !event.target.classList.contains("opened_filter") &&
    (!$('.opened_filter').is(":hover")) ) {

    $('.opened_filter_big_bg').removeClass('opened_filter_big_bg_opened');
    $is_opened_filter_panel = 0;
    console.log('$is_opened_filter_panel = 0;');
  }
});
