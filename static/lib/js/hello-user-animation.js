jQuery(document).ready(function() {
console.log('Высота экрана: ' + screen.height);
var slides = document.getElementsByClassName('slide_r');
var currentSlide = 0;
var slideInterval = setInterval(nextSlide, 4800);
var navigation = document.getElementsByClassName('navigation');
function nextSlide() {
  console.log('Scroll: ' + $(window).scrollTop());
  if ($(window).scrollTop() < screen.height*0.53) {
    slides[currentSlide].className = 'slide_r isnt_showing';
    currentSlide = (currentSlide+1)%slides.length;
    slides[currentSlide].checked = true;
    slides[currentSlide].className = 'slide_r isnt_showing';
   }
 ;}
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
