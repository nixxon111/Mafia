$(document).ready(function()
{
	initChatWindow();
});

function initChatWindow()
{
	var messages = [];
	var socket = io.connect("http://localhost:80");
	var input = $("#input");
	var sendButton = $("#sendButton");
	var chatwindow = $("#chatwindow");

	socket.on("message", function(data)
	{	
		if (data.message)
		{
			messages.push(data.message);
			var html = "";
			for (var i = 0; i < messages.length; i++)
			{
				html += messages[i] + "<br/>";
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
		socket.emit("send", { message: messagetext});
	});

};