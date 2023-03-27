var Discord = require('discord.io');
var fs = require('fs');

var vineBoomStart = function(bot){
    //Let's join the voice channel, the ID is whatever your voice channel's ID is.
    bot.joinVoiceChannel('187399091418824705', function(error, events) {
        //Check to see if any errors happen while joining.
        if (error) return console.error(error);

        //Then get the audio context
        bot.getAudioContext('187399091418824705', function(error, stream) {
            //Once again, check to see if any errors exist
            if (error) return console.error(error);

            //Create a stream to your file and pipe it to the stream
            //Without {end: false}, it would close up the stream, so make sure to include that.
            fs.createReadStream('myFile.mp3').pipe(stream, {end: false});

            //The stream fires `done` when it's got nothing else to send to Discord.
            stream.on('done', function() {
               //Handle
            });
        });
    });
}

module.exports.vineBoomStart = vineBoomStart;