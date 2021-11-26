function toggleShow(idPubContainer) {
  $(".pubs_container_one_type#"+idPubContainer).toggleClass('show');
  $(".result_type_container#"+idPubContainer+" .triangle_to_open_and_hide").toggleClass('dontShow');
}
