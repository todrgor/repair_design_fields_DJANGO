
function toggleShowExpertInfo() {
  if ($('select[name="role"]').val()=='2' or $('select[name="role"]').val()=='2') {
    $('.expert_inputs').addClass('show');
  } else {
    $('.expert_inputs').removeClass('show');
  }
}

$('select[name="role"]').change(function () {
  toggleShowExpertInfo();
});

$(document).ready(function() {
  toggleShowExpertInfo();
});
