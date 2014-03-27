var io;
var gameSocket;
var usernames = [];
exports.init = function(_io, _socket)
{
	io = _io;
	gameSocket = _socket;

	gameSocket.emit("updatechat", {user: "SERVER",message: "welcome to the chat"});

	gameSocket.on("updatechat", function(data) 
	{
		io.sockets.emit("updatechat", data);
	});
	gameSocket.on("adduser", function(name)
	{
		addUserToChat(name);
	});
	gameSocket.on("removeuser", function(name)
	{
		removeUserFromChat(name);
	});
	gameSocket.on("disconnect", function(name) 
	{
		removeUserFromChat(name);
  	});
}


addUserToChat = function(name)
{
	usernames.push({id: gameSocket.id, name : name});;
	gameSocket.emit("updatechat",{user : "SERVER" , message : "you have connected"});
	io.sockets.emit("updatechat", {user : "SERVER", message : name+" has connected"});
	gameSocket.emit("updateusers", usernames);
	io.sockets.emit("updateusers", usernames);
}

removeUserFromChat = function()
{
	io.sockets.emit("updatechat", {user : "SERVER", message : usernames[gameSocket.id]+" has disconnected"});
	for (var i = 0, len=usernames.length; i<len; i++)
	{
		var c = usernames[i]
		if (c.id == gameSocket.id)
		{
			usernames.splice(i,1);
			break;
		}
	}
	gameSocket.emit("updateusers", usernames);
	io.sockets.emit("updateusers", usernames);
}