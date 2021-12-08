function toggleSavePub_D(idPub) {
  $.ajax({
        url: "/pub/makesaved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
                $('.pub_one.design#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                $('.pub_one.design#'+idPub+' .user_just_saved_it input').val('В «Избранное»');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one.design#'+idPub+' .user_just_saved_it').addClass('pub_saved');
              $('.pub_one.design#'+idPub+' .user_just_saved_it input').val('Сохранено');
              console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

$(document).ready(function() {
  $filters_on = 0;
  $selected_colors = 0;
  $color1 = "none";
  $color2 = "none";
  $color3 = "none";
  $selected_styles = 0;
  $selected_rooms = 0;

  $(".triangle_to_open_and_hide.open_hide_colors").on('click', function() {
    $('.color_panel').toggleClass('hidden');
    $('.open_hide_colors').toggleClass('color_panel_hidden');
  });

  $(".triangle_to_open_and_hide.open_hide_design_styles").on('click', function() {
    $('.styles_labels_open').toggleClass('hidden');
    $('.open_hide_design_styles').toggleClass('styles_labels_hidden');
  });

  $(".triangle_to_open_and_hide.open_hide_checked_rooms").on('click', function() {
    $('.checked_rooms_open').toggleClass('hidden');
    $('.open_hide_checked_rooms').toggleClass('checked_rooms_open_hidden');
  });

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

  $(".styles_labels_open label").on('click', function() {
    console.log("label clicked");
    if (this.classList.contains('any_one')) {
      document.getElementById('checked_styles_count').innerHTML="Любой";
      $('input[name="style_design"]').prop('checked', false);
      $selected_styles = 0;
    } else {
      $selected_styles = $(':input[name="style_design"]:checked').length;
      document.getElementById('checked_styles_count').innerHTML= $selected_styles + " выбрано";
    }
  });

  $(".checked_rooms label").on('click', function() {
    console.log("label clicked");
    if (this.classList.contains('any_one')) {
      document.getElementById('checked_rooms_count').innerHTML="Любая";
      $('input[name="checked_room"]').prop('checked', false);
      $selected_rooms = 0;
    } else {
      $selected_rooms = $(':input[name="checked_room"]:checked').length;
      document.getElementById('checked_rooms_count').innerHTML= $selected_rooms + " выбрано";
    }
  });

  $(".clear_filter").on('click', function() {
    console.log("clear_filter inp clicked");
    $filters_on = 0;
    $selected_colors = 0;
    $color1 = "none";
    $color2 = "none";
    $color3 = "none";
    $selected_styles = 0;
    $selected_rooms = 0;
    document.getElementById('fltr_cost_min').value = '';
    document.getElementById('fltr_cost_max').value = '';
    document.getElementById('color_1_inp').value = '';
    document.getElementById('color_2_inp').value = '';
    document.getElementById('color_3_inp').value = '';
    $('.cp__color.active').removeClass('active');
    $('.checked_colors_count').removeClass('color_was_checked');
    $('.checked_colors_div').removeClass('checked_color');
    $(':input[name="style_design"]:checked').prop('checked', false);
    $(':input[name="checked_room"]:checked').prop('checked', false);
    document.getElementById('checked_colors_count').innerHTML="Любые";
    document.getElementById('checked_styles_count').innerHTML="Любой";
    document.getElementById('checked_rooms_count').innerHTML="Любая";
  });

  $(document).on('click', function() {
    $filters_on = 0;
    if (document.getElementById('fltr_cost_min').value != ''  || document.getElementById('fltr_cost_max').value != '') {
      document.getElementById('fltr_cost_p').innerHTML = "Бюджет ";
      if (document.getElementById('fltr_cost_min').value != '') {
        document.getElementById('fltr_cost_p').innerHTML += "от " + document.getElementById('fltr_cost_min').value + "₽";
      }
      if (document.getElementById('fltr_cost_min').value != '' && document.getElementById('fltr_cost_max').value != '') {
        document.getElementById('fltr_cost_p').innerHTML += " ";
      }
      if (document.getElementById('fltr_cost_max').value != '') {
        document.getElementById('fltr_cost_p').innerHTML += "до " + document.getElementById('fltr_cost_max').value + "₽";
      }
      if ((document.getElementById('fltr_cost_min').value != '' && document.getElementById('fltr_cost_max').value != '') &&
          (document.getElementById('fltr_cost_max').value < document.getElementById('fltr_cost_min').value)) {
        a = document.getElementById('fltr_cost_min').value;
        document.getElementById('fltr_cost_min').value = document.getElementById('fltr_cost_max').value;
        document.getElementById('fltr_cost_max').value = a;
        document.getElementById('fltr_cost_p').innerHTML = "Бюджет от " + document.getElementById('fltr_cost_min').value + "₽";
        document.getElementById('fltr_cost_p').innerHTML += " до " + document.getElementById('fltr_cost_max').value + "₽";
      }
      $('#fltr_cost').addClass('show');
      $filters_on += 1;
      console.log("from input +1");
    }

    if ($selected_colors >= 1) {
      $('#fltr_color').addClass('show');
      $filters_on += 1;
      console.log("from $selected_colors +1");
    }

    if ($selected_styles >= 1) {
      if ($selected_styles == 1) {
        document.getElementById('fltr_style_p').innerHTML = "Стиль " + $(':input[name="style_design"]:checked')[0].value;
      }
      if ($selected_styles > 1) {
        document.getElementById('fltr_style_p').innerHTML = $(':input[name="style_design"]:checked').length + " стилей";
      }
      $('#fltr_style').addClass('show');
      $filters_on += 1;
      console.log("from $selected_styles +1");
    }

    if ($selected_rooms >= 1) {
      if ($selected_rooms == 1) {
        document.getElementById('fltr_room_p').innerHTML = "Комната " + $(':input[name="checked_room"]:checked')[0].value;
      }
      if ($selected_rooms > 1) {
        document.getElementById('fltr_room_p').innerHTML = $(':input[name="checked_room"]:checked').length + " комнат";
      }
      $('#fltr_room').addClass('show');
      $filters_on += 1;
      console.log("from $selected_rooms +1");
    }

    if (document.getElementById('fltr_cost_min').value == ''  && document.getElementById('fltr_cost_max').value == '') {
      $('#fltr_cost').removeClass('show');
    }
    if ($selected_colors == 0) {
      $('#fltr_color').removeClass('show');
    }
    if ($selected_styles == 0) {
      $('#fltr_style').removeClass('show');
    }
    if ($selected_rooms == 0) {
      $('#fltr_room').removeClass('show');
    }

    if ($filters_on >= 1) {
      console.log("$filters_on >= 1");

      $(".filters_on").addClass('show');
      $(".filters_off").addClass('hidden');
      $(".filter_tags_count").addClass('show');
      $(".filter_btn").addClass('tags_count_showed');
      $(".filter").addClass('tags_count_showed');
      $(".filter_to_filter").addClass('turned_on');
      $(".show_pubs_container").addClass('turned_on');
      document.getElementById('tags_count').innerHTML = $filters_on;
    } else {
      console.log("$filters_on !!!>= 1");

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
  $('.to_close_filter.fltr_style').on('click', function() {
    $selected_styles = 0;
    $(':input[name="style_design"]:checked').prop('checked', false);
    document.getElementById('checked_styles_count').innerHTML="Любой";
    $('#fltr_style').removeClass('show');
    console.log("#fltr_style closed");
  });
  $('.to_close_filter.fltr_room').on('click', function() {
    $selected_rooms = 0;
    $(':input[name="checked_room"]:checked').prop('checked', false);
    document.getElementById('checked_rooms_count').innerHTML="Любая";
    $('#fltr_room').removeClass('show');
    console.log("#fltr_room closed");
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
