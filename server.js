var express = require("express");

var path = require("path");

var app = express();

var mafia = require("./mafia");

app.configure( function()
{
	app.use(express.logger("test"));
	app.use(express.static(path.join(__dirname, "public")));
});

var server = require("http").createServer(app).listen(80);

var io = require("socket.io").listen(server);

io.sockets.on("connection", function(socket)
{
	mafia.init(io, socket);
})