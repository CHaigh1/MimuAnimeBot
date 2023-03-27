const fs = require('fs');

var game = function game(){
  var textByLine = fs.readFileSync("./games.txt").toString().split("\n");
  
  var gameList = [];
  for(var i = 0; i < textByLine.length; i++) {
    gameList.push(textByLine[i].trim());
  }

  var randomIndex = Math.floor(Math.random() * gameList.length);
  return gameList[randomIndex];
}

var addGame = function addGame(input){
  fs.appendFile('./games.txt', '\n' + input, (err) => {
    if (err) throw err;
  });
}

module.exports.game = game;
module.exports.addGame = addGame;