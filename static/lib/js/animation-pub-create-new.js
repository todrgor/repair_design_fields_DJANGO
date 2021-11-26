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

$('input[name="pub_role"]').change(function () {
  if ($('#pub_role:checked').val() == 'repair') {
    console.log('pub_role = repair');
    $('#budget.cost').addClass('show');
    $('#repair.checked_spheres').addClass('show');
    $('#repair.checked_styles').addClass('show');
    $('#repair.checked_rooms').addClass('show');
    $('#design.color').removeClass('show');
    $('#design.checked_rooms').removeClass('show');
    $('#design.color').removeClass('show');
    $('#lifehack.checked_styles').removeClass('show');
  }

  if ($('#pub_role:checked').val() == 'design') {
    console.log('pub_role = design');
    $('#budget.cost').addClass('show');
    $('#repair.checked_spheres').removeClass('show');
    $('#repair.checked_styles').removeClass('show');
    $('#repair.checked_rooms').removeClass('show');
    $('#design.color').addClass('show');
    $('#design.checked_rooms').addClass('show');
    $('#design.color').addClass('show');
    $('#lifehack.checked_styles').removeClass('show');
  }

  if ($('#pub_role:checked').val() == 'lifehack') {
    console.log('pub_role = lifehack');
    $('#budget.cost').removeClass('show');
    $('#repair.checked_spheres').removeClass('show');
    $('#repair.checked_styles').removeClass('show');
    $('#repair.checked_rooms').removeClass('show');
    $('#design.color').removeClass('show');
    $('#design.checked_rooms').removeClass('show');
    $('#design.color').removeClass('show');
    $('#lifehack.checked_styles').addClass('show');
  }
});
