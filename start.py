#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

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

class Game(object):
    cycle=0
    userList = {}
    roleList=[]

    def __init__(self, waiters):
        self.waiters = waiters
        self.compileRoleList()
        self.giveRoles()

    def __str__(self):
        return ("cycle: ", cycle, " - UserList: ", userList)

    def compileRoleList(self):
        count=0
        length = len(self.waiters)
        print("waiters/players: ", length)
        mafias = length/3.5
        benign=0
        hostile=0
        evil=0
        if (length >= 11):
            hostile = 1
        if (length >= 7):
            benign = 1
        if (length >= 14):
            evil = 1
        towns = length-(benign+hostile+mafias)
        for user in self.waiters:
            count += 1

            #add another random class, some method
            # calculate how many mafia, town etc, and random between roles
            if mafias > 0:
                self.roleList.append("Mafia Role")
                mafias -= 1
            elif hostile > 0:
                self.roleList.append("Hostile Role")
                hostile -= 1
            elif benign > 0:
                self.roleList.append("Benign Role")
                benign -= 1
            elif evil > 0:
                self.roleList.append("Evil Role")
                evil -= 1
            elif towns > 0:
                self.roleList.append("Town Role")
                towns -= 1

        print(self.roleList)

    def giveRoles(self):
        count=0
        currentLen = len(self.waiters)
        if len(self.waiters)!=len(self.roleList):
            print("WTF len(waiters!=len(self.roleList)!!!? Why not the same?")
        for user in self.waiters:
            count+=1
            roleNo = randint(0,currentLen-count)
            self.userList[user]=self.roleList[roleNo]
            #self.roleList.remove(self.roleList[roleNo])
            del self.roleList[roleNo]
        print(self.userList)

class Role(object):
    number=0
    align="NoAlignYetForThisRole"
    healed=False
    jailed=False
    abilityNight=False
    abilityAvail=False
    immune=False
    sheriffMess = "Does not have sheriff Message yet."
    investMess = "Does not have investigator Message yet."
    isAlive = True
    LW = "Insert Last Will here."
    name="NoNameYetForThisRole" #always override

    def __init__(self, user):
       self.user=user

    def setLW(self, newLW):
        self.LW=newLW

    def useAbility(self, target):
        #override
        pass

    def getLW(self ):
        return self.LW

    def __str__(self):
     return self.name

class Doctor(Role):
    name="Doctor"

class Godfather(Role):
    name="Godfather"

class Sheriff(Role):
    name="Godfather"

class RoomSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self):
        pass

    def open(self):
        self.players.append(self)

    def on_close(self):
        self.players.remove(self)

    def on_message(self, message):
        logging.info("mess:%r", message)
        parsed = tornado.escape.json_decode(message)
        if parsed["body"] is None or len(parsed["body"])<1:     #avoids printing empty messages
            return
        else:
            chat = {
            "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
            "body": parsed["body"],
            "nameId": (" %s says " % parsed["name"]),
            }
            #chat["html"] = tornado.escape.to_basestring(self.render_string("message.html", message=chat))
            for player in self.players:
                try:
                    player.write_message(chat)
                except:
                    logging.error("Error sending message", exc_info=True)

class Room(object):
    players = []
    game = "GameNotStarted"


    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def startGame(self):
        game = Game(self.players)

    def __init__(self):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
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
        self.render("index.html", messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()     #class field
    cache = []          #class field
    cache_size = 30     #class field        #hvor mange linjer/beskeder den skal huske/printe når en ny person joiner
    rooms = []          
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
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD? Bliver brugt som id for HTML "objektet"
        "body": parsed["body"],
        "nameId": (" %s says " % parsed["name"]),
        }
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)            
        ChatSocketHandler.send_updates(chat)

    def targetMethod(self, parsed):
        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
        "body": parsed["body"],
        "nameId": (" %s targets " % parsed["name"]),
        }
        chat["html"] = tornado.escape.to_basestring(
        self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def newroom(self, parsed):
        room = Room()
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

    def getRole(self, parsed):

        
        logging.info(type(self.room.game) is str)
         #hvorfor FUCK!!? er game i room en string?

        index = self.room.players.index(self)   #get index of 'this player' in the room
        logging.info("INDEX: ", index)
        role = self.room.game.roleList[index]        
                        # get role description instead, and show it as text instead

        chat = {
        "id": str(uuid.uuid4()),        #Hvad skal vi bruge det lort til? Får error hvis man fjerner det...wtf bliver ikke brugt xD?
        "body": parsed["body"],
        "nameId": (">Role< %s has role: %s" % (parsed["name"], role.name))
        }
        
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
            room = ChatSocketHandler.rooms[0] #input from
            room.startGame()

            chat = {
            "id": str(uuid.uuid4()),       # Hvad skal vi bruge det lort til?
            "body": "Game has started!",
            "nameId": "Game",
            }
            chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))
            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_updates(chat)

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



