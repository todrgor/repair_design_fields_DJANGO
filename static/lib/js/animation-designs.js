
function start_loading_animation(idPub) {
  $('.pub_one#'+idPub+' .user_just_saved_it img').attr('src', '/static/sources/SVG/heart_loading.gif');
  // $('.pub_one#'+idPub+' .user_just_saved_it img').css('transform', 'rotate(-25deg)');
  $('.pub_one#'+idPub+' .user_just_saved_it input').val('Загрузка...');
}

function end_loading_animation(idPub) {
  $('.pub_one#'+idPub+' .user_just_saved_it img').attr('src', '/static/sources/SVG/heart.svg');
  // $('.pub_one.design#'+idPub+' .user_just_saved_it img').css('transform', 'rotate(0deg)');
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

//  пока что это ненужно
    $(".cp__color").on('click', function() {
      if (!this.classList.contains('active')) {
        if ($selected_colors == 3 || this.classList.contains('any_3_colors')) {
          $(".cp__color.active").removeClass('active');
          document.getElementById('checked_colors_count').innerHTML="Любые";
          $('.checked_colors_count').removeClass('color_was_checked');
          $('.checked_colors_div').removeClass('checked_color');
          document.getElementById('color_1_inp').value = "";
          document.getElementById('color_2_inp').value = "";
          document.getElementById('color_3_inp').value = "";
          console.log("$color1", document.getElementById('color_1_inp').value);
          console.log("$color2", document.getElementById('color_2_inp').value);
          console.log("$color3", document.getElementById('color_3_inp').value);
          $selected_colors = 0;
          $color1 = "none";
          $color2 = "none";
          $color3 = "none";
          $filters_on -= 1;
        }

        if (!this.classList.contains('any_3_colors')) {
          if ($selected_colors == 0) {
            $color1 = this.id;
            document.getElementById('color_1_inp').value = this.id;
            console.log("$color1", document.getElementById('color_1_inp').value);
            document.getElementById('checked_colors_count').innerHTML="2 любых +";
            $('.checked_color_1').addClass('checked_color');
            $('.checked_color_1').attr('id', this.id);
            $('.checked_colors_count').addClass('color_was_checked');
          }
          if ($selected_colors == 1) {
            $color2 = this.id;
            document.getElementById('color_2_inp').value = this.id;
            console.log("$color2", document.getElementById('color_2_inp').value);
            document.getElementById('checked_colors_count').innerHTML="1 любой +";
            $('.checked_color_2').addClass('checked_color');
            $('.checked_color_2').attr('id', this.id);
            $('.checked_colors_count').addClass('color_was_checked');
          }
          if ($selected_colors == 2) {
            $color2 = this.id;
            document.getElementById('color_3_inp').value = this.id;
            console.log("$color3", document.getElementById('color_3_inp').value);
            document.getElementById('checked_colors_count').innerHTML="";
            $('.checked_color_3').addClass('checked_color');
            $('.checked_color_3').attr('id', this.id);
            $('.checked_colors_count').addClass('color_was_checked');
          }

          $(this).addClass('active');
          $selected_colors += 1;
        }
      }
    });
    $('.to_close_filter.fltr_color').on('click', function() {
      $selected_colors = 0;
      $color1 = "none";
      $color2 = "none";
      $color3 = "none";
      $('.cp__color.active').removeClass('active');
      $('.checked_colors_count').removeClass('color_was_checked');
      $('.checked_colors_div').removeClass('checked_color');
      document.getElementById('color_1_inp').value = '';
      document.getElementById('color_2_inp').value = '';
      document.getElementById('color_3_inp').value = '';
      document.getElementById('checked_colors_count').innerHTML="Любые";
      $('#fltr_color').removeClass('show');
      console.log("#fltr_color closed");
    });


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
  TagsWereSelectedBeforeLoadingThePage();

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
  console.log("window).scroll");
  if ($(window).scrollTop() > 30) {
    $(".filter").addClass('user_scrolled');
    console.log("(.filter).addClass('user_scrolled'");
  } else {
    $(".filter").removeClass('user_scrolled');
    console.log("(.filter).removeClass('user_scrolled'");
  }
});
