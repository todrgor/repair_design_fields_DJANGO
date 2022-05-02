function toggleRemovePubFromSaved_D(idPub) {
  $.ajax({
        url: "/pub/makesaved/" + idPub + "/",

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
        url: "/pub/makesaved/" + idPub + "/",

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
        url: "/pub/makesaved/" + idPub + "/",

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

$is_opened_pub_additional_functions = 0;
$opened_pub_additional_functions_id = 0;
function togglePubAdditionalFunctions(idPub) {
  $('.pub_one.lifehack#'+idPub+' .pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.pub_additional_functions').offset({top:( $('.pub_one.lifehack#'+idPub+' .pub_show_full').offset().top - 10  )});
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}
function openNewComplaintForm() {
  // $opened_pub_additional_functions_id
  $(' .new_complaint').addClass('show');
  if ($('.share_the_pub').hasClass('show')) {
    $('.share_the_pub').removeClass('show')
  }
}
function shareThePub() {
  // $opened_pub_additional_functions_id
  $(' .share_the_pub').addClass('show');
  $('.share_the_pub a').html('http://127.0.0.1:8000/pub/one/'+ $opened_pub_additional_functions_id +'/')
  $('.share_the_pub a').attr('href', 'http://127.0.0.1:8000/pub/one/'+ $opened_pub_additional_functions_id +'/')
  if ($('.new_complaint').hasClass('show')) {
    $('.new_complaint').removeClass('show')
  }
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
            alert("Какая-то ошибка с жалобой...");
          }
      });

    $is_opened_pub_additional_functions = 0;
    $opened_pub_additional_functions_id = 0;
  } else {
    alert('Жалоба не отправлена, для начала напишите её!');
  }
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



