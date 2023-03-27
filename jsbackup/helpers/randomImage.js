var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

var getImage = function getImage(){
  valid = false;
  url = '';

  while(!valid) {
    var rstring = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
    var http = new XMLHttpRequest();
    http.open('HEAD', 'http://i.imgur.com/' + rstring + '.jpg', false);
    http.send();
    
    if (http.status != 404) {
      valid = true;
      url = 'http://i.imgur.com/' + rstring + '.jpg';
    }
  }
  
  return url;
};

module.exports.getImage = getImage;