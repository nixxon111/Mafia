from random import randint

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
    game = "GameNotStarted"


    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def startGame(self):
        game = Game(self.players)

    def __init__(self):
        pass