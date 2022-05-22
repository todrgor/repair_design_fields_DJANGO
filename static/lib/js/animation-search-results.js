
// start-end toggle saved loading animation is in animation-lifehack.js
function toggleSavePub_D(idPub) {
  console.log("$(this): ", $(this));
  start_loading_animation(idPub);

  $.ajax({
        url: "/pub/" + idPub + "/toggle_saved/",

        success: function (data) {
          end_loading_animation(idPub);

            if (data.result == 0) {
                $('.pub_one#'+idPub+' .user_just_saved_it').removeClass('pub_saved');
                $('.pub_one#'+idPub+' .user_just_saved_it input').val('В «Избранное»');
                console.log("Публикация больше не в сохранённом, ID:" +idPub);
            }
            if (data.result == 1) {
              $('.pub_one#'+idPub+' .user_just_saved_it').addClass('pub_saved');
              $('.pub_one#'+idPub+' .user_just_saved_it input').val('Сохранено');
              console.log("Произошло сохранение публикации, ID:" +idPub);
            }
        },
        error: function (data) {
          end_loading_animation(idPub);
          $('.pub_one#'+idPub+' .user_just_saved_it input').val('Попробуйте ещё раз...');
          console.log("ошибка какая-то");
        }
    });
}

function toggleShow(idPubContainer) {
  $(".pubs_container_one_type#"+idPubContainer).toggleClass('show');
  $(".result_type_container#"+idPubContainer+" .triangle_to_open_and_hide").toggleClass('dontShow');
}
