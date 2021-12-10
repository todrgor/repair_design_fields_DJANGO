// function start_edit_pub() {
//   console.log('cant edit sorry');
//   url (edit_the_pub.py?idPub=99);
// }

function toggleSavePub_D(idPub) {
  $.ajax({
        url: "/pub/makesaved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
                $('.user_just_saved_it').removeClass('pub_saved');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
                $('.user_just_saved_it').addClass('pub_saved');
                console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function toggleGetNotiFromAuthor(idAccount) {
  $.ajax({
        url: "/account/getNotifications/" + idAccount + "/",

        success: function (data) {
            if (data.result == 0) {
              $('.get_noti').removeClass('noties_gotten');
              console.log("Прекратилось получение уведомлений от автора этой публикации");
            }
            if (data.result == 1) {
              $('.get_noti').addClass('noties_gotten');
              console.log("Началось получение уведомлений от автора этой публикации");
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

$is_opened_pub_additional_functions = 0;
$opened_pub_additional_functions_id = 0;
$is_opened_statistics = 0;
$is_opened_delete_the_pub = 0;
function togglePubAdditionalFunctions(idPub) {
  $('.pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.pub_additional_functions').offset({top:( $('.pub_show_full').offset().top - 30  ), left:( $('.pub_show_full').offset().left + 30  )});
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией, ID:" +idPub);
}
function openNewComplaintForm() {
  // $opened_pub_additional_functions_id
  $('.new_complaint').addClass('show');
  $('.new_complaint').offset({top:( $('.pub_show_full').offset().top - 220  ), left:( $('.pub_show_full').offset().left - 220  )});
}
function shareThePub() {
  // $opened_pub_additional_functions_id
  $('.share_the_pub').addClass('show');
  $('.share_the_pub').offset({top:( $('.pub_show_full').offset().top - 40  ), left:( $('.pub_show_full').offset().left - 220  )});
  $.ajax({
        url: "/pub/change_shared_count/" + $opened_pub_additional_functions_id + "/",

        success: function (data) {
          console.log("Успех c увеличением счётчика репостов");
        },
        error: function (data) {
          console.log("ошибка какая-то c увеличением счётчика репостов");
        }
    });
}
function open_statistics() {
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.statistics').addClass('show');
  $('.pub_additional_functions').css('display', 'none');
  $is_opened_statistics = 1;
  $is_opened_pub_additional_functions = 1;
}
function user_tried_to_delete() {
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.delete_the_pub').addClass('show');
  $('.pub_additional_functions').css('display', 'none');
  $is_opened_delete_the_pub = 1;
  $is_opened_pub_additional_functions = 1;
}
function really_delete() {
  alert('Публикация удалена. Восстановить её не получится.');
  window.location.replace('watch_repairs.html');
}

function new_complaint_was_sent() {
  $idPub = $opened_pub_additional_functions_id;
  $('.pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').toggleClass('show');
  $is_opened_pub_additional_functions = 0;
  $opened_pub_additional_functions_id = 0;
  $('.new_complaint').removeClass('show');
  $('.new_complaint textarea').val('');
  alert('Жалоба успешно отправлена, будет проверена когда-то там');
  console.log("Жалоба типо отпрвлена");
}


$(document).on('click', function(e) {
  if ($is_opened_pub_additional_functions == 1) {
    if ($(e.target).hasClass('pub_additional_functions_bg')) {
      $idPub = $opened_pub_additional_functions_id;
      $('.pub_show_full').removeClass('pub_additional_functions_opened');
      $('.pub_additional_functions_bg').toggleClass('show');
      $is_opened_pub_additional_functions = 0;
      $opened_pub_additional_functions_id = 0;
      $('.new_complaint').removeClass('show');
      $('.share_the_pub').removeClass('show');
      $('.statistics').removeClass('show');
      $('.delete_the_pub').removeClass('show');
      $('.pub_additional_functions').css('display', 'inherit');
      console.log("Закрылись дополнительные действия с публикацией, ID:" +$idPub);
    }
  }

  if ($is_opened_delete_the_pub == 1) {
    if ($(e.target).is('#cancel_deleting') || $(e.target).is('.pub_additional_functions_bg')) {
      $('.delete_the_pub').removeClass('show');
      $('.pub_additional_functions_bg').removeClass('show');
      $('.pub_additional_functions').css('display', 'inherit');
      $is_opened_delete_the_pub = 0;
    }
  }

});

$(window).scroll(function () {
  if ($is_opened_pub_additional_functions == 1) {
    $idPub = $opened_pub_additional_functions_id;
    $('.pub_show_full').removeClass('pub_additional_functions_opened');
    $('.pub_additional_functions_bg').toggleClass('show');
    $is_opened_pub_additional_functions = 0;
    $opened_pub_additional_functions_id = 0;
    $is_opened_statistics = 0;
    $is_opened_delete_the_pub = 0;
    $('.new_complaint').removeClass('show');
    $('.share_the_pub').removeClass('show');
    $('.statistics').removeClass('show');
    $('.delete_the_pub').removeClass('show');
    $('.pub_additional_functions').css('display', 'inherit');
    console.log("Дополнительные действия с публикацией закрылись :3, ID:" +$idPub);
  }
});
