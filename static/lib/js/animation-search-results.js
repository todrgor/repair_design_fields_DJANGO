
function toggleSavePub_D(idPub) {
  $.ajax({
        url: "/pub/make_saved/" + idPub + "/",

        success: function (data) {
            if (data.result == 0) {
                $('.pub_one.design#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                $('.pub_one.design#'+idPub+' .user_just_saved_it input').val('В «Избранное»');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one.design#'+idPub+' .user_just_saved_it').addClass('pub_saved');
              $('.pub_one.design#'+idPub+' .user_just_saved_it input').val('Сохранено');
              console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          console.log("ошибка какая-то");
        }
    });
}

function toggleShow(idPubContainer) {
  $(".pubs_container_one_type#"+idPubContainer).toggleClass('show');
  $(".result_type_container#"+idPubContainer+" .triangle_to_open_and_hide").toggleClass('dontShow');
}
