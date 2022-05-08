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

$('input[name="pub_type"], .pub_types select').change(function () {
  if ($('#pub_type:checked').val() == 'repair' || $('.pub_types select').val() == '11') {
    console.log('pub_type = repair');
    $('.pub_preview.pub_inp_one h4:first').html('Превью:');
    $('.repair').addClass('show');
    $('.design, .lifehack').removeClass('show');
    $('.pub_description, .pub_photos').removeClass('hidden');
  }

  if ($('#pub_type:checked').val() == 'design' || $('.pub_types select').val() == '21') {
    console.log('pub_type = design');
    $('.pub_preview.pub_inp_one h4:first').html('Превью:');
    $('.repair, .lifehack').removeClass('show');
    $('.design').addClass('show');
    $('.pub_description, .pub_photos').removeClass('hidden');
  }

  if ($('#pub_type:checked').val() == 'lifehack' || $('.pub_types select').val() == '31') {
    console.log('pub_type = lifehack');
    $('.pub_preview.pub_inp_one h4:first').html('Файл:');
    $('.repair, .design').removeClass('show');
    $('.lifehack').addClass('show');
    $('.pub_description, .pub_photos').addClass('hidden');
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

$('#type_of_contacting_support').change(function () {
  if ($('#type_of_contacting_support select').val() == '11') {
    $('#complaint_pub').removeClass('hidden');
    $('#complaint_account').addClass('hidden');
  } else if ($('#type_of_contacting_support select').val() == '12') {
    $('#complaint_pub').addClass('hidden');
    $('#complaint_account').removeClass('hidden');
  } else {
    $('#complaint_pub').addClass('hidden');
    $('#complaint_account').addClass('hidden');
  }
});
