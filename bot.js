var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');

var eventGrabber = require('./eventGrabber.js');
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`
    if (message.substring(0, 1) == '!') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
       
        args = args.splice(1);
        switch(cmd) {
            // !ping
            case 'ping':
                bot.sendMessage({
                    to: channelID,
                    message: 'Pong!'
                });
            break;
            // !calendar
            // Gets the current day
            case 'date':
                var today = new Date();
                var dd = String(today.getDate()).padStart(2, '0');
                var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                var yyyy = today.getFullYear();

                today = mm + '/' + dd + '/' + yyyy;
                
                bot.sendMessage({
                    to: channelID,
                    message: 'The current date is: ' + today
                });
            break;
            // !events
            // Gets the events for the next few days
            case 'events':
                if(args[0] == 'add') {
                    var input = "";
                    var inputArr = args.slice(1);
                    
                    inputArr.forEach(word => input = input + word + ' ');
                    eventGrabber.addEvent(input);
                    
                    bot.sendMessage({
                        to: channelID,
                        message: 'Recieved event!'
                    });
                }
                else if(args[0] == 'remove') {
                    if(args.length != 2) {
                        bot.sendMessage({
                            to: channelID,
                            message: 'Incorrect usage! Proper format is "!events remove <message id>"'
                        });
                    } 
                    else {
                        eventGrabber.removeEvent(args[1]);
                        bot.sendMessage({
                            to: channelID,
                            message: 'Event removed!'
                        });
                    }
                }
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: 'Here are the upcoming events:\n\n' + eventGrabber.events()
                    });
                }
            break;
            // Just add any case commands if you want to..
         }
     }
});