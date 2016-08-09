// Hardware parameters
type = 'wifi';
address = 'arduino.local';

setInterval(function() {

  // Update power
  json_data = send(type, address, '/id');

  // Update status
  if (json_data.connected == 1){
    $("#status").html("Device Online");
    $("#status").css("color","green");    
  }
  else {
    $("#status").html("Device Offline");
    $("#status").css("color","red");     
  }

}, 5000);

// Function to control the lamp
function buttonClick(name){
    var req = new XMLHttpRequest();
    req.open("GET",'/toggleSwitch?sensor=3D%20Printer&state=True',false);
    req.send(null);
}