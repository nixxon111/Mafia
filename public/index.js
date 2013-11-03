$(document).ready(function()
{
	IO.init();
});

	var IO =
	{
		init: function()
		{
			IO.socket = io.connect("http://localhost:8000", 
			{
			"sync disconnect on unload" : true
			});
		IO.messages = [];
		IO.input = $("#chatinput");
		IO.sendButton = $("#sendButton");
		IO.chatwindow = $("#chatwindow");
		IO.userlistbox = $("#userList");
		IO.name = prompt("what's your name?");
		
		IO.socket.on("updatechat", function(data)
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
		});
		
		IO.socket.on("updateusers", function(data)
		{
			IO.userlistbox.html("");
			for (var key in data)
			{
				IO.userlistbox.append("<li>"+data[key]+"</li>");
			}
		});

		IO.sendButton.click(IO.sendChatMessage);

		IO.input.keyup(function(e){
		if(e.keycode == 13){
			IO.sendChatMessage();
		}
		});
		IO.socket.on("connect", function()
		{
			IO.socket.emit("adduser", IO.name);
		});
		
		IO.socket.on("disconnect", function()
		{
			IO.socket.emit("removeuser", IO.socket.id);
		});
	},

		sendChatMessage: function()
		{
			var messagetext = IO.input.val();
			IO.socket.emit("updatechat", { user: IO.name, message: messagetext});
			IO.input.val("");
		}

	};