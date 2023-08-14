function move_axis(axis, distance) {
  var xhr = new XMLHttpRequest();
  var form_data = new FormData()

  xhr.open("POST", "api/ctrl/move")
  form_data.append('axis', axis)
  form_data.append('distance', distance)
  xhr.onload = function() {
    if(xhr.status == 200) {
      console.log("move success")
    }
  }
  xhr.send(form_data)
}

function get_move_distance()
{
  return 10;
}

function move_left() {
  distance = get_move_distance();
  move_axis('X', distance);
}

function move_right() {
  distance = get_move_distance();
  move_axis('X', -distance);
}

function move_front() {
  distance = get_move_distance();
  move_axis('Y', distance);
}

function move_back() {
  distance = get_move_distance();
  move_axis('Y', -distance);
}

function move_up() {
  distance = get_move_distance();
  move_axis('Z', distance);
}

function move_down() {
  distance = get_move_distance();
  move_axis('Z', -distance);
}

function set_bed_temp(event) {
  if(event.keyCode == 13) {
    var xhr = new XMLHttpRequest();
    var form_data = new FormData();
    xhr.open("POST", "api/ctrl/heat");
    form_data.append("target", "2");
    form_data.append("temp", document.getElementById('targetBedTemp').value);
    xhr.onload = function() {
      console.log("heat success");
    }
    xhr.send(form_data);
  }
}

function set_nozzle_temp(event) {
  if(event.keyCode == 13) {
    var xhr = new XMLHttpRequest();
    var form_data = new FormData();
    xhr.open("POST", "api/ctrl/heat");
    form_data.append("target", "0");
    form_data.append("temp", document.getElementById('targetTemp0').value);
    xhr.onload = function() {
      console.log("heat success");
    }
    xhr.send(form_data);
  }
}