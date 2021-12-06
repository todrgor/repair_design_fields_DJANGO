// function check_count_of_uploaded_img() {
//   if ($("#pub_photos")[0].files.length > 20) {
//     alert('Загружено больше 20 фотографий. Будут использоваться только первые 20 по порядку.');
//   }
// }
//
// $('#pub_photos').change(function () {
//   if ($("#pub_photos")[0].files.length > 20) {
//     for (var i = 21; i < $("#pub_photos")[0].files.length; i++) {
//       delete $("#pub_photos")[0].files[i];
//       // $("#pub_photos")[0].files.remove(i);
//     }
//     alert('Загружено больше 20 фотографий. Будут использоваться только первые 20 по порядку.');
//   } else {
//     console.log($("#pub_photos")[0].files.length + ' фотографий успешно загружены.');
//   }
// });

$('input[name="pub_role"], .pub_roles select').change(function () {
  if ($('#pub_role:checked').val() == 'repair' || $('.pub_roles select').val() == '11') {
    console.log('pub_role = repair');
    $('#budget.cost').addClass('show');
    $('#repair.checked_spheres').addClass('show');
    $('#repair.checked_styles').addClass('show');
    $('#repair.checked_rooms').addClass('show');
    $('#design.color').removeClass('show');
    $('#design.checked_rooms').removeClass('show');
    $('#design.checked_styles').removeClass('show');
    $('#lifehack.checked_spheres').removeClass('show');
  }

  if ($('#pub_role:checked').val() == 'design' || $('.pub_roles select').val() == '21') {
    console.log('pub_role = design');
    $('#budget.cost').addClass('show');
    $('#repair.checked_spheres').removeClass('show');
    $('#repair.checked_styles').removeClass('show');
    $('#repair.checked_rooms').removeClass('show');
    $('#design.color').addClass('show');
    $('#design.checked_rooms').addClass('show');
    $('#design.checked_styles').addClass('show');
    $('#lifehack.checked_spheres').removeClass('show');
  }

  if ($('#pub_role:checked').val() == 'lifehack' || $('.pub_roles select').val() == '31') {
    console.log('pub_role = lifehack');
    $('#budget.cost').removeClass('show');
    $('#repair.checked_spheres').removeClass('show');
    $('#repair.checked_styles').removeClass('show');
    $('#repair.checked_rooms').removeClass('show');
    $('#design.color').removeClass('show');
    $('#design.checked_rooms').removeClass('show');
    $('#design.checked_styles').removeClass('show');
    $('#lifehack.checked_spheres').addClass('show');
  }

});

$('#id_cost_min, #id_cost_max').change(function () {
  if ($('#id_cost_min').val() > $('#id_cost_max').val() && $('#id_cost_max').val() != 0) {
    min = $('#id_cost_min').val();
    max = $('#id_cost_max').val();
    $('#id_cost_min').val(max);
    $('#id_cost_max').val(min);
  }
});
