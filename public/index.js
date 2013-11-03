$(document).ready(function()
{
	var socket = io.connect("http://localhost:8000");
	var name = prompt("what's your name?");
	socket.on("connect", function()
	{
		socket.emit("adduser", name);
	});
	initChatWindow(name, socket);
});


function initChatWindow(name, socket)
{
	var messages = [];
	var input = $("#input");
	var sendButton = $("#sendButton");
	var chatwindow = $("#chatwindow");

	socket.on("updatechat", function(data)
	{	
		if (data.message)
		{
			messages.push({user : data.user, message : data.message});
			var html = "";
			for (var i = 0; i < messages.length; i++)
			{
				html += messages[i].user +": "+messages[i].message + "<br/>";
			}
			chatwindow.html(html);
		}
		else 
		{
			console.log("invalid data received");
		}
	});
	
	sendButton.click(function()
	{
		var messagetext = input.val();
		socket.emit("updatechat", { user: name, message: messagetext});
	});

};
