$('input[name="pub_type"], .pub_types select').change(function () {
  if ($('#pub_type:checked').val() == 'repair' || $('.pub_types select').val() == '11') {
    console.log('pub_type = repair');
    $('.pub_preview.pub_inp_one h4:first').html('Превью:');
    $('.repair').addClass('show');
    $('.pub_content').addClass('show');
    $('.design, .lifehack').removeClass('show');
    $('.design input, .lifehack input').prop('checked', false);
    $('.pub_description, .pub_photos').removeClass('hidden');
  }

  if ($('#pub_type:checked').val() == 'design' || $('.pub_types select').val() == '21') {
    console.log('pub_type = design');
    $('.pub_preview.pub_inp_one h4:first').html('Превью:');
    $('.design').addClass('show');
    $('.pub_content').addClass('show');
    $('.repair, .lifehack').removeClass('show');
    $('.repair input, .lifehack input').prop('checked', false);
    $('.pub_description, .pub_photos').removeClass('hidden');
  }

  if ($('#pub_type:checked').val() == 'lifehack' || $('.pub_types select').val() == '31') {
    console.log('pub_type = lifehack');
    $('.pub_preview.pub_inp_one h4:first').html('Файл:');
    $('.repair, .design, .pub_content').removeClass('show');
    $('.lifehack').addClass('show');
    $('.repair input, .design input').prop('checked', false);
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
