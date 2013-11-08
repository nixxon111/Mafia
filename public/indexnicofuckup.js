	$(document).ready(function()
{
	IO.init();
});

	var IO =
	{
		init: function()
		{
			// IO variables
			IO.socket = io.connect("http://localhost:8000", 
			{
			"sync disconnect on unload" : true
			});
			IO.messages = [];
			IO.input = $("#chatinput");
			IO.sendButton = $("#sendButton");
			IO.btnCreateGame = $("#btnCreateGame");
			IO.chatwindow = $("#chatwindow");
			IO.userlistbox = $("#userList");
			IO.playerlist = $("#testtext");
			IO.name = prompt("what's your name?");
			
/* Annagrammatix
			onNewGameCreated : function(data) 
			{
            		Game.Host.gameInit(data);
        		};
*/

			IO.bindEvents();

		},

		bindEvents: function()
		{
			IO.socket.on("updatechat", IO.updateChat);
			IO.sendButton.click(IO.sendChatMessage);
			IO.socket.on("updateusers", IO.updateUserList);

			IO.btnCreateGame.click(IO.startGame);
			
			IO.socket.on("connect", function()
			{
				IO.socket.emit("adduser", IO.name);
			});
		
			IO.socket.on("disconnect", function()
			{
				IO.socket.emit("removeuser", IO.socket.id);
			});

/* Annagrammatix*/
			IO.socket.on('newGameCreated', IO.onNewGameCreated );
            		IO.socket.on('playerJoinedRoom', IO.playerJoinedRoom );
            		IO.socket.on('beginNewGame', IO.beginNewGame );
            		IO.socket.on('error', Game.error );

			IO.input.keypress(function(e)
			{
				if(e.which == 13)
				{
					IO.sendChatMessage();
				}
			});

		},
/* Annagrammatix*/
		onConnected : function() {
            		// Cache a copy of the client's socket.IO session ID on the App
            		App.mySocketId = IO.socket.socket.sessionid;
           		// console.log(data.message);
        	},
		updateUserList: function(data)
		{	
			IO.userlistbox.html("");
			for (var value in data)
			{
				IO.userlistbox.append("<li>"+data[value]+"</li>");
			}

		},
		updateChat: function(data)
		{

			if (data.message)
			{
				IO.messages.push({user : data.user, message : data.message});
				var html = "";
				for (var i = 0; i < IO.messages.length; i++)
				{
					html += IO.messages[i].user +": "+IO.messages[i].message + "<br/>";
				}
				IO.chatwindow.html(html);
			}
			else 
			{
				console.log("invalid data received");
			}
		},
		sendChatMessage: function()
		{
			var messagetext = IO.input.val();
			IO.socket.emit("updatechat", { user: IO.name, message: messagetext});
			if (messagetext == "day") {
				$("#daynight").text('Day');
			}
			

			if (messagetext == 'night') {
				$("#daynight").text('Night');
			}

			if (messagetext == "startgame") {
				startGame();
			}
			
			IO.input.val("");
			$("#chatinput").focus();

		},

		startGame: function(data) 
		{	
		
			alert( "Handler for .click() called." );
			Game[Game.myRole].gameCountdown(data);
		}

/*******************************************************************************
 ****									    ****
 ****				From annagrammatix MPgame		    ****
 **** 									    ****
 *******************************************************************************/

};

