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
			IO.chatwindow = $("#chatwindow");
			IO.userlistbox = $("#userList");
			IO.playerlist = $("#testtext");
			IO.name = prompt("what's your name?");
			
			IO.bindEvents();

		},

		bindEvents: function()
		{
			IO.socket.on("updatechat", IO.updateChat);
			IO.sendButton.click(IO.sendChatMessage);
			IO.socket.on("updateusers", IO.updateUserList);
			
			IO.socket.on("connect", function()
			{
				IO.socket.emit("adduser", IO.name);
			});
		
			IO.socket.on("disconnect", function()
			{
				IO.socket.emit("removeuser");
			});

			IO.input.keypress(function(e)
			{
				if(e.which == 13)
				{
					IO.sendChatMessage();
				}
			});

		},
		updateUserList: function(data)
		{	
			IO.userlistbox.html("");
			for (var i=0; i < data.length; i++)
			{
				IO.userlistbox.append("<li>"+data[i].name+"</li>");
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
			IO.input.val("");
		}

	};

/**
 * .select2Buttons - Convert standard html select into button like elements
 *
 * Version: 1.0.1
 * Updated: 2011-04-14
 *
 *  Provides an alternative look and feel for HTML select buttons, inspired by threadless.com
 *
 * Author: Sam Cavenagh (cavenaghweb@hotmail.com)
 * Doco and Source: https://github.com/o-sam-o/jquery.select2Buttons
 *
 * Licensed under the MIT
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
