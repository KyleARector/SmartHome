// Module
var express = require('express');
var path = require('path');
var redis = require('redis');

// Create app
var app = express();
var port = 3700;
var client = redis.createClient(4747, '127.0.0.1');
var sensorList = []

// Set views
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'views')));

// Serve files
app.get('/', function(req, res){
  res.sendfile('views/interface.html')
});

// API access
app.get('/key', function getKeyDetails(req, res, next) {
  if(req.query.key){
    var key = req.query.key;
    console.log('getting value of key ' + key);
    client.get(key, function(err, value) {
      res.json(value);
    });
  }
  else {
    res.json("No key sent");
  }
});

app.get('/sensors', function testGetting(req, res) {
    client.lrange('sensors', 0, -1, function (error, items) {
        sensorList = [];
        items.forEach(function (item) {
            sensorList.push(JSON.parse(item));
        });
    });
    res.json(sensorList);
});

// Start server
app.listen(port);
console.log("Listening on port " + port);