Var Game = {
	//App[App.myRole]

	beginNewGame : function(data) 
	{
            App[App.myRole].gameCountdown(data);
        },
	error : function(data) 
	{
            alert(data.message);
        }



}
	};



 
    



    var App = {
	// Initialize variables
        /**
         * Keep track of the gameId, which is identical to the ID
         * of the Socket.IO Room used for the players and host to communicate
         *
         */
        gameId: 0,

        
        myRole: '',   

        /**
         * The Socket.IO socket object identifier. This is unique for
         * each player and host. It is generated when the browser initially
         * connects to the server when the page loads for the first time.
         */
        mySocketId: '',

        /**
         * Identifies the current round.
         */
        currentRound: 1,

        /* *************************************
         *                Setup                *
         * *********************************** */

        /**
         * This runs when the page initially loads.
         */
        init: function () {
            Game.cacheElements();
            Game.showInitScreen();
            Game.bindEvents();

            // Initialize the fastclick library
            FastClick.attach(document.body);
        },

        /**
         * Create references to on-screen elements used throughout the game.
         */
        cacheElements: function () {
            Game.$doc = $(document);

            // Templates
            Game.$gameArea = $('#gameArea');
            Game.$templateIntroScreen = $('#intro-screen-template').html();
            Game.$templateNewGame = $('#create-game-template').html();
            Game.$templateJoinGame = $('#join-game-template').html();
            Game.$hostGame = $('#host-game-template').html();
        },

        /**
         * Create some click handlers for the various buttons that appear on-screen.
         */
        bindEvents: function () {
            // Host
            Game.$doc.on('click', '#btnCreateGame', App.Host.onCreateClick);

            // Player
            Game.$doc.on('click', '#btnJoinGame', App.Player.onJoinClick);
            Game.$doc.on('click', '#btnStart',App.Player.onPlayerStartClick);
            Game.$doc.on('click', '.btnAnswer',App.Player.onPlayerAnswerClick);
            Game.$doc.on('click', '#btnPlayerRestart', App.Player.onPlayerRestart);
        },

        /* *************************************
         *             Game Logic              *
         * *********************************** */

        /**
         * Show the initial Anagrammatix Title Screen
         * (with Start and Join buttons)
         */
        showInitScreen: function() {
            Game.$gameArea.html(App.$templateIntroScreen);
            Game.doTextFit('.title');
        },


        /* *******************************
           *         HOST CODE           *
           ******************************* */
        Host : {

            /**
             * Contains references to player data
             */
            players : [],

            /**
             * Flag to indicate if a new game is starting.
             * This is used after the first game ends, and players initiate a new game
             * without refreshing the browser windows.
             */
            isNewGame : false,

            /**
             * Keep track of the number of players that have joined the game.
             */
            numPlayersInRoom: 0,

            /**
             * A reference to the correct answer for the current round.
             */
            currentCorrectAnswer: '',

            /**
             * Handler for the "Start" button on the Title Screen.
             */
            onCreateClick: function () {
                // console.log('Clicked "Create A Game"');
                IO.socket.emit('hostCreateNewGame');
            },

            /**
             * The Host screen is displayed for the first time.
             * @param data{{ gameId: int, mySocketId: * }}
             */
            gameInit: function (data) {
                Game.gameId = data.gameId;
                Game.mySocketId = data.mySocketId;
                Game.myRole = 'Host';
                Game.Host.numPlayersInRoom = 0;

                Game.Host.displayNewGameScreen();
                // console.log("Game started with ID: " + App.gameId + ' by host: ' + App.mySocketId);
            },

            /**
             * Show the Host screen containing the game URL and unique game ID
             */
            displayNewGameScreen : function() {
                // Fill the game screen with the appropriate HTML
                App.$gameArea.html(App.$templateNewGame);

                // Display the URL on screen
                $('#gameURL').text(window.location.href);
                App.doTextFit('#gameURL');

                // Show the gameId / room id on screen
                $('#spanNewGameCode').text(App.gameId);
            },

            /**
             * Update the Host screen when the first player joins
             * @param data{{playerName: string}}
             */
            updateWaitingScreen: function(data) {
                // If this is a restarted game, show the screen.
                if ( App.Host.isNewGame ) {
                    App.Host.displayNewGameScreen();
                }
                // Update host screen
                $('#playersWaiting')
                    .append('<p/>')
                    .text('Player ' + data.playerName + ' joined the game.');

                // Store the new player's data on the Host.
                App.Host.players.push(data);

                // Increment the number of players in the room
                App.Host.numPlayersInRoom += 1;

                // If two players have joined, start the game!
                if (App.Host.numPlayersInRoom === 2) {
                    // console.log('Room is full. Almost ready!');

                    // Let the server know that two players are present.
                    IO.socket.emit('hostRoomFull',App.gameId);
                }
            },

            /**
             * Show the countdown screen
             */
            gameCountdown : function() {

                // Prepare the game screen with new HTML
                App.$gameArea.html(App.$hostGame);
                App.doTextFit('#hostWord');

                // Begin the on-screen countdown timer
                var $secondsLeft = $('#hostWord');
                App.countDown( $secondsLeft, 5, function(){
                    IO.socket.emit('hostCountdownFinished', App.gameId);
                });

                // Display the players' names on screen
                $('#player1Score')
                    .find('.playerName')
                    .html(App.Host.players[0].playerName);

                $('#player2Score')
                    .find('.playerName')
                    .html(App.Host.players[1].playerName);

                // Set the Score section on screen to 0 for each player.
                $('#player1Score').find('.score').attr('id',App.Host.players[0].mySocketId);
                $('#player2Score').find('.score').attr('id',App.Host.players[1].mySocketId);
            },

            /**
             * Show the word for the current round on screen.
             * @param data{{round: *, word: *, answer: *, list: Array}}
             */
            newWord : function(data) {
                // Insert the new word into the DOM
                $('#hostWord').text(data.word);
                App.doTextFit('#hostWord');

                // Update the data for the current round
                App.Host.currentCorrectAnswer = data.answer;
                App.Host.currentRound = data.round;
            },

            /**
             * Check the answer clicked by a player.
             * @param data{{round: *, playerId: *, answer: *, gameId: *}}
             */
            checkAnswer : function(data) {
                // Verify that the answer clicked is from the current round.
                // This prevents a 'late entry' from a player whos screen has not
                // yet updated to the current round.
                if (data.round === App.currentRound){

                    // Get the player's score
                    var $pScore = $('#' + data.playerId);

                    // Advance player's score if it is correct
                    if( App.Host.currentCorrectAnswer === data.answer ) {
                        // Add 5 to the player's score
                        $pScore.text( +$pScore.text() + 5 );

                        // Advance the round
                        App.currentRound += 1;

                        // Prepare data to send to the server
                        var data = {
                            gameId : App.gameId,
                            round : App.currentRound
                        }

                        // Notify the server to start the next round.
                        IO.socket.emit('hostNextRound',data);

                    } else {
                        // A wrong answer was submitted, so decrement the player's score.
                        $pScore.text( +$pScore.text() - 3 );
                    }
                }
            },


            /**
             * All 10 rounds have played out. End the game.
             * @param data
             */
            endGame : function(data) {
                // Get the data for player 1 from the host screen
                var $p1 = $('#player1Score');
                var p1Score = +$p1.find('.score').text();
                var p1Name = $p1.find('.playerName').text();

                // Get the data for player 2 from the host screen
                var $p2 = $('#player2Score');
                var p2Score = +$p2.find('.score').text();
                var p2Name = $p2.find('.playerName').text();

                // Find the winner based on the scores
                var winner = (p1Score < p2Score) ? p2Name : p1Name;
                var tie = (p1Score === p2Score);

                // Display the winner (or tie game message)
                if(tie){
                    $('#hostWord').text("It's a Tie!");
                } else {
                    $('#hostWord').text( winner + ' Wins!!' );
                }
                App.doTextFit('#hostWord');

                // Reset game data
                App.Host.numPlayersInRoom = 0;
                App.Host.isNewGame = true;
            },

            /**
             * A player hit the 'Start Again' button after the end of a game.
             */
            restartGame : function() {
                App.$gameArea.html(App.$templateNewGame);
                $('#spanNewGameCode').text(App.gameId);
            }
        },


        /* *****************************
           *        PLAYER CODE        *
           ***************************** */

        Player : {

            /**
             * A reference to the socket ID of the Host
             */
            hostSocketId: '',

            /**
             * The player's name entered on the 'Join' screen.
             */
            myName: '',

            /**
             * Click handler for the 'JOIN' button
             */
            onJoinClick: function () {
                // console.log('Clicked "Join A Game"');

                // Display the Join Game HTML on the player's screen.
                App.$gameArea.html(App.$templateJoinGame);
            },

            /**
             * The player entered their name and gameId (hopefully)
             * and clicked Start.
             */
            onPlayerStartClick: function() {
                // console.log('Player clicked "Start"');

                // collect data to send to the server
                var data = {
                    gameId : +($('#inputGameId').val()),
                    playerName : $('#inputPlayerName').val() || 'anon'
                };

                // Send the gameId and playerName to the server
                IO.socket.emit('playerJoinGame', data);

                // Set the appropriate properties for the current player.
                App.myRole = 'Player';
                App.Player.myName = data.playerName;
            },

            /**
             *  Click handler for the Player hitting a word in the word list.
             */
            onPlayerAnswerClick: function() {
                // console.log('Clicked Answer Button');
                var $btn = $(this);      // the tapped button
                var answer = $btn.val(); // The tapped word

                // Send the player info and tapped word to the server so
                // the host can check the answer.
                var data = {
                    gameId: App.gameId,
                    playerId: App.mySocketId,
                    answer: answer,
                    round: App.currentRound
                }
                IO.socket.emit('playerAnswer',data);
            },

            /**
             *  Click handler for the "Start Again" button that appears
             *  when a game is over.
             */
            onPlayerRestart : function() {
                var data = {
                    gameId : App.gameId,
                    playerName : App.Player.myName
                }
                IO.socket.emit('playerRestart',data);
                App.currentRound = 0;
                $('#gameArea').html("<h3>Waiting on host to start new game.</h3>");
            },

            /**
             * Display the waiting screen for player 1
             * @param data
             */
            updateWaitingScreen : function(data) {
                if(IO.socket.socket.sessionid === data.mySocketId){
                    App.myRole = 'Player';
                    App.gameId = data.gameId;

                    $('#playerWaitingMessage')
                        .append('<p/>')
                        .text('Joined Game ' + data.gameId + '. Please wait for game to begin.');
                }
            },

            /**
             * Display 'Get Ready' while the countdown timer ticks down.
             * @param hostData
             */
            gameCountdown : function(hostData) {
                App.Player.hostSocketId = hostData.mySocketId;
                $('#gameArea')
                    .html('<div class="gameOver">Get Ready!</div>');
            },

            /**
             * Show the list of words for the current round.
             * @param data{{round: *, word: *, answer: *, list: Array}}
             */
            newWord : function(data) {
                // Create an unordered list element
                var $list = $('<ul/>').attr('id','ulAnswers');

                // Insert a list item for each word in the word list
                // received from the server.
                $.each(data.list, function(){
                    $list                                //  <ul> </ul>
                        .append( $('<li/>')              //  <ul> <li> </li> </ul>
                            .append( $('<button/>')      //  <ul> <li> <button> </button> </li> </ul>
                                .addClass('btnAnswer')   //  <ul> <li> <button class='btnAnswer'> </button> </li> </ul>
                                .addClass('btn')         //  <ul> <li> <button class='btnAnswer'> </button> </li> </ul>
                                .val(this)               //  <ul> <li> <button class='btnAnswer' value='word'> </button> </li> </ul>
                                .html(this)              //  <ul> <li> <button class='btnAnswer' value='word'>word</button> </li> </ul>
                            )
                        )
                });

                // Insert the list onto the screen.
                $('#gameArea').html($list);
            },

            /**
             * Show the "Game Over" screen.
             */
            endGame : function() {
                $('#gameArea')
                    .html('<div class="gameOver">Game Over!</div>')
                    .append(
                        // Create a button to start a new game.
                        $('<button>Start Again</button>')
                            .attr('id','btnPlayerRestart')
                            .addClass('btn')
                            .addClass('btnGameOver')
                    );
            }
        },


        /* **************************
                  UTILITY CODE
           ************************** */

        /**
         * Display the countdown timer on the Host screen
         *
         * @param $el The container element for the countdown timer
         * @param startTime
         * @param callback The function to call when the timer ends.
         */
        countDown : function( $el, startTime, callback) {

            // Display the starting time on the screen.
            $el.text(startTime);
            App.doTextFit('#hostWord');

            // console.log('Starting Countdown...');

            // Start a 1 second timer
            var timer = setInterval(countItDown,1000);

            // Decrement the displayed timer value on each 'tick'
            function countItDown(){
                startTime -= 1
                $el.text(startTime);
                App.doTextFit('#hostWord');

                if( startTime <= 0 ){
                    // console.log('Countdown Finished.');

                    // Stop the timer and do the callback.
                    clearInterval(timer);
                    callback();
                    return;
                }
            }

        },

        /**
         * Make the text inside the given element as big as possible
         * See: https://github.com/STRML/textFit
         *
         * @param el The parent element of some text
         */
        doTextFit : function(el) {
            textFit(
                $(el)[0],
                {
                    alignHoriz:true,
                    alignVert:false,
                    widthOnly:true,
                    reProcess:true,
                    maxFontSize:300
                }
            );
        }

    };

    IO.init();
    App.init();

}($));


