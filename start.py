import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from random import randint
from tornado.options import define, options
import roles

define("port", default=8888, help="run on the given port", type=int)

import tornado

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/lobby", LobbyHandler),
            (r"/chatsocket", ChatSocketHandler),
            (r"/gameroom", GameRoomHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", roomlist=ChatSocketHandler.rooms)

class LobbyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("lobby.html", messages=ChatSocketHandler.cache)

class GameRoomHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("gameroom.html")

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()     #class field
    cache = []          #class field
    cache_size = 30     #class field        #hvor mange linjer/beskeder den skal huske/printe når en ny person joiner
    rooms = []          #class field
    userId = randint(0,10)
    #room = "Is not in any room"

    @classmethod
    def getPlayers(cls): #static method, no self...ok?
        return len(cls.waiters)

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    def __str__(self):
        return str("PlayerID: %s" % self.userId)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def chatMethod(self, parsed):
        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til?? Bliver brugt som id for HTML "objektet"
        "body": parsed["body"],
        "nameId": (" %s says " % parsed["name"]),
        }
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)            
        ChatSocketHandler.send_updates(chat)

    def targetMethod(self, parsed):
        chat = {
        "id": str(uuid.uuid4()),        #Hv
        "body": parsed["body"],
        "nameId": (" %s targets " % parsed["name"]),
        }
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def newroom(self, parsed):
        room = roles.Room()
        ChatSocketHandler.rooms.append(room)    # Add a new room to the list

        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
        "body": parsed["body"],
        "nameId": (">New Room< %s creates room (RoomNo:%d) " % (parsed["name"], len(ChatSocketHandler.rooms)))
        }
        
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def join(self, parsed):
        room = ChatSocketHandler.rooms[0] #replace 0 with parsed number
        room.addPlayer(self)
        self.room = room
        #ChatSocketHandler.waiters.remove(self) # remove player from main chat as they enter a room
        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
        "body": parsed["body"],
        "nameId": (" %s joins room 1 (fixed) " % parsed["name"]),
        }
        
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        #ChatSocketHandler.update_cache(chat) #dont update cache here :O for fun
        ChatSocketHandler.send_updates(chat)

    def getRole(self, parsed):
        role = self.room.game.userList[self]
        logging.info(role)
        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
        "body": parsed["body"],
        "nameId": (">Role< %s has role: %s" % (parsed["name"], role.name))
        }
        
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def start(self, parsed):
        room = ChatSocketHandler.rooms[0] #input from
        room.startGame()
        chat = {
        "id": str(uuid.uuid4()),       # Hvad skal vi bruge det lort til?
        "body": "Game has started!",
        "nameId": "Game",
        }
        index = self.room.players.index(self)   #get index of 'this player' in the room
        logging.info("INDEX: %s" % index)
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def on_message(self, message):
        logging.info("mess:%r", message)
        parsed = tornado.escape.json_decode(message)
        if parsed["body"] is None or len(parsed["body"])<1:     #avoids printing empty messages
            return

        if parsed["body"]=="newroom":
            self.newroom(parsed);

        elif parsed["body"]=="join":
            self.join(parsed);

        elif parsed["body"]=="role":
            self.getRole(parsed);
        
        elif parsed["method"]=="target":
            self.targetMethod(parsed);

        # if "start" then start a new game and print that its started
        elif (parsed["body"]=="start"):
            self.start(parsed);

        elif parsed["method"]=="chat":
            self.chatMethod(parsed);

def getPlayersInChat(): #static method, no self...ok?
        return ChatSocketHandler.getPlayers()

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()