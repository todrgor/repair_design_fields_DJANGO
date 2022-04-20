function ShowHideSelectedTags() {
  if ($('.opened_filter :input[type="checkbox"]:checked').length > 0 || $('#fltr_cost_min')[0].value != ''  || $('#fltr_cost_max')[0].value != '') {
    console.log('win');
    $(".filters_on, .filter_tags_count").addClass('show');
    $(".filters_off").addClass('hidden');
    $(".filter_btn, .filter").addClass('tags_count_showed');
    $(".filter_to_filter, .show_pubs_container").addClass('turned_on');
    // document.getElementById('tags_count').innerHTML = $filters_on;
  } else {
    console.log('huy tebe');
    $(".filters_on, .filter_tags_count").removeClass('show');
    $(".filters_off").removeClass('hidden');
    $(".filter_btn, .filter").removeClass('tags_count_showed');
    $(".filter_to_filter, .show_pubs_container").removeClass('turned_on');
    // document.getElementById('tags_count').innerHTML = $filters_on;
  }
}

$(document).ready(function() {
  ShowHideSelectedTags();

  $(".opened_filter :input[type='checkbox'], .opened_filter :input[type='number']").on('change', function () {
    ShowHideSelectedTags();
  });

  $("#fltr_cost_min, #fltr_cost_max").on('change', function () {
    if ($('#fltr_cost_min')[0].value != ''  || $('#fltr_cost_max')[0].value != '') {
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
          ($('#fltr_cost_max')[0].value < $('#fltr_cost_min')[0].value)) {
        a = $('#fltr_cost_min')[0].value;
        $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value;
        $('#fltr_cost_max')[0].value = a;
        $('#fltr_cost_p')[0].innerHTML = "Бюджет от " + $('#fltr_cost_min')[0].value + "₽";
        $('#fltr_cost_p')[0].innerHTML += " до " + $('#fltr_cost_max')[0].value + "₽";
      }
      $('#fltr_cost').addClass('show');
      console.log("from cost input +1");
    }
  });

  $(".one_tag ").on('click', function() {
    // console.log('$(this).checked =', this.checked);
    category_id = $(this).parents(".labels").first().attr('id');
    category_name = $('.filter_mini_div.category#' + category_id + ' .category_name').html();
    selected_tags_in_category = $(this).parents(".labels").first().find(':input:checked');
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
  });

  $('.to_close_filter.fltr_cost').on('click', function() {
    $('#fltr_cost').removeClass('show');
    $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value = '';
    ShowHideSelectedTags();
    console.log("#fltr_cost closed");
  });

  $('.to_close_filter, :input[name="clear_category"]').on('click', function() {
    category_id = this.id;
    $('#fltr_' + category_id).removeClass('show');
    $('#'+ category_id +'.labels :input').prop('checked', false);
    ShowHideSelectedTags();
    $('#'+ category_id +'.category .count_checked').html("Любое");
    console.log("id of closed just category:", this.id);
  });

  $(".clear_filter").on('click', function() {
    $(".opened_filter :input[type='checkbox']").prop('checked', false);
    $('#fltr_cost_min')[0].value = $('#fltr_cost_max')[0].value = '';
    ShowHideSelectedTags();
    $('.filter_one').removeClass('show');
    $('.category .count_checked').html("Любое");
    console.log("all inputs cleared");
  });

  $(".triangle_to_open_and_hide").on('click', function() {
    $(this).parents(".filter_mini_div").first().find('.labels').first().toggleClass('hidden');
    $(this).parents(".filter_mini_div").first().find('.triangle_to_open_and_hide').first().toggleClass('labels_hidden');
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

});