/**
 * .select2Buttons - Convert standard html select into button like elements
 * Provides an alternative look and feel for HTML select buttons, inspired by threadless.com
 * Author: Sam Cavenagh (cavenaghweb@hotmail.com)
 * Doco and Source: https://github.com/o-sam-o/jquery.select2Buttons

 * Der kan uden tvivl ryddes op i det lort herunder. Kan nico eventuelt gøre når han forstår hvad der sker :O
 **/

jQuery.fn.select2Buttons = function(options) {
  return this.each(function(){
    var $ = jQuery;
    var select = $(this);
    var multiselect = select.attr('multiple');
    select.hide();

    var buttonsHtml = $('<div class="select2Buttons"></div>');
    var selectIndex = 0;
    var addOptGroup = function(optGroup){
      if (optGroup.attr('label')){
        buttonsHtml.append('<strong>' + optGroup.attr('label') + '</strong>');
      }
      var ulHtml =  $('<ul class="select-buttons">');
      optGroup.children('option').each(function(){
        var liHtml = $('<li></li>');
        if ($(this).attr('disabled') || select.attr('disabled')){
          liHtml.addClass('disabled');
          liHtml.append('<span>' + $(this).html() + '</span>');
        }else{
          liHtml.append('<a href="#" data-select-index="' + selectIndex + '">' + $(this).html() + '</a>');
        }

        // Mark current selection as "picked"
        if((!options || !options.noDefault) && $(this).attr('selected')){
          liHtml.children('a, span').addClass('picked');
        }
        ulHtml.append(liHtml);
        selectIndex++;
      });
      buttonsHtml.append(ulHtml);
    }

    var optGroups = select.children('optgroup');
    if (optGroups.length == 0) {
      addOptGroup(select);
    }else{
      optGroups.each(function(){
        addOptGroup($(this));
      });
    }

    select.after(buttonsHtml);

    buttonsHtml.find('a').click(function(e){
      e.preventDefault();
      var clickedOption = $(select.find('option')[$(this).attr('data-select-index')]);
      if(multiselect){
        if(clickedOption.attr('selected')){
          $(this).removeClass('picked');
          clickedOption.removeAttr('selected');
        }else{
          $(this).addClass('picked');
          clickedOption.attr('selected', 'selected');
        }
      }else{
        buttonsHtml.find('a, span').removeClass('picked');
        $(this).addClass('picked');
        clickedOption.attr('selected', 'selected');
      }
      select.trigger('change');
    });
  });
};
