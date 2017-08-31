function alert_box() {
  alert("Welcome to Grace Milton's Portfolio Webpage! I hope you enjoy exploring it as much as I enjoyed creating it.");
}
function zoom() {
  document.getElementById("profile_photo").id = "zoomed";
}
function unzoom() {
  document.getElementById("zoomed").id = "profile_photo";
}

function reveal() {
  ff.style.display="block";
  ff_button.style.display="none";
  ff_title.style.display="block";
}
function plusDivs(n) {
  showDivs(slideIndex += n);
}
function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex-1].style.display = "inline";
}
