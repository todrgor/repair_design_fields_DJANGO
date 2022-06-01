
function start_loading_animation() {
  $('.user_just_saved_it img').attr('src', '/static/sources/SVG/heart_loading.gif');
  $('.user_just_saved_it input').val('Загрузка...');
}

function end_loading_animation() {
  $('.user_just_saved_it img').attr('src', '/static/sources/SVG/heart.svg');
  console.log("loading ended");
}

function toggleSavePub_D(idPub) {
  console.log("$(this): ", $(this));
  start_loading_animation(idPub);

 $.ajax({
        url: "/pub/" + idPub + "/toggle_saved/",

        success: function (data) {
            end_loading_animation(idPub);

            if (data.result == 0) {
                $('.user_just_saved_it').removeClass('pub_saved');
                $('.user_just_saved_it input').val('В «Избранное»');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
                $('.user_just_saved_it').addClass('pub_saved');
                $('.user_just_saved_it input').val('Сохранено');
                console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          end_loading_animation();
          $('.user_just_saved_it input').val('Попробуйте ещё раз...');
          console.log("ошибка какая-то");
        }
    });
}

function toggleGetNotiFromAuthor(idAccount) {
  $('.get_noti').removeClass('noties_gotten');
  $('.get_noti').addClass('loading');

  $.ajax({
        url: "/account/" + idAccount + "/toggleNotifications/",

        success: function (data) {
            if (data.result == 0) {
              $('.get_noti').removeClass('noties_gotten, loading');
              console.log("Прекратилось получение уведомлений от автора этой публикации");
            }
            if (data.result == 1) {
              $('.get_noti').removeClass('loading');
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
  $('.pub_additional_functions').offset({
    top: ( $('.pub_show_full').offset().top) -20,
    left: ( $('.pub_show_full').offset().left) -25
  });
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией, ID:" +idPub);
}

function openNewComplaintForm() {
  $('.new_complaint').addClass('show');
  $('.new_complaint').offset({top:( $('.pub_show_full').offset().top - 220  ), left:( $('.pub_show_full').offset().left - 220  )});
}

function shareThePub() {
  $('.share_the_pub').addClass('show');
  $('.share_the_pub').offset({top:( $('.pub_show_full').offset().top - 40  ), left:( $('.pub_show_full').offset().left - 220  )});
  $.ajax({
        url: "/pub/" + $opened_pub_additional_functions_id + "/change_shared_count/",

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
  if (!$('.new_complaint textarea').val().match(/^\s*$/)) {
    $('.pub_show_full').removeClass('pub_additional_functions_opened');
    $('.pub_additional_functions_bg').removeClass('show');
    $('.new_complaint').removeClass('show');

    // подготовка загружаемых файлов к отправке
    $photos = $('.new_complaint input[type="file"]')[0].files;
    $data = new FormData();

    if( typeof $photos != 'undefined' ) {
      // заполняем объект данных файлами в подходящем для отправки формате
      $.each( $photos, function( key, value ){
        console.log('key: ', key, 'value: ', value.name, value);
    		$data.append( value.name, value );
    	});
    }

    $data.append( 'complaint_id', $opened_pub_additional_functions_id );
    $data.append( 'complaint_type', 11 );
    $data.append( 'complaint_text', $('.new_complaint textarea').val() );
    $.ajax({
          type: "POST",
          url: "/admin/new_complaint/",
          data: $data,
          files: $data,
          dataType    : 'json',
      		// отключаем обработку передаваемых данных, пусть передаются как есть
      		processData : false,
      		// отключаем установку заголовка типа запроса. Так jQuery скажет серверу что это строковой запрос
      		contentType : false,

          success: function (data) {
            alert('Жалоба принята, ждите решения модерации. Ответ Вы получите в уведомлении.');
            $('.new_complaint textarea').val('');
          },
          error: function (data) {
            alert("Какая-то ошибка с жалобой... Попробуйте спустя время отправить снова!");
          }
      });

    $is_opened_pub_additional_functions = 0;
    $opened_pub_additional_functions_id = 0;
  } else {
    alert('Жалоба не отправлена, для начала напишите её!');
  }
}


$(document).on('click', function(e) {
  if ($is_opened_pub_additional_functions == 1) {
    if ($(e.target).hasClass('pub_additional_functions_bg') || $(e.target).hasClass('cancel')) {
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
