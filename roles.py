from random import randint
import logging

class Game(object):
    cycle=0
    userList = {}

    def __init__(self, players):
        roleList = self.compileRoleList(players)
        self.giveRoles(players, roleList)

    def __str__(self):
        return ("cycle: ", cycle, " - UserList: ", userList)

    def compileRoleList(self, players):     #take len(players instead? faster?)
        count=0
        length = len(players)
        mafias = length/3.5
        benign=0
        hostile=0
        evil=0
        roleList = []
        mafiaRoles = [] ### ADD HERE TO GIVE RANDOM ROLES maybe? take from array?

        if (length >= 11):
            hostile = 1
        if (length >= 7):
            benign = 1
        if (length >= 14):
            evil = 1
        towns = length-(benign+hostile+mafias)
        for user in players:
            count += 1

            #add another random class, some method
            # calculate how many mafia, town etc, and random between roles


            if mafias > 0:
                roleList.append(Godfather())
                mafias -= 1
            elif hostile > 0:
                roleList.append("Hostile Role")
                hostile -= 1
            elif benign > 0:
                roleList.append("Benign Role")
                benign -= 1
            elif evil > 0:
                roleList.append("Evil Role")
                evil -= 1
            elif towns > 0:
                roleList.append(Doctor())
                towns -= 1

        logging.info(roleList)
        return roleList
        


    def giveRoles(self, players, roleList):
        currentLen = len(players)
        if len(players)!=len(roleList):
            print("WTF len(waiters!=len(self.roleList)!!!? Why not the same?")
        for user in players:
            #if len(roleList) == 0:
            #    roleNo = 0
            #else:
            roleNo = randint(0,len(roleList)-1)         #stupid randrange OR randint cannot random from 0 to 0. 
            self.userList[user]=roleList[roleNo]
            #self.roleList.remove(self.roleList[roleNo])
            del roleList[roleNo]
        print(self.userList)

class Role(object):
    number=0
    align="NoAlignYetForThisRole"
    healed=False
    jailed=False
    abilityNight=False      #not needed?
    abilityAvail=False      #not needed?
    immune=False
    sheriffMess = "Does not have sheriff Message yet."
    investMess = "Does not have investigator Message yet."
    isAlive = True
    LW = "Insert Last Will here."
    name="NoNameYetForThisRole" #always override

    def __init__(self):
        logging.info("I AM role: %s" % self.name) #nothing in constr?

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
    align="Town"

class Godfather(Role):
    name="Godfather"
    align="Mafia"       #enums exist in python? Or maybe create constants in class.Role for safety?

class Sheriff(Role):
    name="Sheriff"
    align="Town"

'''
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
'''

class Room(object):
    players = []
    game = None
    #game = "GameNotStarted"


    def addPlayer(self, player):
        self.players.append(player)
        index = self.players.index(player)   #get index of 'this player' in the room
        logging.info("INDEX: %s" % index)

    def removePlayer(self, player):
        self.players.remove(player)

    def startGame(self):
        if self.game is None:
            self.game = Game(self.players)
        else:
            logging.info("Game alrdy started")
        

    def __init__(self):
        pass