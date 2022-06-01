
function toggleShowExpertInfo() {
  if ($('select[name="role"]').val()=='2' ||
      $('select[name="role"]').val()=='4' ||
      $('.user_role_id').html()=='2'      ||
      $('.user_role_id').html()=='4' ) {
    $('.expert_inputs').addClass('show');
  } else {
    $('.expert_inputs').removeClass('show');
  }
}

$('select[name="role"]').change(function () {
  $('.user_role_id').html('');
  toggleShowExpertInfo();
});

$(document).ready(function() {
  toggleShowExpertInfo();
});
