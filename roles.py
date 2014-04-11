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
    name=""

    def __str__(self):
     return str(self.name)

class Doctor(object):
    name="Doctor"

class Godfather(object):
    name="Godfather"