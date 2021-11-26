$(document).ready(function() {
  $filters_on = 0;
  $selected_spheres = 0;
  $selected_styles = 0;
  $selected_rooms = 0;

  $(".triangle_to_open_and_hide.open_hide_design_styles").on('click', function() {
    $('.styles_labels_open').toggleClass('hidden');
    $('.open_hide_design_styles').toggleClass('styles_labels_hidden');
  });

  $(".triangle_to_open_and_hide.open_hide_spheres").on('click', function() {
    $('.spheres_labels_open').toggleClass('hidden');
    $('.open_hide_spheres').toggleClass('spheres_labels_hidden');
  });

  $(".triangle_to_open_and_hide.open_hide_checked_rooms").on('click', function() {
    $('.checked_rooms_open').toggleClass('hidden');
    $('.open_hide_checked_rooms').toggleClass('checked_rooms_open_hidden');
  });

  $(".spheres_labels_open label").on('click', function() {
    console.log("label sphere clicked");
    if (this.classList.contains('any_one')) {
      document.getElementById('checked_spheres_count').innerHTML="Любого";
      $('input[name="sphere_one"]').prop('checked', false);
      $selected_spheres = 0;
    } else {
      $selected_spheres = $(':input[name="sphere_one"]:checked').length;
      document.getElementById('checked_spheres_count').innerHTML= $selected_spheres + " выбрано";
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
      document.getElementById('checked_rooms_count').innerHTML="В любом";
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
    $selected_spheres = 0;
    $selected_styles = 0;
    $selected_rooms = 0;
    document.getElementById('fltr_cost_min').value = '';
    document.getElementById('fltr_cost_max').value = '';
    $(':input[name="sphere_one"]:checked').prop('checked', false);
    $(':input[name="style_design"]:checked').prop('checked', false);
    $(':input[name="checked_room"]:checked').prop('checked', false);
    document.getElementById('checked_spheres_count').innerHTML="Любого";
    document.getElementById('checked_styles_count').innerHTML="Любой";
    document.getElementById('checked_rooms_count').innerHTML="В любом";
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

    if ($selected_spheres >= 1) {
      if ($selected_spheres == 1) {
        document.getElementById('fltr_sphere_p').innerHTML = "Ремонтировать: " + $(':input[name="sphere_one"]:checked')[0].value;
      }
      if ($selected_spheres > 1) {
        document.getElementById('fltr_sphere_p').innerHTML = $(':input[name="sphere_one"]:checked').length + " сфер ремонта";
      }
      $('#fltr_sphere').addClass('show');
      $filters_on += 1;
      console.log("from $selected_spheres +1");
    }

    if ($selected_styles >= 1) {
      if ($selected_styles == 1) {
        document.getElementById('fltr_style_p').innerHTML = "Инструмент " + $(':input[name="style_design"]:checked')[0].value;
      }
      if ($selected_styles > 1) {
        document.getElementById('fltr_style_p').innerHTML = "С импользованием " + $(':input[name="style_design"]:checked').length + " инструментов";
      }
      $('#fltr_style').addClass('show');
      $filters_on += 1;
      console.log("from $selected_styles +1");
    }

    if ($selected_rooms >= 1) {
      if ($selected_rooms == 1) {
        document.getElementById('fltr_room_p').innerHTML = "Работа в помещении " + $(':input[name="checked_room"]:checked')[0].value;
      }
      if ($selected_rooms > 1) {
        document.getElementById('fltr_room_p').innerHTML = "Работа в " + $(':input[name="checked_room"]:checked').length + " помещениях";
      }
      $('#fltr_room').addClass('show');
      $filters_on += 1;
      console.log("from $selected_rooms +1");
    }

    if (document.getElementById('fltr_cost_min').value == ''  && document.getElementById('fltr_cost_max').value == '') {
      $('#fltr_cost').removeClass('show');
    }
    if ($selected_styles == 0) {
      $('#fltr_style').removeClass('show');
    }
    if ($selected_rooms == 0) {
      $('#fltr_room').removeClass('show');
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
  $('.to_close_filter.fltr_sphere').on('click', function() {
    $selected_spheres = 0;
    $(':input[name="sphere_one"]:checked').prop('checked', false);
    document.getElementById('checked_styles_count').innerHTML="Любого";
    $('#fltr_sphere').removeClass('show');
    console.log("#fltr_sphere closed");
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
    document.getElementById('checked_rooms_count').innerHTML="В любом";
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
