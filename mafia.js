var io;
var gameSocket;

exports.init = function(_io, _socket)
{
	io = _io;
	gameSocket = _socket;
	gameSocket.emit("message", {message: "welcome to the chat"});
	gameSocket.on("send", function(data) 
	{
		io.sockets.emit("message", data);
	})
}