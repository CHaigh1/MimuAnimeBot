const fs = require('fs');

var events = function events(){
  var textByLine = fs.readFileSync("./events.txt").toString().split("\n");
  
  var eventList = "";
  for(var i = 0; i < textByLine.length; i++) {
    eventList += textByLine[i].trim() + '\n';
  }

  return eventList;
};

var addEvent = function addEvent(input){
  fs.appendFile('events.txt', input + '\n', (err) => {
    if (err) throw err;
  });
};

var removeEvent = function removeEvent(index){
  var textByLine = fs.readFileSync("./events.txt").toString().split("\n");
  
  var eventList = "";
  for(var i = 0; i < textByLine.length - 1; i++) {
    if(i != index) {
      eventList += textByLine[i].trim() + '\n';
    }
  }
  eventList += textByLine[textByLine.length - 1].trim();

  fs.writeFile('events.txt', eventList, (err) => {
    if (err) throw err;
  });
};

module.exports.events = events;
module.exports.addEvent = addEvent;
module.exports.removeEvent = removeEvent;