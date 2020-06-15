const fs = require('fs');

var reminders = function reminders(){
  var textByLine = fs.readFileSync("./reminders.txt").toString().split("\n");
  
  var reminderList = "";
  for(var i = 0; i < textByLine.length; i++) {
    reminderList += textByLine[i].trim() + '\n';
  }

  return reminderList;
};

var addReminder = function addReminder(input){
  fs.appendFile('./reminders.txt', input + '\n', (err) => {
    if (err) throw err;
  });
};

var removeReminder = function removeReminder(index){
  var textByLine = fs.readFileSync("./reminders.txt").toString().split("\n");
  
  var reminderList = "";
  for(var i = 0; i < textByLine.length - 1; i++) {
    if(i != index) {
      reminderList += textByLine[i].trim() + '\n';
    }
  }
  reminderList += textByLine[textByLine.length - 1].trim(); //this will add the newline after last line

  fs.writeFile('reminders.txt', reminderList, (err) => {
    if (err) throw err;
  });
};

module.exports.reminders = reminders;
module.exports.addReminder = addReminder;
module.exports.removeReminder = removeReminder;