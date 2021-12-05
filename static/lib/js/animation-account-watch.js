$('.bio.notNone').offset({top: ( $('.bio.notNone').offset().top) - 20, left:( $('.user_role').offset().left) - 88});
$('.bio.None').offset({left:( $('.user_role').offset().left) - 88});

function toggleSavePub_LH(idPub) {
  $('.pub_one.lifehack#'+idPub+' .user_just_saved_it').toggleClass('pub_saved');
  console.log("Произошло сохранение/нет публикации");
}

function toggleGetNotiFromAuthor(idPub) {
  $('.get_noti').toggleClass('noties_gotten');
  console.log("Произошло получение/нет уведомлений от автора этой публикации");
}

$is_opened_pub_additional_functions = 0;
$opened_pub_additional_functions_id = 0;
function togglePubAdditionalFunctionsPub(idPub) {
  $('.pub_one.lifehack#'+idPub+' .pub_show_full').toggleClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg#pub').toggleClass('show');
  $('.pub_additional_functions_bg#pub .pub_additional_functions').offset($('.pub_one.lifehack#'+idPub+' .pub_show_full').offset());
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}
function togglePubAdditionalFunctionsAuthor(idPub) {
  $('.photo_nickname_role_additionalFunctions .additionalFunctions').toggleClass('opened');
  $('.pub_additional_functions_bg#author').toggleClass('show');
  $('.pub_additional_functions_bg#author .pub_additional_functions').offset($('.photo_nickname_role_additionalFunctions .additionalFunctions').offset());
  $is_opened_pub_additional_functions = 1;
  $opened_pub_additional_functions_id = idPub;
  console.log("Открыты дополнительные действия с публикацией под ID "+ idPub);
}
function openNewComplaintForm() {
  // $opened_pub_additional_functions_id
  $(' .new_complaint').addClass('show');
  if ($('.share_the_pub').hasClass('show')) {
    $('.share_the_pub').removeClass('show')
  }
}
function shareThePub() {
  // $opened_pub_additional_functions_id
  $(' .share_the_pub').addClass('show');
  if ($('.new_complaint').hasClass('show')) {
    $('.new_complaint').removeClass('show')
  }
}

function new_complaint_was_sent() {
  $idPub = $opened_pub_additional_functions_id;
  $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
  $('.pub_additional_functions_bg').removeClass('show');
  $is_opened_pub_additional_functions = 0;
  $opened_pub_additional_functions_id = 0;
  $('.new_complaint').removeClass('show');
  $('.new_complaint textarea').val('');
  testFu('Жалоба успешно отправлена, будет проверена когда-то там');
  console.log("Жалоба типо отпрвлена");
}

function checkScrollForVideo() {
  var fraction = 0.9; // Play video when 80% of the player is visible.

  $('video').each(function(){
    var video = $(this).get(0);
    var x = video.offsetLeft, y = video.offsetTop, w = video.offsetWidth, h = video.offsetHeight, r = x + w, //right
        b = y + h, //bottom
        visibleX, visibleY, visible;

        visibleX = Math.max(0, Math.min(w, window.pageXOffset + window.innerWidth - x, r - window.pageXOffset));
        visibleY = Math.max(0, Math.min(h, window.pageYOffset + window.innerHeight - y, b - window.pageYOffset));

        visible = visibleX * visibleY / (w * h);

    if (visible > fraction) {
        $(this).removeClass('paused');
        video.play();
        console.log("видео начало воспроизвоиться");
    } else {
        video.pause();
        console.log("видео не начало / перестало воспроизвоиться");
        $(this).addClass('paused');
    }
  })
}

function testFu(t) {
  alert (t);
}


$(document).on('click', function(e) {
  if ($is_opened_pub_additional_functions == 1) {
    if ($(e.target).hasClass('pub_additional_functions_bg')) {
      $idPub = $opened_pub_additional_functions_id;
      $('.pub_one.lifehack#'+$idPub+' .pub_show_full').removeClass('pub_additional_functions_opened');
      $('.photo_nickname_role_additionalFunctions .additionalFunctions').removeClass('opened');
      $('.pub_additional_functions_bg').removeClass('show');
      $is_opened_pub_additional_functions = 0;
      $opened_pub_additional_functions_id = 0;
      $('.new_complaint').removeClass('show');
      $('.share_the_pub').removeClass('show');
      console.log("Закрылись дополнительные действия с публикацией с ID "+ $idPub);
    }
  }
});


$(window).scroll(function () {
  checkScrollForVideo();

  if ($is_opened_pub_additional_functions == 1) {
    $idPub = $opened_pub_additional_functions_id;
    $('.pub_one.lifehack#'+$idPub+' .pub_show_full').toggleClass('pub_additional_functions_opened');
    $('.photo_nickname_role_additionalFunctions .additionalFunctions').removeClass('opened');
    $('.pub_additional_functions_bg').removeClass('show');
    $is_opened_pub_additional_functions = 0;
    $opened_pub_additional_functions_id = 0;
    $('.new_complaint').removeClass('show');
    $('.share_the_pub').removeClass('show');
    console.log("Дополнительные действия с публикацией закрылись :3");
  }
});
