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
import random
import roles

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Game(object):
    cycle=0
    userList = {}
    roleList=[]


    def __init__(self, waiters):
        self.waiters = waiters
        self.compileRoleList()
        self.giveRoles(waiters)

    def compileRoleList(self):
        count=0
        for user in self.waiters:
            count+=1
            #add another random class, some method
            # calculate how many mafia, town etc, and random between roles
            if (count==1):
                self.roleList.append(Doctor())
            elif (count==2):
                self.roleList.append(Godfather())
            else:
                self.roleList.append("I am some role %s <--" % count)
        print(self.roleList)

    def giveRoles(self, waiters):
        count=0
        for user in waiters:
            count+=1
            print("player: ", count)
            self.userList[user]=self.roleList[count-1]
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


class Doctor(object):
    name="Doctor"

class Godfather(object):
    name="Godfather"

'''
                                TORNADO STARTS HERE!!       TORNADO STARTS HERE!!       TORNADO STARTS HERE!!       TORNADO STARTS HERE!!       TORNADO STARTS HERE!!
'''

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
    waiters = set()
    cache = []
    cache_size = 200

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

    def on_message(self, message):
        logging.info("mess:%r", message)
        parsed = tornado.escape.json_decode(message)
        if (parsed["body"]=="start"): 
            chat = {
            "id": str(uuid.uuid4()),
            "body": "Game has begun",
            }
            chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))
            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_updates(chat)
            game = Game(ChatSocketHandler.waiters)
        else:
            chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }

        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


def getPlayersInChat(): #static method, no self...ok?
        return ChatSocketHandler.getPlayers()


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

