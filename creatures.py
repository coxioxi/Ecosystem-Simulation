import turtle
import random

class World:
    
    def getPlantCount(self):
        return self.__plantsCount
    
    def getBearCount(self):
        return self.__bearCount
    
    def getFishCount(self):
        return self.__fishCount
    
    def setFishCount(self, count):
        self.__fishCount = count
    
    def setBearCount(self, count):
        self.__bearCount = count
    
    def setPlantCount(self, count):
        self.__plantsCount = count

    def __init__(self, mx, my):
        self.maxX = mx
        self.maxY = my
        self.thingList = []
        self.grid = []
        self.__bearCount = 0
        self.__fishCount = 0
        self.__plantsCount = 0
    
        for arow in range(self.maxY):     
            row = []
            for acol in range(self.maxX):
                row.append(None)
            self.grid.append(row)        
    
        self.wturtle = turtle.Turtle()
        self.wscreen = turtle.Screen()
        self.wscreen.setworldcoordinates(0,0,self.maxX-1,self.maxY-1)   
        self.wscreen.addshape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Bear.gif")
        self.wscreen.addshape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Fish.gif")
        self.wscreen.addshape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Plant.gif")
        self.wturtle.hideturtle()               

    def draw(self):
        self.wscreen.tracer(0)
        self.wturtle.forward(self.maxX-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxX-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY-1)
        self.wturtle.left(90)    
        for i in range(self.maxY-1):
            self.wturtle.forward(self.maxX-1)
            self.wturtle.backward(self.maxX-1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wturtle.forward(1)
        self.wturtle.right(90)
        for i in range(self.maxX-2):
            self.wturtle.forward(self.maxY-1)
            self.wturtle.backward(self.maxY-1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wscreen.tracer(1)
        
    def freezeWorld(self):
        self.wscreen.exitonclick()
        
    def addThing(self, athing, x, y):   
        athing.setX(x)
        athing.setY(y)
        self.grid[y][x] = athing        
        athing.setWorld(self)
        self.thingList.append(athing)   
        athing.appear()       
        if isinstance(athing, Bear):
            self.__bearCount += 1
        elif isinstance(athing, Fish):
            self.__fishCount += 1
        else:
            self.__plantsCount += 1
    
    def delThing(self,athing):
        athing.hide()                                     
        self.grid[athing.getY()][athing.getX()] = None     
        self.thingList.remove(athing)  
        if isinstance(athing, Bear):
            self.__bearCount -= 1
        elif isinstance(athing, Fish):
            self.__fishCount -= 1
        else:
            self.__plantsCount -= 1                    
    
    def moveThing(self,oldx,oldy,newx,newy):
        self.grid[newy][newx] = self.grid[oldy][oldx]
        self.grid[oldy][oldx] = None
    
    def getMaxX(self):
        return self.maxX
    
    def getMaxY(self):
        return self.maxY
    
    def shuffle(self,athingList):
        for i in range(len(athingList)):
            randomIndex = random.randint(0,len(athingList)-1)
            athingList[i], athingList[randomIndex] = athingList[randomIndex], athingList[i]
        return athingList

    def liveALittle(self):      
        self.thingList = self.shuffle(self.thingList)                         
        if self.thingList != [ ]:
           athing = random.randrange(len(self.thingList))    
           randomthing = self.thingList[athing]              
           randomthing.liveALittle(0.06)                       
     
    def emptyLocation(self,x,y):
        if self.grid[y][x] == None:
            return True
        else:
            return False
        
    def lookAtLocation(self,x,y):
       return self.grid[y][x]

class Creature:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()

        self.xpos = 0
        self.ypos = 0
        self.world = None                 
        
        self.breedTick = 0
        self.offsetList = [(-1,1) ,(0,1) ,(1,1),          
                           (-1,0)        ,(1,0),
                           (-1,-1),(0,-1),(1,-1)]

    def setX(self,newx):
        self.xpos = newx
    
    def setY(self,newy):
        self.ypos = newy
    
    def getX(self):
        return self.xpos
    
    def getY(self):
        return self.ypos
    
    def setWorld(self,aworld):
        self.world = aworld
 
    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()
    
    def move(self,newx,newy):
        self.world.moveThing(self.xpos,self.ypos,newx,newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def liveALittle(self, probability):
        pass

    def tryToBreed(self, LifeForm):
        self.offsetList    
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextx = self.xpos + randomOffset[0]
        nexty = self.ypos + randomOffset[1]
        while not (0 <= nextx < self.world.getMaxX() and 
                   0 <= nexty < self.world.getMaxY()):  
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
    
        if self.world.emptyLocation(nextx,nexty):    
           childThing = LifeForm()
           self.world.addThing(childThing,nextx,nexty)
           self.breedTick = 0

    def tryToMove(self):
        self.offsetList
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextx = self.xpos + randomOffset[0]
        nexty = self.ypos + randomOffset[1]
        while not(0 <= nextx < self.world.getMaxX() and 
                  0 <= nexty < self.world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]
    
        if self.world.emptyLocation(nextx,nexty):
           self.move(nextx,nexty)
           
    def tryToEat(self, prey):
        self.offsetList
        adjprey = []                 
        for offset in self.offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx,newy)) and isinstance(self.world.lookAtLocation(newx,newy), prey):
                    adjprey.append(self.world.lookAtLocation(newx,newy))       
                
        if len(adjprey)>0:                
            randomprey = adjprey[random.randrange(len(adjprey))]   
            preyx = randomprey.getX()
            preyy = randomprey.getY()
        
            self.world.delThing(randomprey)                            
            self.move(preyx,preyy)                                      
            self.starveTick = 0                     
        else:
            self.starveTick = self.starveTick + 1  

        
class Fish(Creature):
    def __init__(self):
        super().__init__()
        self.turtle.shape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Fish.gif")
        self.starveTick = 0
        self.maxPop = random.randint(3,4)
        self.breedPoint = random.randint(6,12)
        self.starvePoint = random.randint(6,12)
        
    
    def liveALittle(self, probability):
        if probability <= random.random():
            self.offsetList   
            adjfish = 0                                  
            for offset in self.offsetList:                    
                newx = self.xpos + offset[0]             
                newy = self.ypos + offset[1]
                if 0 <= newx < self.world.getMaxX()  and  0 <= newy < self.world.getMaxY():          
                    if (not self.world.emptyLocation(newx,newy)) and isinstance(self.world.lookAtLocation(newx,newy),Fish):
                        adjfish = adjfish + 1
                        
            self.tryToEat(Plant)          

            if adjfish >= self.maxPop or self.starveTick >= self.starvePoint:                   
                self.world.delThing(self)      
            else:
                self.breedTick = self.breedTick + 1
                if self.breedTick >= self.breedPoint:
                    self.tryToBreed(Fish)

                self.tryToMove()

class Bear(Creature):
    def __init__(self):
        super().__init__()
        self.turtle.shape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Bear.gif")
        self.starveTick = 0
        self.breedPoint = random.randint(7,8)
        self.starvationPoint = random.randint(6,10)

    def liveALittle(self, probability):
        if probability <= random.random():
            self.breedTick = self.breedTick + 1
            if self.breedTick >= self.breedPoint:
                self.tryToBreed(Bear)
        
            self.tryToEat(Fish)          
        
            if self.starveTick == self.starvationPoint:
                self.world.delThing(self)
            else:
                self.tryToMove()

            
class Plant(Creature):
    def __init__(self):
        super().__init__()
        self.turtle.shape("C:\\Users\\samuk\\Desktop\\Python\\Lab10\\Plant.gif")
        self.breedPoint = random.randint(6,15)

    def liveALittle(self, probability):
            if probability <= random.random():
                self.breedTick = self.breedTick + 1
                if self.breedTick >= self.breedPoint:
                    self.tryToBreed(Plant)

def mainSimulation():
    numberOfBears = 4
    numberOfFish = 8
    numberOfPlants = 16
    worldLifeTime = 2500
    worldWidth = 15
    worldHeight = 15
    
    myworld = World(worldWidth,worldHeight)      
    myworld.draw()                               
    
    for i in range(numberOfFish):  
        newfish = Fish()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newfish,x,y)        
    
    for i in range(numberOfBears):   
        newbear = Bear()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):   
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newbear,x,y)    
        
    for i in range(numberOfPlants):   
        newplant = Plant()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):   
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newplant,x,y)      
    
    for i in range(worldLifeTime):     
        myworld.liveALittle()          
    
    myworld.freezeWorld()          

mainSimulation()
