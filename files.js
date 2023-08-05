var file_list_page_index = 0;

function file_list() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", 'api/files/list?page=' + file_list_page_index + '&page_per_count=10', true);
  xhr.onload = function() {
    if(xhr.status == 200) {
      console.log("Upload succes");
      var response_text = xhr.responseText;
      window.file_list_page_index = response_text.slice(1, response_text.indexOf(']'));
      file_names = response_text.slice(response_text.indexOf(']') + 1).split('//');
      console.log(window.file_list_page_index)
      console.log(file_names)

      // Clear item
      for(var i=0;i<10;i++) {
        document.getElementById("file" + i).innerHTML = "";
      }

      if(file_names.length > 0) {
        for(index in file_names) {
          document.getElementById("file" + index).innerHTML = file_names[index];
        }
      }
      else {

      }
    }
  }
  xhr.send();
}

function file_first_page() {
  window.file_list_page_index = 0;
  file_list();
}

function file_next_page() {
  window.file_list_page_index++;
  file_list();
}

function file_prev_page() {
  if(window.file_list_page_index > 0) {
    window.file_list_page_index--;
    file_list();
  }
}

function file_upload() {
  var xhr = new XMLHttpRequest()
  xhr.open("POST", "api/files/upload", true)
  var form_data = new FormData();
  form_data.append('file', document.getElementById('file').files[0])
  xhr.onload = function() {
    if(xhr.status == 200) {
      console.log("Upload success");
    }
  }
  xhr.send(form_data);
}
