$('select[name="role"]').change(function () {
  if ($('select[name="role"]').val()=='2') {
    $('.expert_inputs').addClass('show');
  } else {
    $('.expert_inputs').removeClass('show');
  }
});
