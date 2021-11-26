function cancel_following(idUser) {
  $('.user_one#'+idUser+' .cancel_following').toggleClass('dont_cancel');
  if ($('.user_one#'+idUser+' .cancel_following').hasClass('dont_cancel')) {
    $('.user_one#'+idUser+' .cancel_following').html('Подписаться');
  } else {
    $('.user_one#'+idUser+' .cancel_following').html('Отписаться');
  }
}
