var io;
var gameSocket;
var usernames = {};
exports.init = function(_io, _socket)
{
	io = _io;
	gameSocket = _socket;

	gameSocket.emit("updatechat", {user: "SERVER",message: "welcome to the chat"});

	gameSocket.on("updatechat", function(data) 
	{
		io.sockets.emit("updatechat", data);
	})
	gameSocket.on("adduser", function(name)
	{
		addUserToChat(name);
	})
	gameSocket.on("removeuser", function(id)
	{
		removeUserFromChat(id);
	})
}


addUserToChat = function(name)
{
	usernames[gameSocket.id] = name;
	gameSocket.emit("updatechat",{user : "SERVER" , message : "you have connected"});
	gameSocket.broadcast.emit("updatechat", {user : "SERVER", message : name+" has connected"});
	gameSocket.emit("updateusers", usernames);
	gameSocket.broadcast.emit("updateusers", usernames);
}

removeUserFromChat = function(id)
{
	var name = usernames.id;
	gameSocket.broadcast.emit("updatechat", {user : "SERVER", message : name+" has disconnected"});
	gameSocket.emit("updateusers", usernames);
	gameSocket.broadcast.emit("updateusers", usernames);
}