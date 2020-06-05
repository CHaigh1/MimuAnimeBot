const jikanjs = require('jikanjs');

var topSeason = function topSeason(year, season, callback){
  var top5shows = "";
  var showArr = [];

  jikanjs.loadSeason(year, season).then((response) => {
    response.anime.forEach(show => {
      showArr.push(show);
    });

    showArr.sort((a, b) => (a.score > b.score) ? -1 : 1);
    
    for(var i = 0; i < 5; i++) {
      top5shows += showArr[i].title + '\n';
    }
    callback(top5shows);
  }).catch((err) => {
    console.error(err);
  });
};

module.exports.topSeason = topSeason;