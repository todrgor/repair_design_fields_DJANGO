let $to_notifications = $('.to_notifications');

$to_notifications.on('click', function () {
  $('.notifications_container').toggleClass('show_ntfctns_more');
  if ($is_opened_notifications == 0) {
    $is_opened_notifications = 1;
  } else {
    $is_opened_notifications = 0;
  }
  console.log('$is_opened_notifications = ', $is_opened_notifications);
});
