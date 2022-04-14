function toggleShow(idPubContainer) {
  $(".pubs_container_one_type#"+idPubContainer).toggleClass('show');
  $(".result_type_container#"+idPubContainer+" .triangle_to_open_and_hide").toggleClass('dontShow');
}

function really_delete_pub(pub_id) {
  $('.cancel_or_delete a').attr('href', '/pub/delete/'+pub_id);
  $('.pub_additional_functions_bg').addClass('show');
}

function really_delete_account(user_id) {
  $('.cancel_or_delete a').attr('href', '/account/delete/'+user_id);
  $('.pub_additional_functions_bg').addClass('show');
}

$('.pub_additional_functions_bg').on('click', function(e) {
  if (!($(e.target).hasClass("dont_close_on_click"))) {
    $('.pub_additional_functions_bg').removeClass('show');
  }
});
