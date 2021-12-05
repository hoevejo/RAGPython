import sys;

class Process:
    def __init__(self, numR):
        self.hold = [0 for _ in numR]
        self.wait = [0 for _ in numR]

    def request(self,r, n, w):
        self.hold[r] += n
        self.wait[r] += w

    def release(self, r, n):
        self.hold[r] -= n


    def waitRequest(self, r, a):
        n = self.wait[r]
        self.wait[r] = 0
        if(n < a):
            w = 0
        else: 
            w = n - a
            n = n - w
        self.request(r, n, w)

       
        
class ResourceManager:

    def __init__(self, file_name):
        self.step = 0
        self.numberProcesses = 0
        self.numberResources = 0
        self.processList = []
        self.resourceValues = []
        self.priorityLists = []
        self.statementList = []
        self.isDeadlock = False
        self.blocked = []
        self.finished = []
         
        
        self.read_input(file_name)
    

    def read_input(self, file_name):
         with open(file_name, "r") as f:
            lines = f.readlines()
            self.numberProcesses = int(lines[0].split(" ")[0])
            print(self.numberProcesses)
            self.numberResources = int(lines[1].split(" ")[0])
            print(self.numberResources)
            for x in range (0, self.numberResources):
                self.resourceValues.append(int(lines[2].split(" ")[x]))
                
            self.priorityLists = [[] for _ in self.numberResources]
            print(self.resourceValues)
            
            
            for x in range(3, len(lines)):
                self.statementList.append(lines[x])
            print(self.statementList)
            for _ in range(self.numberProcesses):
                self.processList.append((Process(self.numberResources))) 
                self.finished.append(False) 
                self.blocked.append(False)
            
            f.close()
            self.simulate()
    

    def simulate(self):
        while self.step < len(self.statementList):
            self.parse_statement()
        
            self.step += 1
            if(self.isDeadlock == True):
                self.step = len(self.statementList)
                break
        sum1 = 0
        for x in range(0, self.numberProcesses):
            sum1 += sum(self.processList[x].hold)
            if(sum1 > 0):
                self.isDeadlock = True
                self.shutdown_prompt()
                break
        
            sum1 = 0 
        print(self.blocked)   
        if(self.isDeadlock == False):
            self.end_prompt()

    def parse_statement(self):
        statement = self.statementList[self.step].split(" ")

        keyword = statement[0]
        p = int(statement[1])
        r = int(statement[2])
        n = int(statement[3])
        print(keyword)
        print(p)
        print(r)
        print(n)
        if(keyword == 'request'):
            if(n < self.resourceValues[r]):
                self.processList[p].request(r, n, 0)
                self.check_deadlockRQ()
                
            else:
                w = n - self.resourceValues[r]
                n = n - w
                self.processList[p].request(r, n, w)
                self.priorityLists[r].append(p)
                self.check_deadlockRQ()
                

        if(keyword == 'release'):
            self.processList[p].release(r,n)
            self.resourceValues[r] += n
            if(len(self.priorityLists[r]) != 0):
                print(self.resourceValues[r])
                self.processList[self.priorityLists[r][0]].waitRequest(r, self.resourceValues[r])
                self.priorityLists[r].pop(0)
            self.check_deadlockRL()
    

    def check_deadlockRQ(self):
        sum1 = 0
        for x in range(0, self.numberProcesses):
            sum1 += sum(self.processList[x].wait)
            if(sum1 > 0):
                self.blocked[x] = True
            else:
                self.blocked[x] = False
            sum1 = 0
        print(self.blocked)
        flag = not any(self.blocked)
        if(flag == True):
            self.isDeadlock = False
            print("Not all processes are blocked")
        else:
            self.isDeadlock = True
            self.step = len(self.statementList)
            print("System is in deadlock")

        


        
    def check_deadlockRL(self): 
        print("YOOOOOOOOOOOOOOOOOOOO") 

    def shutdown_prompt(self):
        # If this is the final drawing, give the user a chance to view final graph before closing
        if self.step == len(self.statementList):
            print("System is in deadlock")

    def end_prompt(self):
        print("System is deadlock free")

    

        


if __name__ == '__main__':
    if len(sys.argv) == 2:
        ResourceManager(sys.argv[1]).simulate()
    else:
        print("Please enter a valid input file")


    

