
if ($('.bio.notNone').length) {
  $('.bio.notNone').offset({top: ( $('.bio.notNone').offset().top) - 40, left:( $('.user_role').offset().left) + 10});
}
if ($('.bio.None').length) {
  $('.bio.None').offset({top: ( $('.user_role').offset().top) +40, left:( $('.user_role').offset().left) - 10});
}

function YouHaveToLogin(action) {
  alert('Вам нужно авторизоваться перед тем, как ' + action + '.')
}

function start_loading_animation(idPub) {
  $('.pub_one#'+idPub+' .user_just_saved_it img').attr('src', '/static/sources/SVG/heart_loading.gif');
  $('.pub_one#'+idPub+' .user_just_saved_it input').val('Загрузка...');
}

function end_loading_animation(idPub) {
  $('.pub_one#'+idPub+' .user_just_saved_it img').attr('src', '/static/sources/SVG/heart.svg');
  console.log("loading ended");
}

function toggleSavePub_LH(idPub) {
  console.log("$(this): ", $(this));
  start_loading_animation(idPub);

  $.ajax({
        url: "/pub/" + idPub + "/toggle_saved/",

        success: function (data) {
            end_loading_animation(idPub);

            if (data.result == 0) {
                $('.pub_one#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one#'+idPub+' .user_just_saved_it').addClass('pub_saved');
              console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          end_loading_animation(idPub);
          console.log("ошибка какая-то");
        }
    });
}

function toggleSavePub_D(idPub) {
  console.log("$(this): ", $(this));
  start_loading_animation(idPub);

  $.ajax({
        url: "/pub/" + idPub + "/toggle_saved/",

        success: function (data) {
            end_loading_animation(idPub);

            if (data.result == 0) {
                $('.pub_one#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                $('.pub_one#'+idPub+' .user_just_saved_it input').val('В «Избранное»');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one#'+idPub+' .user_just_saved_it').addClass('pub_saved');
              $('.pub_one#'+idPub+' .user_just_saved_it input').val('Сохранено');
              console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          end_loading_animation(idPub);
          $('.pub_one#'+idPub+' .user_just_saved_it input').val('Попробуйте ещё раз...');
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
              $('a#'+idAccount+' .get_noti').removeClass('noties_gotten, loading');
              console.log("Прекратилось получение уведомлений от автора этой публикации");
            }
            if (data.result == 1) {
              $('.get_noti').removeClass('loading');
              $('a#'+idAccount+' .get_noti').addClass('noties_gotten');
              console.log("Началось получение уведомлений от автора этой публикации");
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function openNewComplaintForm() {
  $(' .new_complaint').addClass('show');
  $('.delete_the_pub, .share_the_pub, .statistics').removeClass('show');
}

function new_complaint_was_sent() {
  if (!$('.new_complaint textarea').val().match(/^\s*$/)) {
    $photos = $('.new_complaint input[type="file"]')[0].files;
    $data = new FormData();

    if ($('.pub_additional_functions_bg#author').hasClass('show')) {
      $data.append( 'complaint_type', 12 );
      $('.additionalFunctions').removeClass('opened');
    }
    if ($('.pub_additional_functions_bg#pub').hasClass('show')) {
      $data.append( 'complaint_type', 11 );
      $('.pub_show_full').removeClass('pub_additional_functions_opened');
    }

    if ( typeof $photos != 'undefined' ) {
      // заполняем объект данных файлами в подходящем для отправки формате
      $.each( $photos, function( key, value ){
        console.log('key: ', key, 'value: ', value.name, value);
    		$data.append( value.name, value );
    	});
    }

    $data.append( 'complaint_id', $opened_pub_additional_functions_id );
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
            $('.new_complaint textarea').val('');
            alert('Жалоба принята, ждите решения модерации. Ответ Вы получите в уведомлении.');
          },
          error: function (data) {
            alert("Какая-то ошибка с жалобой... Попробуйте спустя время отправить снова!");
          }
      });

      close_additional_functions();
  } else {
    alert('Жалоба не отправлена, для начала напишите её!');
  }
}

function shareThePub() {
  server_url = 'todrgor.pythonanywhere.com';
  pub_url = server_url + $('.lifehack#' + $opened_pub_additional_functions_id + ' .pub_url').html();
  $('.new_complaint, .statistics, .delete_the_pub, .delete_the_user').removeClass('show');
  $('.share_the_pub').addClass('show');
  $('.share_the_pub a').html(pub_url).attr('href', pub_url);
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

function showThePubStatistic() {
  $('.statistics.visible_block h1').html('Статистика по публикации «' + $('.lifehack#'+ $opened_pub_additional_functions_id +' .div_pub_text .pub_text').html() +'»:');
  $('.statistics.visible_block .seen_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .seen_count').html());
  $('.statistics.visible_block .saved_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .saved_count').html());
  $('.statistics.visible_block .average_age_watchers').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .average_age_watchers').html());
  $('.statistics.visible_block .average_age_savers').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .average_age_savers').html());
  $('.statistics.visible_block .shared_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .shared_count').html());
  $('.statistics.visible_block .reported_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .reported_count').html());
  $('.delete_the_user, .new_complaint, .share_the_pub, .delete_the_pub').removeClass('show');
  $('.statistics').addClass('show');
}

function deleteTheUser() {
  $('.delete_the_pub, .new_complaint, .share_the_pub, .statistics').removeClass('show');
  $('.delete_the_user').addClass('show');
}

function deleteThePub() {
  $('.delete_the_pub h1').html('Вы точно хотите удалить публикацию «'+ $('.lifehack#'+ $opened_pub_additional_functions_id +' .div_pub_text .pub_text').html() +'»?');
  $('.delete_the_pub a#delete').attr('href', $('.lifehack#'+ $opened_pub_additional_functions_id +' .delete_url').html());
  $('.delete_the_user, .new_complaint, .share_the_pub, .statistics').removeClass('show');
  $('.delete_the_pub').addClass('show');
}

function checkScrollForVideo() {
  var fraction = 0.9; // Play video when 80% of the player is visible.

  $('video').each(function(){
    var video = $(this).get(0);
    var x = video.offsetLeft, y = video.offsetTop, w = video.offsetWidth, h = video.offsetHeight, r = x + w, //right
        b = y + h, //bottom
        visibleX, visibleY, visible;

        visibleX = Math.max(0, Math.min(w, window.pageXOffset + window.innerWidth - x, r - window.pageXOffset));
        visibleY = Math.max(0, Math.min(h, window.pageYOffset + window.innerHeight - y, b - window.pageYOffset));

        visible = visibleX * visibleY / (w * h);

    if (visible > fraction) {
        $(this).removeClass('paused');
        video.play();
        console.log("видео начало воспроизвоиться");
    } else {
        video.pause();
        console.log("видео не начало / перестало воспроизвоиться");
        $(this).addClass('paused');
    }
  })
}

$MillisecondsToSetThePubSeen = 2000;
$scrollTopOld = $(window).scrollTop();
$SeenPubsList = [];
$AllPubsList = [];
secundomer = false;
$('.lifehack').each(function(){
  var pub = $(this).get(0);
  $AllPubsList.push(pub.id);
})

function startSecundomer() {
  if (($SeenPubsList.length) < ($AllPubsList.length)) {
    if (secundomer) {
      clearInterval(secundomer); // остановить секндомер и запустить его снова
    }
    secundomer = setInterval(setThePubSeen, $MillisecondsToSetThePubSeen);
  } else {
    clearInterval(secundomer); // остановить секндомер
    secundomer = false;
  }
}

function setThePubSeen() {
  var fraction = 0.85; // set the pub seen when 90% of the pub is visible.
  $scrollTopNow = $(window).scrollTop();
  if (($scrollTopOld == $scrollTopNow) || // если пользователь не скроллил или сделал это совсем чуть-чуть
     (($scrollTopOld > $scrollTopNow) && (($scrollTopOld / $scrollTopNow) >= fraction)) ||
     (($scrollTopOld < $scrollTopNow) && (($scrollTopNow / $scrollTopOld) >= fraction)))
  {
    $('.lifehack').each(function(){
      var pub = $(this).get(0);
      if ($.inArray(pub.id, $SeenPubsList) == -1) { // если публикация до этого не была видна
        var x = pub.offsetLeft, y = pub.offsetTop, w = pub.offsetWidth, h = pub.offsetHeight, r = x + w, //right
            b = y + h, //bottom
            visibleX, visibleY, visible;

            visibleX = Math.max(0, Math.min(w, window.pageXOffset + window.innerWidth - x, r - window.pageXOffset));
            visibleY = Math.max(0, Math.min(h, window.pageYOffset + window.innerHeight - y, b - window.pageYOffset));

            visible = visibleX * visibleY / (w * h);

        if (visible >= fraction) { // если публикация достаточно в зоне видимости
            $SeenPubsList.push(pub.id);
            $.ajax({
                  url: "/pub/" + pub.id + "/set_seen/",

                  success: function (data) {
                    console.log("+1 к счётчику просмотров публикации с ID:" +pub.id);
                  },
                  error: function (data) {
                    console.log("ошибка какая-то c счётчиком просмотров, ID если что:" +pub.id);
                  }
              });
        }
      }
    })
  } else {  // если пользователь скроллил и не чуть-чуть
    startSecundomer(); // то остановить секндомер и запустить его снова
  }

  console.log('SeenPubsList: ' + $SeenPubsList);
  $scrollTopOld = $(window).scrollTop();
}

$is_opened_pub_additional_functions = 0;
$opened_pub_additional_functions_id = 0;

function togglePubAdditionalFunctions(idPub) {
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;

  $('.pub_additional_functions_bg#pub .selected_tags').html('');
  if ($('.lifehack#'+ idPub +' .selected_tag').length > 0 ) {
    $('.pub_additional_functions_bg#pub .opened_filter_form').css('display', 'block');
    $('.lifehack#'+ idPub +' .selected_tag').each(function () {
      $('.pub_additional_functions_bg#pub .selected_tags').html(
        $('.pub_additional_functions_bg#pub .selected_tags').html() + ' <input type="hidden" name="'+ this.name +'" value="'+ this.value +'" class="selected_tag">'
      );
    })
  } else {
    $('.pub_additional_functions_bg#pub .opened_filter_form').css('display', 'none');
  }

  if ($('.lifehack#'+ idPub +' .info_for_author_or_admin').length > 0) {
    $('.pub_additional_functions .for_author_or_admin.edit').attr('href', $('.lifehack#'+ idPub +' .edit_url').html());
    $('.pub_additional_functions .for_author_or_admin').addClass('show');
  }

  $('.pub_one.lifehack#'+ idPub +' .pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg#pub').toggleClass('show');
  $('.pub_additional_functions').offset({
    top: ( $('.pub_one.lifehack#'+ idPub +' .pub_show_full').offset().top) -20,
    left: ( $('.pub_one.lifehack#'+ idPub +' .pub_show_full').offset().left) -25
  });
  console.log("Открыты дополнителknknjnjnjnjnjьные действия с публикацией под ID "+ idPub);
}

function togglePubAdditionalFunctionsAuthor(idPub) {
  $('.photo_nickname_role_additionalFunctions .additionalFunctions').toggleClass('opened');
  $('.pub_additional_functions_bg#author').toggleClass('show');
  $('.pub_additional_functions_bg#author .pub_additional_functions').offset({
    top: ( $('.photo_nickname_role_additionalFunctions .additionalFunctions').offset().top) -20,
    left: ( $('.photo_nickname_role_additionalFunctions .additionalFunctions').offset().left) -25
  });
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}

function close_additional_functions() {
  if ($is_opened_pub_additional_functions == 1) {
    $idPub = $opened_pub_additional_functions_id;
    $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
    $is_opened_pub_additional_functions = $opened_pub_additional_functions_id = 0;
    $('.pub_additional_functions_bg, .delete_the_user, .new_complaint, .share_the_pub, .statistics, .delete_the_pub, .for_author_or_admin').removeClass('show');
    $('.photo_nickname_role_additionalFunctions .additionalFunctions').removeClass('opened');
    console.log("Закрылись дополнительные действия с публикацией с ID "+ $idPub);
    console.log("pub_additional_functions_bg closed");
  }
}


$(document).ready(function() {
  checkScrollForVideo();
  startSecundomer();
});

$(document).on('click', function(e) {
  if ($(e.target).hasClass('pub_additional_functions_bg') || $(e.target).hasClass('cancel')) {
    close_additional_functions();
  }
});


$(window).scroll(function () {
  checkScrollForVideo();
  close_additional_functions();
  startSecundomer();
});

function togglePubAdditionalFunctionsAuthor_and_deleteTheUser() {
  $is_opened_pub_additional_functions = 1;
  $('.pub_additional_functions_bg#author').toggleClass('show');
  deleteTheUser();
}
