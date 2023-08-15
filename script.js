// alert('x:' +screen.width + ' y:' + screen.height);

// for menu style
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}


// on tab-button(print, upload, ctrl) clicked
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var file_btns = document.getElementsByClassName("file_item");
var file_name = document.getElementById("file_name");
var priniting_file_name = document.getElementById("printing_filename");


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
for (let j = 0; j < file_btns.length; j++) {

  file_btns[j].onclick = function() {
    var filename = file_btns.item(j).innerHTML;
    if(filename!=""){
      modal.style.display = "block";
      // change text of span
      file_name.innerHTML = filename;
      priniting_file_name.innerHTML = filename;
  
      //get info of this file and wait for it
  
    }
  }
}

var goPrint = document.getElementById("go2print")
goPrint.onclick = function(){
  modal.style.display = "none";
  document.getElementById("defaultOpen").click();
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var pause_resume_btn = document.getElementById("btn_pause_resume");
pause_resume_btn.onclick = function(){
  if (pause_resume_btn.innerHTML=="Pause") {
    pause_resume_btn.innerHTML="Resume";
  }else{
    pause_resume_btn.innerHTML="Pause";
  }
}

// menubtn
function menu_toggle(x) {
  x.classList.toggle("change");
}

var url_get_status = "api/g_status";
function send_get(url) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, false);
  xhr.onreadystatechange = function() {
    if(xhr.readyState == 4) {
      if(xhr.status == 200) {
        
      }
      else {
        console.log(xhr.status)
      }
    }
  }
  xhr.send();
}

function request_status() {
  send_get(url_get_status);
}

var bed_temp=25;

// var timerId = setInterval(() => {
//   bed_temp = bed_temp + 1;
//   document.getElementById("bed_temp").innerHTML = bed_temp;
// }, 1000);

function body_init() {
  location.reload(true);
}