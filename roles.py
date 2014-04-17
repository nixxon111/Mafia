import random
import logging
import copy
from math import ceil

class Game(object):

    def __init__(self, players):
        self.userList = {}
        self.playerList = []
        self.cycle = 0
        roleList = self.setup1(players)
        self.giveRoles(players, roleList)

    def __str__(self):
        return ("cycle: ", cycle, " - UserList: ", userList)

    def setup1(self, players):
        #sheriff, investigator, core, doctor, invest, power, protect, core, killing, 
        #GODFATHER, support, deception, 
        #benign, hostile, COMPLETELY RANDOM (non mafia.?)
        roleList = []
        length = len(players)

        mafias = int(ceil(length/5))
        if (length >= 7):
            roleList.append(Survivor()) #randomBenign
            length -= 1
            if (length >= 10):  #11th player
                roleList.append(Serialkiller()) #randomHostile()
                length -= 1
                if (length >= 1):  #14th player
                    roleList.append(RoleFactory.RandomNoneMafia())
                    length -= 1
                    
        mafias = int(ceil(length/5)) # one more mafia at 1st, 6th and 13th player
        towns = length-(mafias)

        if (mafias >= 1):
            roleList.append(Godfather())
            if (mafias >= 2):
                roleList.append(RoleFactory.createRandomMafiaDeceptionRole())
                if (mafias >= 3):
                    roleList.append(RoleFactory.createRandomMafiaDeceptionRole())   #mafiaSupport()
        '''
        mafiagenerator = factory.createSortedMafiaRole()
        while (mafias > 0):
            roleList.append(next(mafiagenerator))
            mafias -= 1
        '''
        towngenerator = RoleFactory.createSortedTownRole()
        while (towns > 0):
            roleList.append(next(towngenerator))
            towns -= 1

        if len(roleList) != len(players):
            logging.info("len(roleList) != len(players) NOT GOOD, roles.py: ~45+")
                
        logging.info(roleList)
        return roleList
        


    def giveRoles(self, players, roleList):
        currentLen = len(players)
        if len(players)!=len(roleList):
            print("WTF len(waiters!=len(self.roleList)!!!? Why not the same?")
        for user in players:
            role = random.choice(roleList)      
            self.userList[user] = role
            roleList.remove(role)
            self.playerList.append(user)

        print(self.userList)

class Role(object):
    MAFIA = "Mafia"
    TOWN = "Town"
    NEUTRAL = "Unaligned"

    def __init__(self):
        self.alignment="NoalignmentYetForThisRole"
        self.healed=False
        self.jailed=False
        self.immune=False
        self.sherifMessage = "Does not have sheriff Message yet."
        self.investigatorMessage = "Does not have investigator Message yet."
        self.isAlive = True
        self.lastWill = "Insert Last Will here."
        self.name="NoNameYetForThisRole" #alastWillays override

    def setlastWill(self, newlastWill):
        self.lastWill=newlastWill

    def useAbility(self, target):
        #override
        logging.info("THIS role: %s does not have ABILITY implemented yet" % self.name)
        pass

    def getlastWill(self):
        return self.lastWill

    def __str__(self):
     return self.name

        ########### TOWN ROLES

class Doctor(Role):
    def __init__(self):
        self.name="Doctor"
        self.alignment=Role.TOWN

class Sheriff(Role):
    def __init__(self):
        self.name="Sheriff"
        self.alignment=Role.TOWN
    
class Investigator(Role):
    def __init__(self):
        self.name="Investigator"
        self.alignment=Role.TOWN
            ########### HOSTILE ROLES

class Serialkiller(Role):
    def __init__(self):
        self.name="Serialkiller"
        self.alignment=Role.NEUTRAL

class Arsonist(Role):
    def __init__(self):
        self.name="Arsonist"
        self.alignment=Role.NEUTRAL

        ########### BENIGN ROLES

class Survivor(Role):
    def __init__(self):
        self.name="Survivor"
        self.alignment=Role.NEUTRAL

        ########### MAFIA ROLES

class Godfather(Role):
    def __init__(self):
        self.name="Godfather"
        self.alignment=Role.MAFIA       #enums exist in python? Or maybe create constants in class.Role for safety?

class Beguiler(Role):
    def __init__(self):
        self.name="Beguiler"
        self.alignment=Role.MAFIA  

class Disguiser(Role):
    def __init__(self):
        self.name="Disguiser"
        self.alignment=Role.MAFIA

class Framer(Role):
    def __init__(self):
        self.name="Framer"
        self.alignment=Role.MAFIA

class Janitor(Role):
    def __init__(self):
        self.name="Janitor"
        self.alignment=Role.MAFIA

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
    def __init__(self):
        random.seed()
        self.sortedTownsList = [Sheriff(), Doctor(), Investigator()]
        self.sortedMafiaList = [Godfather()] #second be mafiaSupportList
        self.mafiaDeceptionList = [Beguiler(), Disguiser(), Framer(), Janitor()] #avoid duplicate roles?
        self.benignList = [Survivor()]
        self.hostileList = [Arsonist(), Serialkiller()]

    def createRandomMafiaDeceptionRole(self):
        return copy.copy(random.choice(self.mafiaDeceptionList))

    def createSortedTownRole(self):
        while(True):
            for townie in self.sortedTownsList:
                yield copy.copy(townie)

    def createSortedMafiaRole(self):
        while(True):
            for mafia in self.sortedMafiaList:
                yield copy.copy(mafia)

    def createRandomBenignRole(self):
        return copy.copy(random.choice(self.BenignList))

    def createRandomHostileRole(self):
        return copy.copy(random.choice(self.HostileList))

    def RandomNoneMafia(self):
        #ok that its 1/3 town, 1/3 hostile and 1/3 benign, include Mafia?
        alignmentList = random.choice([self.benignList, self.hostileList, self.sortedTownsList])
        logging.info(alignmentList)
        return copy.copy(random.choice(alignmentList))