$(document).ready(function() {
  $filters_on = 0;
  $selected_styles = 0;

  $(".triangle_to_open_and_hide.open_hide_design_styles").on('click', function() {
    $('.styles_labels_open').toggleClass('hidden');
    $('.open_hide_design_styles').toggleClass('styles_labels_hidden');
  });

  $(".styles_labels_open label").on('click', function() {
    if (this.classList.contains('any_one')) {
      document.getElementById('checked_styles_count').innerHTML="Любой";
      $('input[name="style_design"]').prop('checked', false);
      $selected_styles = 0;
    } else {
      $selected_styles = $(':input[name="style_design"]:checked').length;
      document.getElementById('checked_styles_count').innerHTML= $selected_styles + " выбрано";
    }
  });

  $(".clear_filter").on('click', function() {
    console.log("clear_filter inp clicked");
    $filters_on = 0;
    $selected_styles = 0;
    document.getElementById('fltr_cost_min').value = '';
    document.getElementById('fltr_cost_max').value = '';
    $(':input[name="style_design"]:checked').prop('checked', false);
    document.getElementById('checked_styles_count').innerHTML="Любой";
  });

  $(document).on('click', function(e) {
    $filters_on = 0;

    if ($is_opened_pub_additional_functions == 1) {
      if ($(e.target).hasClass('pub_additional_functions_bg')) {
        $idPub = $opened_pub_additional_functions_id;
        $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
        $('.pub_additional_functions_bg').removeClass('show');
        $is_opened_pub_additional_functions = 0;
        $opened_pub_additional_functions_id = 0;
        $('.new_complaint').removeClass('show');
        $('.share_the_pub').removeClass('show');
        console.log("Закрылись дополнительные действия с публикацией с ID "+ $idPub);
      }
    }

    // if (document.getElementById('fltr_cost_min').value != ''  || document.getElementById('fltr_cost_max').value != '') {
    //   document.getElementById('fltr_cost_p').innerHTML = "Публикации ";
    //   if (document.getElementById('fltr_cost_min').value != '') {
    //     document.getElementById('fltr_cost_p').innerHTML += "от " + document.getElementById('fltr_cost_min').value.split("-").reverse().join(".");
    //   }
    //   if (document.getElementById('fltr_cost_min').value != '' && document.getElementById('fltr_cost_max').value != '') {
    //     document.getElementById('fltr_cost_p').innerHTML += " ";
    //   }
    //   if (document.getElementById('fltr_cost_max').value != '') {
    //     document.getElementById('fltr_cost_p').innerHTML += "до " + document.getElementById('fltr_cost_max').value.split("-").reverse().join(".");
    //   }
    //   if ((document.getElementById('fltr_cost_min').value != '' && document.getElementById('fltr_cost_max').value != '') &&
    //       (Date.parse(document.getElementById('fltr_cost_max').value) < Date.parse(document.getElementById('fltr_cost_min').value))) {
    //     a = document.getElementById('fltr_cost_min').value;
    //     document.getElementById('fltr_cost_min').value = document.getElementById('fltr_cost_max').value;
    //     document.getElementById('fltr_cost_max').value = a;
    //     document.getElementById('fltr_cost_p').innerHTML = "Публикации от " + document.getElementById('fltr_cost_min').value.split("-").reverse().join(".");
    //     document.getElementById('fltr_cost_p').innerHTML += " до " + document.getElementById('fltr_cost_max').value.split("-").reverse().join(".");
    //   }
    //   $('#fltr_cost').addClass('show');
    //   $filters_on += 1;
    //   console.log("from input +1");
    // }

    if ($selected_styles >= 1) {
      if ($selected_styles == 1) {
        document.getElementById('fltr_style_p').innerHTML = "Публикации " + $(':input[name="style_design"]:checked')[0].value;
      }
      if ($selected_styles > 1) {
        document.getElementById('fltr_style_p').innerHTML = $(':input[name="style_design"]:checked').length + " вида публикации";
      }
      $('#fltr_style').addClass('show');
      $filters_on += 1;
      console.log("from $selected_styles +1");
    }

    if (document.getElementById('fltr_cost_min').value == ''  && document.getElementById('fltr_cost_max').value == '') {
      $('#fltr_cost').removeClass('show');
    }
    if ($selected_styles == 0) {
      $('#fltr_style').removeClass('show');
    }

    if ($filters_on >= 1) {
      $(".filters_on").addClass('show');
      $(".filters_off").addClass('hidden');
      $(".filter_tags_count").addClass('show');
      $(".filter_btn").addClass('tags_count_showed');
      $(".filter").addClass('tags_count_showed');
      $(".filter_to_filter").addClass('turned_on');
      $(".show_pubs_container").addClass('turned_on');
      document.getElementById('tags_count').innerHTML = $filters_on;
    } else {
      $(".filters_on").removeClass('show');
      $(".filters_off").removeClass('hidden');
      $(".filter_tags_count").removeClass('show');
      $(".filter_btn").removeClass('tags_count_showed');
      $(".filter").removeClass('tags_count_showed');
      $(".filter_to_filter").removeClass('turned_on');
      $(".show_pubs_container").removeClass('turned_on');
      document.getElementById('tags_count').innerHTML = $filters_on;
    }
  });

  $('.to_close_filter.fltr_cost').on('click', function() {
    document.getElementById('fltr_cost_min').value = '';
    document.getElementById('fltr_cost_max').value = '';
    $('#fltr_cost').removeClass('show');
    console.log("#fltr_cost closed");
  });
  $('.to_close_filter.fltr_style').on('click', function() {
    $selected_styles = 0;
    $(':input[name="style_design"]:checked').prop('checked', false);
    document.getElementById('checked_styles_count').innerHTML="Любой";
    $('#fltr_style').removeClass('show');
    console.log("#fltr_style closed");
  });

  $(window).scroll(function () {
    checkScrollForVideo();

    if ($is_opened_pub_additional_functions == 1) {
      $idPub = $opened_pub_additional_functions_id;
      $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
      $('.pub_additional_functions_bg').removeClass('show');
      $is_opened_pub_additional_functions = 0;
      $opened_pub_additional_functions_id = 0;
      $('.new_complaint').removeClass('show');
      $('.share_the_pub').removeClass('show');
      console.log("Дополнительные действия с публикацией закрылись :3");
    }

    if ($(window).scrollTop() > 30) {
      $(".filter").addClass('user_scrolled');
      console.log("(.filter).addClass('user_scrolled'");
    } else {
      $(".filter").removeClass('user_scrolled');
      console.log("(.filter).removeClass('user_scrolled'");
    }
  });

});
