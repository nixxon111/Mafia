import random
import logging

class Game(object):
    cycle=0
    userList = {}

    def __init__(self, players):
        roleList = self.compileRoleList(players)
        self.giveRoles(players, roleList)

    def __str__(self):
        return ("cycle: ", cycle, " - UserList: ", userList)

    def compileRoleList(self, players):
        length = len(players)
        mafias = length/3.5
        numberofbenign=0
        numberofhostile=0
        numberofevil=0
        factory = RoleFactory.getInstance()

        if (length >= 14):
            numberofevil = 1
        if (length >= 11):
            numberofhostile = 1
        if (length >= 7):
            numberofbenign = 1

        towns = length-(benign+hostile+mafias)

        if hostile > 0:
            roleList.append(Serialkiller()) #randomHostile()
            hostile -= 1
        if evil > 0:
            roleList.append(Arsonist()) #randomEvil()
            evil -= 1
        if benign > 0:
            roleList.append(Survivor()) #randomBenign
            benign -= 1


        while (mafias > 0):
            roleList.append(factory.createMafiaRole())
            mafias -= 1
        while (towns > 0):
            roleList.append(factory.createTownRole())
            towns -= 1

        if len(roleList) != len(players):
            logging.info("len(roleList) != len(players) NOT GOOD, roles.py: ~63+")
                
        logging.info(roleList)
        return roleList
        


    def giveRoles(self, players, roleList):
        currentLen = len(players)
        if len(players)!=len(roleList):
            print("WTF len(waiters!=len(self.roleList)!!!? Why not the same?")
        for user in players:
            role = choice(roleList)      
            self.userList[user] = role
            roleList.remove(role)  
        print(self.userList)

class Role(object):
    number=0
    alignment="NoalignmentYetForThisRole"
    healed=False
    jailed=False
    abilityNight=False      #not needed?
    abilityAvail=False      #not needed?
    immune=False
    sherifMessage = "Does not have sheriff Message yet."
    investigatorMessage = "Does not have investigator Message yet."
    isAlive = True
    lastWill = "Insert Last Will here."
    name="NoNameYetForThisRole" #alastWillays override

    def __init__(self):
        pass

    def setlastWill(self, newlastWill):
        self.lastWill=newlastWill

    def useAbility(self, target):
        #override
        pass

    def getlastWill(self):
        return self.lastWill

    def __str__(self):
     return self.name

        ########### TOWN ROLES

class Doctor(Role):
    name="Doctor"
    alignment="Town"

class Sheriff(Role):
    name="Sheriff"
    alignment="Town"
class Investigator(Role):
    name="Investigator"
    alignment="Town"
            ########### HOSTILE ROLES

class Serialkiller(Role):
    name="Serialkiller"
    alignment="Neutral"

        ########### BENIGN ROLES

class Survivor(Role):
    name="Survivor"
    alignment="Neutral"

        ########### MAFIA ROLES

class Godfather(Role):
    name="Godfather"
    alignment="Mafia"       #enums exist in python? Or maybe create constants in class.Role for safety?

class Beguiler(Role):
    name="Beguiler"
    alignment="Mafia"  

class Disguiser(Role):
    name="Disguiser"
    alignment="Mafia"

class Framer(Role):
    name="Framer"
    alignment="Mafia"

class Janitor(Role):
    name="janitor"
    alignment="Mafia"

class Room(object):
    number = 0
    maxplayers = 15
    def __init__(self):
        self.players = []
        self.game = None
        self.number = Room.number
        Room.number += 1
        
    def __repr__(self):
        return "room number: "+str(self.number)+", players: "+str(len(self.players))+"/"+str(Room.maxplayers)

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

# lazy-loaded singleton
def singleton(cls):
    instances = {}
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getInstance()

@singleton
class RoleFactory(object):
    random.seed()
    sortedTownsList = [Sheriff(), Doctor(), Investigator()]
    sortedMafiaList = [Godfather(), Beguiler(), Disguiser()]
    mafiaDeceptionList = []
    BenignList = []
    HostileList = []
    def createRandomMafiaDeceptionRole():
        return random.choice(mafiaDeceptionList).clone()

    def createSortedTownRole():
        for townie in sortedTownsList:
            yield townie.clone()

    def createSortedMafiaRole():
        for mafia in sortedMafiaList:
            yield mafia.clone()

    def createRandomBenignRole():
        return random.choice(BenignList).clone()

    def createRandomHostileRole():
        return random.choice(HostileList).clone()