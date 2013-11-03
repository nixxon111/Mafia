var io;
var gameSocket;

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
}


function addUserToChat(name)
{
	var usernames = {}
	gameSocket.user = name;
	usernames[name] = name;
	gameSocket.emit("updatechat",{user : "SERVER" , message : "you have connected"});
	gameSocket.broadcast.emit("updatechat", {user : "SERVER", message : name+" has connected"});
	
}