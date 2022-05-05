function toggleRemovePubFromSaved_D(idPub) {
  $.ajax({
        url: "/pub/make_saved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
              $('.pub_one.design#'+idPub+' .remove_pub_from_saved').addClass('pub_removed');
              $('.pub_one.design#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/come_back_to_saved.svg");
              $('.pub_one.design#'+idPub+" .div_pub_text").css('min-height', '100px');
              $('.pub_one.design#'+idPub+" .div_pub_text").css('max-height', '140px');
              $('.pub_one.design#'+idPub+" .remove_pub_from_saved img").attr("title","Публикация удалена. Восстановить её можно, пока не перезагрузите страницу");
              $('.pub_one.design#'+idPub+' .p_for_removed_pubs').addClass('show');
              console.log("Удалена из избранного публикация о дизайне под ID "+idPub);
            }
            if (data.result == 1) {
              $('.pub_one.design#'+idPub+' .remove_pub_from_saved').removeClass('pub_removed');
              $('.pub_one.design#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/remove_from_saved.svg");
              $('.pub_one.design#'+idPub+" .div_pub_text").css('min-height', '180px');
              $('.pub_one.design#'+idPub+" .div_pub_text").css('max-height', '180px');
              $('.pub_one.design#'+idPub+" .remove_pub_from_saved img").attr("title","Удалить из «Избранного»");
              $('.pub_one.design#'+idPub+' .p_for_removed_pubs').removeClass('show');
              console.log("Публикация восстановлена в избранное о дизайне под ID "+idPub);
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function toggleRemovePubFromSaved_R (idPub) {
  $.ajax({
        url: "/pub/make_saved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
              $('.pub_one.repair#'+idPub+' .remove_pub_from_saved').addClass('pub_removed');
              $('.pub_one.repair#'+idPub+" .additional_functions").css("width","43%");
              $('.pub_one.repair#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/come_back_to_saved.svg");
              $('.pub_one.repair#'+idPub+" .remove_pub_from_saved img").attr("title","Публикация удалена. Восстановить её можно, пока не перезагрузите страницу");
              $('.pub_one.repair#'+idPub+' .p_for_removed_pubs').addClass('show');
              console.log("Публикация удалена из избранного о ремонте под ID "+idPub);
            }
            if (data.result == 1) {
              $('.pub_one.repair#'+idPub+' .remove_pub_from_saved').removeClass('pub_removed');
              $('.pub_one.repair#'+idPub+" .additional_functions").css("width","14%");
              $('.pub_one.repair#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/remove_from_saved.svg");
              $('.pub_one.repair#'+idPub+" .remove_pub_from_saved img").attr("title","Удалить из «Избранного»");
              $('.pub_one.repair#'+idPub+' .p_for_removed_pubs').removeClass('show');
              console.log("Публикация восстановлена в избранное о ремонте под ID "+idPub);
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function toggleRemovePubFromSaved_LH(idPub) {
  $.ajax({
        url: "/pub/make_saved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
              $('.pub_one.lifehack#'+idPub+' .remove_pub_from_saved').addClass('pub_removed');
              $('.pub_one.lifehack#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/come_back_to_saved.svg");
              $('.pub_one.lifehack#'+idPub+" .div_pub_text").css('max-height', '255px');
              $('.pub_one.lifehack#'+idPub+" .remove_pub_from_saved img").attr("title","Публикация удалена. Восстановить её можно, пока не перезагрузите страницу");
              $('.pub_one.lifehack#'+idPub+' .p_for_removed_pubs').addClass('show');
              console.log("Удалена из избранного публикация-лайфхак под ID "+idPub);
            }
            if (data.result == 1) {
              $('.pub_one.lifehack#'+idPub+' .remove_pub_from_saved').removeClass('pub_removed');
              $('.pub_one.lifehack#'+idPub+" .remove_pub_from_saved img").attr("src","/static/sources/SVG/remove_from_saved.svg");
              $('.pub_one.lifehack#'+idPub+" .div_pub_text").css('max-height', '270px');
              $('.pub_one.lifehack#'+idPub+" .remove_pub_from_saved img").attr("title","Удалить из «Избранного»");
              $('.pub_one.lifehack#'+idPub+' .p_for_removed_pubs').removeClass('show');
              console.log("Восстановлена в избранное публикация-лайфхак под ID "+idPub);
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
              $('.pub_one.lifehack a#'+idAccount+' .get_noti').removeClass('noties_gotten');
              console.log("Прекратилось получение уведомлений от автора этой публикации");
            }
            if (data.result == 1) {
              $('.pub_one.lifehack a#'+idAccount+' .get_noti').addClass('noties_gotten');
              console.log("Началось получение уведомлений от автора этой публикации");
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}


function openNewComplaintForm() {
  // $opened_pub_additional_functions_id
  $(' .new_complaint').addClass('show');
  if ($('.share_the_pub').hasClass('show')) {
    $('.share_the_pub').removeClass('show')
  }
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

function shareThePub() {
  server_url = 'http://127.0.0.1:8000';
  pub_url = server_url + $('.lifehack#' + $opened_pub_additional_functions_id + ' .pub_url').html();
  // $opened_pub_additional_functions_id
  $('.new_complaint, .statistics, .delete_the_pub').removeClass('show');
  $('.share_the_pub').addClass('show');
  $('.share_the_pub a').html(pub_url).attr('href', pub_url);
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

function showThePubStatistic() {
  $('.statistics h1').html('Статистика по публикации «' + $('.lifehack#'+ $opened_pub_additional_functions_id +' .div_pub_text .pub_text').html() +'»:');
  $('.statistics .seen_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .seen_count').html());
  $('.statistics .saved_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .saved_count').html());
  $('.statistics .average_age_watchers').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .average_age_watchers').html());
  $('.statistics .average_age_savers').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .average_age_savers').html());
  $('.statistics .shared_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .shared_count').html());
  $('.statistics .reported_count').html($('.lifehack#'+ $opened_pub_additional_functions_id +' .statistics .reported_count').html());
  $('.new_complaint, .share_the_pub, .delete_the_pub').removeClass('show');
  $('.statistics').addClass('show');
}

function deleteThePub() {
  // $opened_pub_additional_functions_id;
  $('.delete_the_pub h1').html('Вы точно хотите удалить публикацию «'+ $('.lifehack#'+ $opened_pub_additional_functions_id +' .div_pub_text .pub_text').html() +'»?');
  $('.delete_the_pub a#delete').attr('href', $('.lifehack#'+ $opened_pub_additional_functions_id +' .delete_url').html());
  $('.new_complaint, .share_the_pub, .statistics').removeClass('show');
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
                  url: "/pub/set_seen/" + pub.id + "/",

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

  $('.pub_additional_functions_bg .selected_tags').html('');
  if ($('.lifehack#'+ idPub +' .selected_tag').length > 0 ) {
    $('.pub_additional_functions_bg .opened_filter_form').css('display', 'block');
    $('.lifehack#'+ idPub +' .selected_tag').each(function () {
      $('.pub_additional_functions_bg .selected_tags').html(
        $('.pub_additional_functions_bg .selected_tags').html() + ' <input type="hidden" name="'+ this.name +'" value="'+ this.value +'" class="selected_tag">'
      );
    })
  } else {
    $('.pub_additional_functions_bg .opened_filter_form').css('display', 'none');
  }

  if ($('.lifehack#'+ idPub +' .info_for_author_or_admin').length > 0) {
    $('.pub_additional_functions .for_author_or_admin.edit').attr('href', $('.lifehack#'+ idPub +' .edit_url').html());
    $('.pub_additional_functions .for_author_or_admin').addClass('show');
  }

  $('.pub_one.lifehack#'+ idPub +' .pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.pub_additional_functions').offset($('.pub_one.lifehack#'+ idPub +' .pub_show_full').offset());
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}

function close_additional_functions() {
  if ($is_opened_pub_additional_functions == 1) {
    $idPub = $opened_pub_additional_functions_id;
    $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
    $is_opened_pub_additional_functions = $opened_pub_additional_functions_id = 0;
    $('.pub_additional_functions_bg, .new_complaint, .share_the_pub, .statistics, .delete_the_pub, .for_author_or_admin').removeClass('show');
    console.log("Закрылись дополнительные действия с публикацией с ID "+ $idPub);
  }
}


$(document).ready(function() {
  checkScrollForVideo();
  startSecundomer();
});


$(document).on('click', function(e) {
  if ($(e.target).hasClass('pub_additional_functions_bg')) {
    console.log("pub_additional_functions_bg closed");
    close_additional_functions();
  }
});


$(window).scroll(function () {
  checkScrollForVideo();
  close_additional_functions();
  startSecundomer();
});
