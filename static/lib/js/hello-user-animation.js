jQuery(document).ready(function() {
  var slides = document.getElementsByClassName('slide_r');
  var currentSlide = 0;
  var navigation = document.getElementsByClassName('navigation');
  if (navigation.length > 0) {
    var slideInterval = setInterval(nextSlide, 4800);
    function nextSlide() {
    console.log('Scroll: ' + $(window).scrollTop());
    if ($(window).scrollTop() < screen.height*0.53) {
      slides[currentSlide].className = 'slide_r isnt_showing';
      currentSlide = (currentSlide+1) % slides.length;
      slides[currentSlide].checked = true;
      slides[currentSlide].className = 'slide_r isnt_showing';
     }
   ;}
  };

  $slides = $('.slider_container .slide');
  $slidesFooter = $('.pub_type_one');
  if ($slides.length > 0) {
    $id_showing_slide = 0;
    $slideTimer= setInterval(nextSlideAboutPub, 3500);
    function nextSlideAboutPub() {
      $('#'+ $id_showing_slide +'.slide').removeClass('show');
      $('#'+ $id_showing_slide +'.pub_type_one').removeClass('show');
      $id_showing_slide += 1;
      if ($id_showing_slide == $slides.length) {$id_showing_slide = 0;}
      $('#'+ $id_showing_slide +'.slide').addClass('show');
      $('#'+ $id_showing_slide +'.pub_type_one').addClass('show');
    }
  };
});

$(".header_reg_btm").click(function(){
  $("html, body").stop().animate( {
    scrollTop: screen.height*1.3
  }, 1200);
});

$(".submit_bs_form_input").hover(
  function(){
    $(".submit_bs_form").css("background", "#1b1b28");
  },
  function(){
    $(".submit_bs_form").css("background", "#000");
  }
);
