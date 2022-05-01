function YouHaveToLogin(action) {
  alert('Вам нужно авторизоваться перед тем, как ' + action + '.')
}

function toggleSavePub_LH(idPub) {
  $.ajax({
        url: "/pub/makesaved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
                $('.pub_one.lifehack#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one.lifehack#'+idPub+' .user_just_saved_it').addClass('pub_saved');
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
            alert("Какая-то ошибка с жалобой...");
          }
      });

    $is_opened_pub_additional_functions = 0;
    $opened_pub_additional_functions_id = 0;
  } else {
    alert('Жалоба не отправлена, для начала напишите её!');
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

function checkScrollForVideo() {
  var fraction = 0.9; // Play video when 90% of the player is visible.

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

$is_opened_pub_additional_functions = 0;
$opened_pub_additional_functions_id = 0;

function togglePubAdditionalFunctions(idPub) {
  $('.pub_one.lifehack#'+idPub+' .pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').toggleClass('show');
  $('.pub_additional_functions').offset($('.pub_one.lifehack#'+idPub+' .pub_show_full').offset());
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}

function close_additional_functions() {
  if ($is_opened_pub_additional_functions == 1) {
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




function TagsWereSelectedBeforeLoadingThePage() {
  $('.category').each(function () {
    UpdateOneTag($('.category#' + this.id + ' .one_tag')[0]);
  })
  UpdateSelectedTagsView();
  UpdateCostView();
  UpdateSavePercentView();
  SelectedTagsCount();
}

function SelectedTagsCount() {
  var count = $('.filter_one.show').length;
  $('#tags_count').html(count);
  return count
}

function UpdateSelectedTagsView() {
  if ($('.opened_filter :input[type="checkbox"]:checked').length > 0 || $('#fltr_cost_min')[0].value != ''  || $('#fltr_cost_max')[0].value != '' || $('#save_percent_min')[0].value != '' || $('#save_percent_max')[0].value != '') {
    // console.log('win');
    $(".filters_on, .filter_tags_count").addClass('show');
    $(".filters_off").addClass('hidden');
    $(".filter_btn, .filter").addClass('tags_count_showed');
    $(".filter_to_filter, .show_pubs_container").addClass('turned_on');

    $.ajax({ // create an AJAX call...
        data: $('.opened_filter_form').serialize(), // get the form data
        type: 'GET', // GET or POST
        url: $('.get_filtered_pubs_count').html(), // the file to call
        success: function(response) { // on success..
          pubs_count = response.pubs_count;
          console.log("success..");
          console.log(pubs_count, "pubs founded");
          $('.opened_filter_second_title').html(pubs_count+' подобрано');
          $('.show_pubs_container input[name="to_filter"]').val('Показать '+pubs_count+' подходящих');
        },
        error: function (error) {
          $('.opened_filter_second_title').html('Случилась какая-то ошибка... Возможно, сейчас всё восстановится.');
          $('.show_pubs_container input[name="to_filter"]').val('У сервера какая-то ошибка');
        },
    });
  } else {
    // console.log('*** tebe');
    $(".filters_on, .filter_tags_count").removeClass('show');
    $(".filters_off").removeClass('hidden');
    $(".filter_btn, .filter").removeClass('tags_count_showed');
    $(".filter_to_filter, .show_pubs_container").removeClass('turned_on');
    $('.opened_filter_second_title').html('');
    $('.show_pubs_container input[name="to_filter"]').val('Показать все публикации');
  }
  SelectedTagsCount();
}

function UpdateCostView() {
  console.log("called UpdateCostView();");

  if ($('#fltr_cost_min')[0].value != ''  || $('#fltr_cost_max')[0].value != '') {
    if ($('#fltr_cost_min')[0].value < 0) {
      $('#fltr_cost_min')[0].val(0);
    }
    if ($('#fltr_cost_max')[0].value < 0) {
      $('#fltr_cost_max')[0].val(0);
    }
    $('#fltr_cost_p')[0].innerHTML = "Бюджет ";
    if ($('#fltr_cost_min')[0].value != '') {
      $('#fltr_cost_p')[0].innerHTML += "от " + $('#fltr_cost_min')[0].value + "₽";
    }
    if ($('#fltr_cost_min')[0].value != '' && $('#fltr_cost_max')[0].value != '') {
      $('#fltr_cost_p')[0].innerHTML += " ";
    }
    if ($('#fltr_cost_max')[0].value != '') {
      $('#fltr_cost_p')[0].innerHTML += "до " + $('#fltr_cost_max')[0].value + "₽";
    }
    if (($('#fltr_cost_min')[0].value != '' && $('#fltr_cost_max')[0].value != '') &&
        (parseFloat($('#fltr_cost_max')[0].value) < parseFloat($('#fltr_cost_min')[0].value))) {
      a = $('#fltr_cost_min')[0].value;
      $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value;
      $('#fltr_cost_max')[0].value = a;
      $('#fltr_cost_p')[0].innerHTML = "Бюджет от " + $('#fltr_cost_min')[0].value + "₽";
      $('#fltr_cost_p')[0].innerHTML += " до " + $('#fltr_cost_max')[0].value + "₽";
    }
    $('#fltr_cost').addClass('show');
    SelectedTagsCount();
    // console.log("from cost input +1");
  }
}

function UpdateSavePercentView() {
  console.log("called UpdateSavePercentView();");

  if ($('#save_percent_min')[0].value != ''  || $('#save_percent_max')[0].value != '') {
    if ($('#save_percent_min')[0].value < 0) {
      $('#save_percent_min')[0].value = 0;
    }
    if ($('#save_percent_max')[0].value < 0) {
      $('#save_percent_max')[0].value = 0;
    }
    if ($('#save_percent_min')[0].value > 100) {
      $('#save_percent_min')[0].value = 100;
    }
    if ($('#save_percent_max')[0].value > 100) {
      $('#save_percent_max')[0].value = 100;
    }

    $('#fltr_save_percent_p')[0].innerHTML = "";
    if ($('#save_percent_min')[0].value != '') {
      $('#fltr_save_percent_p')[0].innerHTML += "От " + $('#save_percent_min')[0].value + "%";
    }
    if ($('#save_percent_min')[0].value != '' && $('#save_percent_max')[0].value != '') {
      $('#fltr_save_percent_p')[0].innerHTML += " ";
    }
    if ($('#save_percent_max')[0].value != '') {
      if ($('#save_percent_min')[0].value != '') {
        $('#fltr_save_percent_p')[0].innerHTML += "до " + $('#save_percent_max')[0].value + "%";
      } else {
        $('#fltr_save_percent_p')[0].innerHTML += "До " + $('#save_percent_max')[0].value + "%";
      }
    }
    if (($('#save_percent_min')[0].value != '' && $('#save_percent_max')[0].value != '') &&
        (parseFloat($('#save_percent_max')[0].value) < parseFloat($('#save_percent_min')[0].value))) {
      console.log('save_percent_min -', $('#save_percent_min')[0].value);
      console.log('save_percent_max -', $('#save_percent_max')[0].value);

      a = $('#save_percent_min')[0].value;
      $('#save_percent_min')[0].value = $('#save_percent_max')[0].value;
      $('#save_percent_max')[0].value = a;
      $('#fltr_save_percent_p')[0].innerHTML = "От " + $('#save_percent_min')[0].value + "%";
      $('#fltr_save_percent_p')[0].innerHTML += " до " + $('#save_percent_max')[0].value + "%";
    }
    $('#fltr_save_percent_p')[0].innerHTML += " сохранений";
    $('#fltr_save_percent').addClass('show');
    SelectedTagsCount();
    // console.log("from save_percent input +1");
  }
}

function UpdateOneTag(tag) {
  // console.log('UpdateOneTag(tag) --');
  // console.log($(tag));
  // console.log(tag);

  category_id = $(tag).parents(".labels").first().attr('id');
  category_name = $('.filter_mini_div.category#' + category_id + ' .category_name').html();
  selected_tags_in_category = $(tag).parents(".labels").first().find(':input:checked');
  console.log('category id -', category_id);
  console.log('category name -', category_name);
  console.log('selected count -', selected_tags_in_category.length);

  if (selected_tags_in_category.length == 0) {
    $('#'+ category_id +'.category .count_checked').html("Любое");
    $('#fltr_'+ category_id).removeClass('show');

  } else {
    $('#fltr_'+ category_id).addClass('show');
    if (selected_tags_in_category.length == 1) {
      $('#'+ category_id +'.category .count_checked').html(selected_tags_in_category[0].value);
      $('#fltr_'+category_id+'_p').html(category_name +' '+ selected_tags_in_category[0].value);
    }
    if (selected_tags_in_category.length > 1) {
      $('#'+ category_id +'.category .count_checked').html(selected_tags_in_category.length + " выбрано");
      $('#fltr_'+category_id+'_p').html(category_name +' '+ selected_tags_in_category.length + " выбрано");
    }
  }
}

$(document).ready(function() {
  checkScrollForVideo();
  TagsWereSelectedBeforeLoadingThePage();

  $(document).on('click', function(e) {
    if ($(e.target).hasClass('pub_additional_functions_bg')) {
      close_additional_functions();
    }
  });

  $(".opened_filter :input[type='checkbox'], .opened_filter :input[type='number']").on('change', function() {
    UpdateSelectedTagsView();
  });

  $("#fltr_cost_min, #fltr_cost_max").on('change', function() {
    UpdateCostView();
  });

  $("#save_percent_min, #save_percent_max").on('change', function() {
    UpdateSavePercentView();
  });

  $(".one_tag ").on('click change', function (tag) {
    UpdateOneTag($(tag.currentTarget));
  });

  $('.to_close_filter.fltr_cost').on('click', function() {
    $('#fltr_cost').removeClass('show');
    $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value = '';
    UpdateSelectedTagsView();
    console.log("#fltr_cost closed");
  });

  $('.to_close_filter.fltr_save_percent').on('click', function() {
    $('#fltr_save_percent').removeClass('show');
    $('#save_percent_min')[0].value = $('#save_percent_max')[0].value = '';
    UpdateSelectedTagsView();
    console.log("#fltr_save_percent closed");
  });

  $('.to_close_filter.fltr_some_category, :input[name="clear_category"]').on('click', function() {
    category_id = this.id;
    $('#fltr_' + category_id).removeClass('show');
    $('#'+ category_id +'.labels :input').prop('checked', false);
    UpdateSelectedTagsView();
    $('#'+ category_id +'.category .count_checked').html("Любое");
    console.log("id of closed just category:", this.id);
  });

  $(".clear_filter").on('click', function() {
    $(".opened_filter :input[type='checkbox']").prop('checked', false);
    $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value = $('#save_percent_min')[0].value = $('#save_percent_max')[0].value = '';
    UpdateSelectedTagsView();
    $('.filter_one').removeClass('show');
    $('.category .count_checked').html("Любое");
    console.log("all inputs cleared");
  });

  $(".triangle_to_open_and_hide").on('click', function() {
    $(this).parents(".filter_mini_div").first().find('.labels').first().toggleClass('hidden');
    $(this).parents(".filter_mini_div").first().find('.triangle_to_open_and_hide').first().toggleClass('labels_hidden');
  });

});

$(window).scroll(function () {
  checkScrollForVideo();
  close_additional_functions();

  if ($(window).scrollTop() > 30) {
    $(".filter").addClass('user_scrolled');
    console.log("(.filter).addClass('user_scrolled'");
  } else {
    $(".filter").removeClass('user_scrolled');
    console.log("(.filter).removeClass('user_scrolled'");
  }
});
