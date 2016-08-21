// Module
var express = require('express');
var path = require('path');
var redis = require('redis');

// Create app
var app = express();
var port = 80;
var client = redis.createClient(4747, '127.0.0.1');
var sensorList = [];
var tempChange = 0;
var tempSet = 0;

// Set views
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'views')));

// Serve files
app.get('/', function(req, res){
  res.sendfile('views/interface.html')
});

// API access
app.get('/sensorState', function getState(req, res, next) {
  if(req.query.sensor){
    var sensor = req.query.sensor;
    console.log('getting value of sensor ' + sensor);
    client.get(sensor, function(err, value) {
      res.json(value);
    });
  }
  else {
    res.json("No Sensor Sent");
  }
});

app.get('/toggleSwitch', function toggleSwitch(req, res) {
  if(req.query.sensor && req.query.state){
      var sensor = req.query.sensor;
      var state = req.query.state;
      console.log('Toggling switch ' + sensor);
      var message = '{"name": "' + sensor + '", "state": "' + state + '"}'
      client.rpush('sensor_changes', message);
      res.json(message);
  }
  else {
    res.json("Incorrect Parameters");
  }
});

app.get('/sensors', function getSensors(req, res) {
    client.lrange('sensors', 0, -1, function (error, items) {
        sensorList = [];
        items.forEach(function (item) {
            sensorList.push(JSON.parse(item));
        });
        res.json(sensorList);
    });
});

app.get('/thermostat', function thermoReport(req, res) {
    client.get('tempSet', function(err, reply){
        tempSet = parseInt(reply);
        client.get('tempChange', function (err, reply) {
            tempChange = parseInt(reply);
            var tempDelta = tempChange - tempSet;
            client.set('tempSet', tempChange);
            var output = {"tempDelta":  + " " + tempDelta};
            res.json(output);
        });
    });
});

// Start server
app.listen(port);
console.log("Listening on port " + port);
