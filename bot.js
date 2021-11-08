var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');

var reminder = require('./helpers/remindHelper.js');
var malParser = require('./helpers/malParser.js');
var randomImage = require('./helpers/randomImage.js');
var solve = require('./helpers/solve.js');
var randomGame = require('./helpers/randomGame.js');
var vineBoom = require('./helpers/vineBoomHelper.js');

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

    vineBoom.vineBoomStart(bot);
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
            case 'remind':
                if(args[0] == 'add') {
                    var input = "";
                    var inputArr = args.slice(1);
                    
                    inputArr.forEach(word => input += word + ' ');
                    reminder.addReminder(input);
                    
                    bot.sendMessage({
                        to: channelID,
                        message: '**Recieved reminder!**'
                    });
                }
                else if(args[0] == 'remove') {
                    if(args.length != 2) {
                        bot.sendMessage({
                            to: channelID,
                            message: '**Incorrect usage! Proper format is "!remind remove <message id>"**'
                        });
                    } 
                    else {
                        reminder.removeReminder(args[1]);
                        bot.sendMessage({
                            to: channelID,
                            message: '**Reminder removed!**'
                        });
                    }
                }
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: '**Here are the current group reminders:**\n```\n' + reminder.reminders() + '```'
                    });
                }
            break;
            // !anime
            // Does anime things
            /*case 'anime':
                if(args.length != 2) {
                    bot.sendMessage({
                        to: channelID,
                        message: '**Incorrect usage! Proper format is "!anime <year> <season>"**'
                    })
                }
                else {
                    malParser.topSeason(args[0], args[1], function(results) {
                        bot.sendMessage({
                            to: channelID,
                            message: '**Here are the top 5 shows from the ' + args[1] + ' ' + args[0] + ' season:**\n```\n' + results + '```'
                        });
                    });
                }
            break;*/
            // !epic
            // Shows how epic you are
            case 'epic':
                if(args.length > 0) {
                    var epicString = '';
                    args.forEach(word => epicString += word + ' ');
                    bot.sendMessage({
                        to: channelID,
                        message: '**On the epic scale, I rate ' + epicString + ' ' + Math.floor(Math.random() * 10) + ' out of 10**'
                    });
                }
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: '**On the epic scale, I rate ' + user + ' ' + Math.floor(Math.random() * 10) + ' out of 10**'
                    });
                }
            break;
            // !rimage
            // Displays a random image from imgur
            case 'rimage':
                bot.sendMessage({
                    to: channelID,
                    message: randomImage.getImage()
                });
            break;
            // !solve
            // Answers a math equation with 2 integers
            case 'solve':
                if(args.length != 3) {
                    bot.sendMessage({
                        to: channelID,
                        message: '**The proper format is *!solve <number1> <sign> <number2>***'
                    });
                }
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: '**The answer to your problem is: ' + solve.solve(parseInt(args[0]), args[1], parseInt(args[2])) + '**'
                    });
                }
            break;
            // !rgame
            // Chooses a random game to play. games.txt
            case 'rgame':
                if(args[0] == 'add') {
                    var input = "";
                    var inputArr = args.slice(1);
                    
                    inputArr.forEach(word => input += word + ' ');
                    randomGame.addGame(input);
                    
                    bot.sendMessage({
                        to: channelID,
                        message: '**Added game to list!**'
                    });
                }
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: '**You should play: *' + randomGame.game() + '***'
                    });
                }
            break;
         }
     }
});