# ~~~~~ Untitled RPG ~~~~~
# 
# Created by: NameIsMissing
# APCSA 2023-2024
# 
# Untitled RPG is an RPG made on my own using a tilepack found online for the
# art. The game has features like an expansive map, building interiors, combat,
# enemy attacks, shop to buy items, a dungeon for enemies, a save feature,
# and much more.

# App related global variables
app.frameCount = 0          # Counting frames, used for some animations / player healing
app.stepsPerSecond = 0      # Frames per second of the app. This is set to 0 to simulate a pause, normally at 30
app.mainGradient = gradient(rgb(217, 190, 117), rgb(153, 138, 98), start = "center") # The gradient used for many of the game GUI's
app.debugVisibility = 0    # Used for debugging

# Player related global variables
app.player = None
app.playerShapes = Group()
app.swordSwing = False
app.eventId = -1

# Map related global Variables
app.map = Group()
app.signsList = []
app.signsGroup = Group()
app.inSign = False

# Global variables related to signs/points in game, used to display sign message or transport player
enterHouse = Circle(1511, 1963, 28, opacity = app.debugVisibility)      #0
exitHouse = Circle(622, 3675, 28, opacity = app.debugVisibility)        #1
enterShop = Circle(1602, 1340, 28, opacity = app.debugVisibility)       #2
exitShop = Circle(1173, 3675, 28, opacity = app.debugVisibility)        #3
shopGUI = Circle(1040, 3500, 28, opacity = app.debugVisibility)         #4
enterDungeon = Circle(226, 221, 60, opacity = app.debugVisibility)      #5
exitDungeon = Circle(3300, 1794, 28, opacity = app.debugVisibility)     #6
winDungeon = Circle(3373, 760, 40, opacity = app.debugVisibility)       #7
piggyBank = Circle(466, 3644, 28, opacity = app.debugVisibility)        #8
pondSign = Circle(756, 1794, 28, opacity = app.debugVisibility)         #9
cave = Circle(1024, 296, 28, opacity = app.debugVisibility)             #10

# Both a list and a group are used for performance reasons
app.signsGroup = Group(enterHouse, exitHouse, enterShop, exitShop, shopGUI, enterDungeon, exitDungeon, winDungeon, piggyBank, pondSign, cave)
app.signsList = [enterHouse, exitHouse, enterShop, exitShop, shopGUI, enterDungeon, exitDungeon, winDungeon, piggyBank, pondSign, cave]

# Map initialization
mapBorder = Polygon()
pond1 = Polygon()
pond2 = Polygon()
dungeonWall = Polygon()
houseWall = Polygon()
shopWall = Polygon()

oceanBG = Image("cmu://842876/31169753/water.png", 0, 0)        # Blue background
mapBG = Image("cmu://842876/31222834/rpgMapFinal.png", 0, 0)    # Map background
chest = Image("cmu://842876/31232456/chest.png", 3333, 720)     # Dungeon chest

### These points create the border of the entire map
borderPointList = [ [32, 156],    [414, 156],   [414, 220],   [1184, 220],  [1184, 285],
                    [1504, 285],  [1504, 350],  [1695, 350],  [1695, 285],  [1886, 285],
                    [1886, 220],  [2140, 220],  [2140, 0],    [0, 0],       [0, 2813],
                    [2367, 2813], [2367, 0],    [2144, 0],    [2144, 285],  [2021, 285],
                    [2021, 350],  [1955, 350],  [1955, 480],  [1891, 480],  [1891, 985],
                    [1954, 985],  [1954, 1050], [2021, 1050], [2021, 1304], [2082, 1304],
                    [2082, 1434], [2144, 1434], [2144, 1690], [2211, 1690], [2211, 1945],
                    [2275, 1945], [2275, 2200], [2340, 2200], [2340, 2465], [2275, 2465],
                    [2275, 2595], [2215, 2595], [2215, 2658], [2150, 2658], [2150, 2721],
                    [2022, 2721], [2022, 2786], [1436, 2786], [1436, 2722], [860, 2722],
                    [860, 2660],  [285, 2660],  [285, 2147],  [220, 2147],  [220, 1635],
                    [155, 1635],  [155, 1125],  [92, 1125],   [92, 612],    [32, 612]]
for point in borderPointList:
    mapBorder.addPoint(point[0], point[1])
mapBorder.opacity = app.debugVisibility
mapBorder.left = 0
mapBorder.top = 64

### Creates the border for the upper pond on the map
pond1List = [[743, 547],  [1050, 547], [1050, 609], [1115, 609], [1115, 729],
             [1053, 729], [1053, 793], [871, 793],  [871, 730],  [743, 730]]
for point in pond1List:
    pond1.addPoint(point[0], point[1])
pond1.opacity = app.debugVisibility

### Creates the border for the lower pond on the map
pond2List = [[678, 1442], [924, 1442], [924, 1625], [862, 1625], [862, 1753],
             [669, 1753], [669, 1817], [484, 1817], [484, 1508], [675, 1508]]
for point in pond2List:
    pond2.addPoint(point[0], point[1])
pond2.opacity = app.debugVisibility

### Creates the border for the dungeon on the map
dungeonWallList = [[2936, 578],  [3511, 578],  [3511, 896],  [3447, 896],  [3447, 1091],
                   [3574, 1091], [3574, 1408], [3447, 1408], [3447, 1857], [3127, 1857],
                   [3127, 1601], [2872, 1601], [2782, 898],  [2936, 898],  [2936, 644],
                   [2999, 644],  [2999, 961],  [2935, 961],  [2935, 1218], [3447, 1218],
                   [3447, 1281], [2935, 1281], [2935, 1538], [3255, 1538], [3255, 1601],
                   [3191, 1601], [3191, 1794], [3384, 1794], [3384, 1601], [3320, 1601],
                   [3320, 1538], [3384, 1538], [3384, 1346], [3512, 1346], [3512, 1153],
                   [3384, 1153], [3384, 961],  [3128, 961],  [3128, 834],  [3448, 834],
                   [3448, 641],  [2936, 641]]
for point in dungeonWallList:
    dungeonWall.addPoint(point[0], point[1])
dungeonWall.opacity = app.debugVisibility

### Creates the border for the player house    
houseList = [[412, 3404], [699, 3404], [699, 3691], [412, 3691], [412, 3421],
             [427, 3420], [427, 3676], [684, 3676], [684, 3419], [412, 3419]]
for point in houseList:
    houseWall.addPoint(point[0], point[1])
houseWall.opacity = app.debugVisibility
houseEx = Polygon(1336, 1963, 1567, 1963, 1567, 1708, 1451, 1656, 1336, 1711, opacity = app.debugVisibility)

### Creates the border for the shop
shopList = [[962, 3404], [1249, 3404], [1249, 3691], [962, 3691],  [962, 3507],
            [977, 3507], [977, 3676],  [1234, 3676], [1234, 3505], [962, 3505]]
for point in shopList:
    shopWall.addPoint(point[0], point[1])
shopWall.opacity = app.debugVisibility
shopEx = Polygon(1437, 1339, 1652, 1339, 1652, 1104, 1545, 1056, 1437, 1104, opacity = app.debugVisibility)

# Final group containing all polygons
borders = Group(mapBorder, pond1, pond2, dungeonWall, houseWall, houseEx, shopWall, shopEx)



### The Enemy class controls enemy visuals and behaviour
#
#   The Enemy class is an object representation of the in game enemies.
#   These objects include the enemy body, its health bar, as well as any
#   methods that might be useful to the functions of the game like
#   attacking the player.
#
class Enemy:
    
    enemyGroup = Group()
    enemyList = []
    
    ### Constructor of the enemy class
    #
    #   Requires the name of the enemy, health, position, and color
    #
    def __init__(self, name, hp, positionX, positionY, color, gold):
        self.name = name            # Not used for anything other than differentiation
        self.hp = hp                # Health of the enemy
        self.totalHealth = hp       # Total health of the enemy used for health bar calculations
        self.rewardGold = gold      # The amount of gold given to the player when its killed.
        self.arrowShot = False      # Whether the enemy has an arrow shot or not
        self.toPlayerAngle = 0      # The angle to the player
        self.arrow = Rect(-10, -10, 5, 5, opacity = 0)  # Shape representing the arrow an enemy shoots
        self.nextShot = -1          # The frame when the enemy can next shoot
        posX = app.map.left + positionX
        posY = app.map.top + positionY
        self.body = Group(Circle(posX, posY, 15, fill = color, border = "black", borderWidth = 3))
        backBar = Rect(posX - 30, posY - 30, 60, 5, fill = "black")
        self.hpBar = Rect(posX - 29, posY - 29, 58, 3, fill = "crimson")
        self.sprite = Group(self.body, backBar, self.hpBar)
        Enemy.enemyGroup.add(self.sprite)
        Enemy.enemyList.append(self)
        
    ### Damaging the enemy function
    #
    #   Multiplies the damage by the sword damage multiplier and reduces
    #   the enemy health by that amount. If the health goes below zero
    #   the enemy will die.
    #
    def damage(self, amount):
        amount *= app.player.damageMultiplier # Applying the weapon multiplier to the enemy
        if amount <= 0:
            return
        elif amount >= self.hp:
            self.kill()
            return
        self.hpBar.width -= amount * (58 / self.totalHealth)
        self.hp -= amount
        
    ### A function that kills the enemy
    #   
    #   Adds 10 to the player balance, and removes the enemy from
    #   the group and list. Clears shapes from the canvas.
    #
    def kill(self):
        app.player.addGold(self.rewardGold)
        Enemy.enemyGroup.remove(self.sprite)
        Enemy.enemyList.remove(self)
        self.sprite.clear()
        del self
        
    ### Return the angle to the player from the center of the enemy
    #
    def getPlayerAngle(self):
        return angleTo(self.body.centerX, self.body.centerY, app.playerShapes.centerX, app.playerShapes.centerY)
    
    ### Return the distance between the enemy and the player
    #
    def getPlayerDistance(self):
        return distance(self.body.centerX, self.body.centerY, app.playerShapes.centerX, app.playerShapes.centerY)
        
    ### Initiates an attack on the player
    #
    #   This will create an arrow and start to propel it towards the player
    #   sprite. This will only start if the player distance is less than 160
    #   and the arrow has not been shot yet. Includes random deviation
    #   to the shot so it isnt consistent.
    #
    def attackPlayer(self):
        toPlayerDist = self.getPlayerDistance()
        if toPlayerDist < 160 and not self.arrowShot:
            self.toPlayerAngle = self.getPlayerAngle() + randrange(-8, 8)
            self.arrow = Rect(self.body.centerX, self.body.centerY, 1, 10, opacity = 100, align = "center", rotateAngle = self.toPlayerAngle)
            self.arrowShot = True
            self.sprite.add(self.arrow)
            self.nextShot = app.frameCount + randrange(60, 70)
       
    ### Resets the arrow to the default position
    #
    def resetArrow(self):
            self.arrowShot = False
            self.sprite.remove(self.arrow)
            self.arrow.centerX = self.body.centerX
            self.arrow.centerY = self.body.centerY
            self.arrow.opacity = 0
        
    ### Controls arrow logic
    #
    #   Moves the arrow towards the player 5 steps every frame. Destroys the
    #   arrow if it hits a wall or goes out of range. The player will also be
    #   damaged when the arrow hits the player.
    #
    def advanceArrow(self):
        if distance(self.arrow.centerX, self.arrow.centerY, self.body.centerX, self.body.centerY) < 160 and self.arrowShot:
            self.arrow.centerX, self.arrow.centerY = getPointInDir(self.arrow.centerX, self.arrow.centerY, self.toPlayerAngle, 5)
            if self.arrow.hitsShape(app.player.collide):
                app.player.damage(15)
                self.resetArrow()
            elif self.arrow.hitsShape(borders):
                self.resetArrow()
        else:
            self.resetArrow()



### The Player class controls player movement and other methods
#
#   The Player class is an object representation of the player. There is
#   always only 1 player object that is able to interact with the game's
#   functions. This single player object is stored in the "app.player"
#   variable. The player object here contains all of the shapes that make
#   up things like the player's body and sword as well as the methods
#   that control the player's armor/weapons and gold/bank
#
class Player:
    def __init__(self, name, hp, color):
        # Important Attributes
        self.name = name
        self.hp = hp
        self.totalHp = hp
        self.damageReduction = 1 # Armor stat
        self.damageMultiplier = 1 # Sword upgrades
        self.gold = 0
        self.bank = 0
        # Body Shape Creation
        self.main = Rect(190, 190, 20, 20, fill = color)
        facing = Line(200, 205, 200, 195, lineWidth = 1, arrowEnd = True, fill = "red")
        self.collide = Rect(190, 190, 20, 20, opacity = 0)
        boundingBox = Rect(self.main.centerX, self.main.centerY, 150, 150, align = "center", opacity = 0)
        body = Group(self.main, facing, self.collide, boundingBox)
        # Sword Shape Creation
        self.swordFront = Rect(self.main.centerX, self.main.centerY, 5, 40, fill = "saddleBrown", align = "bottom", opacity = 0)
        swordBack = Rect(self.main.centerX, self.main.centerY, 5, 40, align = "top", opacity = 0)
        self.sword = Group(self.swordFront, swordBack)
        self.sword.rotateAngle = -60
        self.swordArc = Arc(self.main.centerX, self.main.centerY, 90, 90, -60, 120, opacity = 0)
        self.gui = self.drawGui()
        self.fadeAnimation = Rect(0, 0, 400, 400, opacity = 0)
        self.fadePlaying = 0 # 0: not playing, 1: rising, 2: falling
        app.playerShapes = Group(body, self.sword, self.swordArc)
        
    ### Draws gui to the player screen
    #
    #   This includes the player health bar, as well as the
    #   amount of gold the player has.
    #
    def drawGui(self):
        goldBG = Rect(0, 0, 70, 20, fill = app.mainGradient, borderWidth = 2, border = rgb(99, 99, 49))
        self.goldLabel = Label(str(self.gold) + " g", 35, 10, size = 12, font = "montserrat")
        healthBG = Rect(200, 0, 200, 20, fill = app.mainGradient, borderWidth = 2, border = rgb(99, 99, 49))
        barBack = Rect(205, 5, 190, 10, fill = "black")
        self.healthBar = Rect(207, 7, 186, 6, fill = "darkRed")
        return Group(goldBG, self.goldLabel, healthBG, barBack, self.healthBar)
        
    ### The main fade animation used for player death, and going into buildings
    #
    def fadeAnim(self):
        self.fadeAnimation.toFront()
        if self.fadePlaying == 1:
            self.fadeAnimation.opacity += 2
            if self.fadeAnimation.opacity >= 100:
                GameUtils.triggerEvent(app.eventId)
                self.fadePlaying = 2
        elif self.fadePlaying == 2:
            self.fadeAnimation.opacity -= 2
            if self.fadeAnimation.opacity <= 0:
                self.fadePlaying = 0
                self.healthBar.fill = "darkRed"
    
    ### Add gold to the player as a reward
    #
    #   10 gold is rewarded per enemy killed, 50 exiting a completed dungeon
    #   negative values are handled as purchases from shops
    #
    #   Returns False only if a purchase was unsuccessful (not enough gold)
    #   otherwise, returns true
    #
    def addGold(self, amount):
        if amount < 0:
            # purchasing an item
            if self.gold + amount < 0:
                print("not enough gold.")
                return False
            else:
                print("purchase successful!")
                self.gold += amount
        else:
            # source of gold (adding gold to player)
            self.gold += amount
        self.goldLabel.value = str(self.gold) + " g"
        return True
        
    ### Player piggy bank functions
    #
    #   A positive amount will deposit, given the player has enough money.
    #   A negative amount will withdraw, given the player has enough in the bank
    #
    def addBank(self, amount):
        # Withdrawing from the bank
        if amount < 0:
            amount = -amount
            # Make the amount positive so the adding/subtracting makes sense
            if self.bank - amount < 0:
                print("Not enough gold in bank.")
                return
            else:
                self.bank -= amount
                self.gold += amount
        # Depositing to the bank
        elif amount <= self.gold:
            self.bank += amount
            self.gold -= amount
        self.addGold(0) # Updates the display number that is shown to the player
        
    ### Function that handles player health/damage
    #
    #   Applies armor reduction amount and changes player hp
    #   as well as the bar width in the gui
    #
    def damage(self, amount):
        amount *= self.damageReduction # Applying the player armor damage reduction
        if amount <= 0:
            self.healthBar.width = self.hp / (self.totalHp / 186)
            return
        elif amount >= self.hp:
            self.kill()
            return
        self.hp -= amount
        self.healthBar.width = self.hp / (self.totalHp / 186)
    
    ### Kills the player
    #
    #   This will send them back to the safehouse,
    #   and divide their gold in half.
    #
    def kill(self):
        app.eventId = 1
        app.player.fadePlaying = 1
        self.gold //= 2
        self.addGold(0)
        self.hp = 100
        self.healthBar.fill = "black"
        self.damage(0)
        return
    
    ### Handles main move calculations
    #
    #   Tries to move on both X and Y to allow for smooth movement against walls
    #
    def move(self, steps, angle):
        newPosX, newPosY = getPointInDir(app.map.centerX, app.map.centerY, angle, steps)
        changeX = newPosX - app.map.centerX
        changeY = newPosY - app.map.centerY
        self.attemptMove(changeX, 0)
        self.attemptMove(0, changeY)
    
    ### Helper function for moving
    #
    #   Used to detect collisions and move the player in the free direction
    #
    def attemptMove(self, dx, dy):
        app.map.centerX += dx
        app.map.centerY += dy
        if app.player.collide.hitsShape(borders):
            app.map.centerX -= dx
            app.map.centerY -= dy
            
    ### Clears the player shapes from canvas
    #
    def clearPlayer(self):
        app.playerShapes.clear()
        self.gui.clear()
        del self



### The GameUtils class holds important game functions
#
#   Functions like displaying signs and dialogue reside here, as well as
#   the games pause menu, title screen, saving data, and building interior
#   functionality.
#
class GameUtils:
    
    displayScreen = Group()
    
    titleActive = False
    playButton = Group()
    loadSaveButton = Group()
    creditsButton = Group()
    controlsButton = Group()
    
    message = Group()
    messageId = -1
    messageOption1 = Group()
    messageOption2 = Group()
    messageOption3 = Group()
    messageOption4 = Group()
    
    continued = False
    paused = False
    mapShown = False
    menuButton = Group()
    resumeButton = Group()
    okButton = Group()
    returnButton = Group()
    
    ### Displays a message to the user in the form of a text box with options.
    #
    #   "id": used to differentiate the message from others. Used in the onMouseClick function for dialogue
    #   (an id of 0 represents a text box that will simply clear with player input, useful for signs)
    #   "firstLine"... : the text that will be displayed on the lines of the text box
    #   "options": a list that represents all options for the user to click on
    #
    def displayMessage(id, firstLine, secondLine, thirdLine, options):
        GameUtils.clearMessage()
        bgBox = Rect(140, 275, 240, 105, fill = app.mainGradient, borderWidth = 2, border = rgb(99, 99, 49))
        separatingLine = Line(300, 275, 300, 380, lineWidth = 2, fill = rgb(99, 99, 49))
        line1 = Label(firstLine, 220, 300, size = 16, font = "montserrat")
        line2 = Label(secondLine, 220, 330, size = 16, font = "montserrat")
        line3 = Label(thirdLine, 220, 360, size = 16, font = "montserrat")
        if len(options) == 0:
            GameUtils.messageId = 0
            GameUtils.messageOption1 = Group(Rect(305, 280, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label("[OK]", 340, 290, size = 10, font = "montserrat"))
            GameUtils.message = Group(bgBox, separatingLine, line1, line2, line3, GameUtils.messageOption1)
        elif len(options) == 1:
            GameUtils.messageId = id
            GameUtils.messageOption1 = Group(Rect(305, 280, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[0], 340, 290, size = 10, font = "montserrat"))
            GameUtils.message = Group(bgBox, separatingLine, line1, line2, line3, GameUtils.messageOption1)
        elif len(options) == 2:
            GameUtils.messageId = id
            GameUtils.messageOption1 = Group(Rect(305, 280, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[0], 340, 290, size = 10, font = "montserrat"))
            GameUtils.messageOption2 = Group(Rect(305, 305, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[1], 340, 315, size = 10, font = "montserrat"))
            GameUtils.message = Group(bgBox, separatingLine, line1, line2, line3, GameUtils.messageOption1, GameUtils.messageOption2)
        elif len(options) == 3:
            GameUtils.messageId = id
            GameUtils.messageOption1 = Group(Rect(305, 280, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[0], 340, 290, size = 10, font = "montserrat"))
            GameUtils.messageOption2 = Group(Rect(305, 305, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[1], 340, 315, size = 10, font = "montserrat"))
            GameUtils.messageOption3 = Group(Rect(305, 330, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[2], 340, 340, size = 10, font = "montserrat"))
            GameUtils.message = Group(bgBox, separatingLine, line1, line2, line3, GameUtils.messageOption1, GameUtils.messageOption2, GameUtils.messageOption3)
        elif len(options) >= 4:
            GameUtils.messageId = id
            GameUtils.messageOption1 = Group(Rect(305, 280, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[0], 340, 290, size = 10, font = "montserrat"))
            GameUtils.messageOption2 = Group(Rect(305, 305, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[1], 340, 315, size = 10, font = "montserrat"))
            GameUtils.messageOption3 = Group(Rect(305, 330, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[2], 340, 340, size = 10, font = "montserrat"))
            GameUtils.messageOption4 = Group(Rect(305, 355, 70, 20, fill = "tan", borderWidth = 2, border = rgb(99, 99, 49)), Label(options[3], 340, 365, size = 10, font = "montserrat"))
            GameUtils.message = Group(bgBox, separatingLine, line1, line2, line3, GameUtils.messageOption1, GameUtils.messageOption2, GameUtils.messageOption3, GameUtils.messageOption4)
    
    ### Clears the current message on screen
    #
    def clearMessage():
        GameUtils.message.clear()
        GameUtils.message = Group()
        GameUtils.messageId = -1
    
    ### The title sequence of the game featuring play, load save, and credits
    #
    def titleScreen():
        GameUtils.displayScreen.clear()
        app.stepsPerSecond = 0
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 20)
        title = Label("Untitled RPG", 200, 80, size = 42, font = "cinzel", bold = True, fill = "white", border = "black", borderWidth = 1)
        GameUtils.titleActive = True
        GameUtils.paused = False
        
        GameUtils.playButton = Group(Circle(40, 240, 20, fill = "tan", border = "black", borderWidth = 2),
                                     Circle(160, 240, 20, fill = "tan", border = "black", borderWidth = 2),
                                     Rect(100, 240, 120, 40, align = "center", fill = "tan", border = "black", borderWidth = 2),
                                     Rect(100, 240, 122, 36, align = "center", fill = "tan"),
                                     Label("Play Game", 100, 240, fill = "black", size = 22))
        
        GameUtils.loadSaveButton = Group(Circle(40, 300, 20, fill = "tan", border = "black", borderWidth = 2),
                                         Circle(160, 300, 20, fill = "tan", border = "black", borderWidth = 2),
                                         Rect(100, 300, 120, 40, align = "center", fill = "tan", border = "black", borderWidth = 2),
                                         Rect(100, 300, 122, 36, align = "center", fill = "tan"),
                                         Label("Load Save", 100, 300, fill = "black", size = 22))
        
        GameUtils.creditsButton = Group(Circle(40, 360, 20, fill = "tan", border = "black", borderWidth = 2),
                                        Circle(160, 360, 20, fill = "tan", border = "black", borderWidth = 2),
                                        Rect(100, 360, 120, 40, align = "center", fill = "tan", border = "black", borderWidth = 2),
                                        Rect(100, 360, 122, 36, align = "center", fill = "tan"),
                                        Label("Credits", 100, 360, fill = "black", size = 22))
                                        
        GameUtils.controlsButton = Group(Circle(240, 360, 20, fill = "tan", border = "black", borderWidth = 2),
                                         Circle(360, 360, 20, fill = "tan", border = "black", borderWidth = 2),
                                         Rect(300, 360, 120, 40, align = "center", fill = "tan", border = "black", borderWidth = 2),
                                         Rect(300, 360, 122, 36, align = "center", fill = "tan"),
                                         Label("Controls", 300, 360, fill = "black", size = 22))
                                        
        GameUtils.displayScreen = Group(bg, title, GameUtils.playButton, GameUtils.loadSaveButton, GameUtils.creditsButton, GameUtils.controlsButton)
        
    ### The credits screen showing who made what in the game
    #
    def showCredits():
        GameUtils.titleActive = False
        GameUtils.paused = True
        GameUtils.displayScreen.clear()
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 70)
        GameUtils.okButton = Group(Rect(30, 320, 140, 40, fill = "white", border = "black", borderWidth = 2),
                                   Label("Return to Menu", 100, 340, fill = "black", size = 18))
        
        credits = Group(Label("Game Programming: NameIsMissing", 200, 40, fill = "white", size = 20),
                        Label("Map Design: NameIsMissing", 200, 100, fill = "white", size = 20),
                        Label("Map tiles: RPG Nature Tileset by Stealthix", 200, 160, fill = "white", size = 20))
        
        GameUtils.displayScreen.add(bg, GameUtils.okButton, credits)
        
    ### Teaches the player how to control the game...
    #
    def showControls():
        GameUtils.titleActive = False
        GameUtils.paused = True
        GameUtils.displayScreen.clear()
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 70)
        GameUtils.okButton = Group(Rect(30, 320, 140, 40, fill = "white", border = "black", borderWidth = 2),
                                   Label("Return to Menu", 100, 340, fill = "black", size = 18))
        
        credits = Group(Label("W/S: Move forward/back", 200, 40, fill = "white", size = 20),
                        Label("A/D: Turn left/right", 200, 80, fill = "white", size = 20),
                        Label("Space: Swing Sword", 200, 120, fill = "white", size = 20),
                        Label("M: View Map", 200, 160, fill = "white", size = 20),
                        Label("P: Pause Game", 200, 200, fill = "white", size = 20),
                        Label("Save: Pause > Save", 200, 240, fill = "white", size = 20))
        
        GameUtils.displayScreen.add(bg, GameUtils.okButton, credits)
    
    ### Gets the save code for the player which holds all data
    #
    #   The getSaveCode() function returns a string representation of all
    #   data in the game which will allow the player to continue from
    #   where they left off.
    #
    def getSaveCode():
        playerGold = app.player.gold
        playerBank = app.player.bank
        playerArmor = app.player.damageReduction
        playerSword = app.player.damageMultiplier
        return str(playerGold) + "!" + str(playerBank) + "@" + str(playerArmor) + "#" + str(playerSword) + "$"
    
    ### Attempt to load a save from a string entered by the player
    #
    #   If any error occurs while loading the data, it will be handled
    #   and interpreted as an invalid save code by the game.
    #
    def loadSave(saveString):
        try:
            playerGold = int(saveString[0:saveString.index("!")])
            playerBank = int(saveString[saveString.index("!") + 1:saveString.index("@")])
            playerArmor = float(saveString[saveString.index("@") + 1:saveString.index("#")])
            playerSword = float(saveString[saveString.index("#") + 1:saveString.index("$")])
            GameUtils.continued = True
            GameUtils.playGame()
            app.player.addGold(playerGold)
            app.player.bank = playerBank
            if playerArmor in [1, 0.8, 0.6, 0.4, 0.1]:
                app.player.damageReduction = playerArmor
                app.player.main.fill = ["white", "tan", "darkGray", "goldenrod", "forestGreen"][[1, 0.8, 0.6, 0.4, 0.1].index(playerArmor)]
            if playerSword in [1, 1.3, 1.6, 2, 5]:
                app.player.damageMultiplier = playerSword
                app.player.swordFront.fill = ["white", "dimGray", "whiteSmoke", "goldenrod", "lightSkyBlue"][[1, 1.3, 1.6, 2, 5].index(playerSword)]
        except:
            GameUtils.displayScreen.add(Label("Invalid Save Code", 300, 300, size = 20, fill = "red"))
            print("Invalid Save Code")
    
    ### Spawn the player, and start the game
    #
    #   Will spawn the player in the main path area if its a new game,
    #   otherwise they will be spawned in the safehouse.
    #
    def playGame():
        GameUtils.titleActive = False
        GameUtils.displayScreen.clear()
        app.player = Player("testname", 100, "white")
        if GameUtils.continued: 
            # Spawn the player at their safehouse
            app.map.centerX = 1522
            app.map.centerY = -1342
        else: 
            # Spawn the player in the main area
            app.map.centerX = 1246
            app.map.centerY = 101
            GameUtils.displayMessage(11, "What you want", "to learn about", "the game?", ["Weapons", "Armor", "Dungeons", "Nothing"])
        app.stepsPerSecond = 30
        
    ### Display a pause screen to the user
    #
    #   The pause screen features a return to menu button which will 
    #   allow the player to save their progress. Sets app.stepsPerSecond
    #   to 0 which stops all game functions in onStep from running.
    #
    def pause():
        GameUtils.displayScreen.clear()
        GameUtils.paused = True
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 50)
        pauseText = Label("Game Paused", 200, 80, size = 28, font = "monospace", fill = "white")
        GameUtils.resumeButton = Group(Rect(120, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"),
                                       Label("Resume", 120, 280, fill = "black", font = "monospace"))
        GameUtils.menuButton = Group(Rect(280, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"),
                                     Label("Save Game", 280, 280, fill = "black", font = "monospace"))
        GameUtils.displayScreen = Group(bg, pauseText, GameUtils.resumeButton, GameUtils.menuButton)
        app.stepsPerSecond = 0
        
    ### Resume the game from the paused state
    #
    def unpause():
        GameUtils.paused = False
        GameUtils.displayScreen.clear()
        app.stepsPerSecond = 30
        
    def showMap():
        if GameUtils.mapShown:
            GameUtils.mapShown = False
            GameUtils.displayScreen.clear()
        else:
            GameUtils.mapShown = True
            GameUtils.displayScreen.add(Rect(54, 23, 292, 354), Image("cmu://842876/31242720/minimap.png", 56, 25))
            GameUtils.displayScreen.toFront()
        
    ### Return to the title screen of the game
    #
    #   Displays the players save code to the screen which will
    #   allow them to continue at a later date.
    #
    def returnToMenu():
        GameUtils.displayScreen.clear()
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 50)
        save = Group(Label("Save Code:", 200, 80, size = 28, font = "monospace", fill = "white"), 
                     Label(GameUtils.getSaveCode(), 200, 110, size = 18, font = "monospace", fill = "white"), 
                     Label("(Save this to keep your progress!)", 200, 140, size = 18, font = "monospace", fill = "white"))
        
        GameUtils.okButton = Group(Rect(200, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"),
                                   Label("OK", 200, 280, fill = "black", font = "monospace"))
        
        GameUtils.displayScreen = Group(bg, save, GameUtils.okButton)
        app.player.clearPlayer()
        
    ### A function used to transport the player between interiors
    #
    #   This should have been used for more things, but I did not have 
    #   enough time to move more events here.
    #
    def triggerEvent(num):
        app.eventId = -1
        if num == 1: # Enter the player house
            Enemy.enemyGroup.clear()
            Enemy.enemyList = []
            app.map.centerX = 1555
            app.map.centerY = -1365
        elif num == 2: # Exit the player house
            app.map.centerX = 601
            app.map.centerY = 120
        elif num == 3: # Enter the shop
            app.map.centerX = 1008
            app.map.centerY = -1393
        elif num == 4: # Exit the shop
            app.map.centerX = 506
            app.map.centerY = 776
        elif num == 5: # Enter the dungeon and spawn enemies
            Enemy("level1", 100, 3020, 1345, "red", 10)
            Enemy("level1", 100, 3137, 1477, "red", 10)
            Enemy("level1", 100, 3333, 1329, "red", 10)
            
            Enemy("level2", 200, 3308, 1152, "royalBlue", 15)
            Enemy("level2", 200, 3077, 1001, "royalBlue", 15)
            Enemy("level2", 200, 3012, 1157, "royalBlue", 15)
            
            Enemy("boss", 400, 3165, 737, "mediumSeaGreen", 25)
            
            app.map.centerX = -1178
            app.map.centerY = 479
        elif num == 6: # Exit the dungeon
            if len(Enemy.enemyList) == 0:
                # Award the player gold if they killed all enemies
                app.player.addGold(50)
            Enemy.enemyGroup.clear()
            Enemy.enemyList = []
            app.map.centerX = 1884
            app.map.centerY = 1884


### Used to interpret the player holding a key down (onKeyHold)
#
#   All of the player movement detection resides here. Code inside each
#   block will continue to execute while a key is held down.
#   
#   Code for detecting when a player is inside of a sign also resides here
#   because it is more efficient to check only when a player moves rather
#   than every frame.
#
def onKeyHold(key):
    if "w" in key:
        app.player.move(-4, app.playerShapes.rotateAngle)
    if "s" in key:
        app.player.move(4, app.playerShapes.rotateAngle)
    if "d" in key:
        app.playerShapes.rotateAngle += 3
        app.player.collide.rotateAngle = 0
    if "a" in key:
        app.playerShapes.rotateAngle -= 3
        app.player.collide.rotateAngle = 0
    
    playerX, playerY = (app.playerShapes.centerX, app.playerShapes.centerY)
    
    if app.signsGroup.hits(playerX, playerY) and not app.inSign:
        if app.signsList[0].hits(playerX, playerY):
            GameUtils.displayMessage(1, "Do you want to", "enter your house?", "", ["Yes", "No"])
        elif app.signsList[1].hits(playerX, playerY):
            GameUtils.displayMessage(2, "Do you want to", "leave your house?", "", ["Yes", "No"])
        elif app.signsList[2].hits(playerX, playerY):
            GameUtils.displayMessage(3, "Do you want to", "enter the shop?", "", ["Yes", "No"])
        elif app.signsList[3].hits(playerX, playerY):
            GameUtils.displayMessage(4, "Do you want to", "leave the shop?", "", ["Yes", "No"])
        elif app.signsList[4].hits(playerX, playerY):
            GameUtils.displayMessage(5, "Welcome to the", "shop. What do you", "want to buy?", ["Weapons", "Armor", "Nothing"])
        elif app.signsList[5].hits(playerX, playerY):
            GameUtils.displayMessage(9, "Do you want to", "enter the", "dungeon?", ["Yes", "No"])
        elif app.signsList[6].hits(playerX, playerY):
            GameUtils.displayMessage(10, "Do you want to", "exit the dungeon?", "", ["Yes", "No"])
        elif app.signsList[7].hits(playerX, playerY):
            app.eventId = 6
            app.player.fadePlaying = 1 
        elif app.signsList[8].hits(playerX, playerY):
            try:
                amount = int(app.getTextInput("Bank balance: " + str(app.player.bank) + "g || Enter amount to deposit or negative to withdraw."))
                app.player.addBank(amount)
            except:
                return
        elif app.signsList[9].hits(playerX, playerY):
            GameUtils.displayMessage(0, "You are looking", "at a pond.", "", [])
        elif app.signsList[10].hits(playerX, playerY):
            GameUtils.displayMessage(0, "Sorry this cave", "was never finished.", "", [])
        app.inSign = True
        
        
    app.inSign = app.signsGroup.hits(playerX, playerY)



### Used to interpret a single key press (onKeyPress)
#
#   This method is used instead of onKeyHold to make sure the code in the
#   blocks are only executed once.
#
def onKeyPress(key):
    if key == "space" and not app.swordSwing:
        app.swordSwing = True
        if Enemy.enemyGroup.hitsShape(app.player.swordArc):
            for enemy in Enemy.enemyList:
                if enemy.sprite.hitsShape(app.player.swordArc):
                    enemy.damage(20)
    elif key == "p":
        if not GameUtils.paused:
            GameUtils.pause()
        else:
            GameUtils.unpause()
            
    elif key == "m":
        GameUtils.showMap()



### Used to detect mouse clicks by the player (onMousePress)
#   
#   All functions of the game that rely on player clicks reside here because
#   it is the only place where clicks can be interpreted by CMU.
#
def onMousePress(posX, posY):
    
    GU = GameUtils
    # Replacing all mentions of GameUtils class with GU to *simplify* things
    
    ### Title screen click logic
    if GU.titleActive:
        if GU.playButton.hits(posX, posY):
            GU.continued = False
            GU.playGame()
        elif GU.loadSaveButton.hits(posX, posY):
            try:
                saveString = app.getTextInput("Please enter save code or \"X\" to cancel.")
            except:
                return
            if saveString == "" or saveString.lower() == "x":
                return
            GU.loadSave(saveString)
        elif GU.creditsButton.hits(posX, posY):
            GU.showCredits()
        elif GU.controlsButton.hits(posX, posY):
            GU.showControls()
        
    ### Pause menu click logic
    elif GU.paused:
        if GU.resumeButton.hits(posX, posY):
            GU.unpause()
        elif GU.menuButton.hits(posX, posY):
            GU.returnToMenu()
        elif GU.okButton.hits(posX, posY):
            GU.paused = False
            GU.titleScreen()
    
    ### Message handling logic
    #
    #   Displays another message or executes code based on what choice has
    #   been picked in a dialogue box.
    #
    elif GU.messageId != -1:
        if GU.messageId == 0: # Default text box, has an ok button this will clear it.
            if GU.messageOption1.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 1: # Reserved for entering the player house
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 1
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 2: # Reserved for exiting the player house
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 2
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 3: # Reserved for entering the shop
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 3
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 4: # Reserved for exiting the shop
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 4
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 5: # Weapon buy menu
            if GU.messageOption1.hits(posX, posY):
                GU.clearMessage()
                GU.displayMessage(7, "What sword do", "you want to buy?", "", ["Stone (20)", "Iron (100)", "Gold (300)", "None"])
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
                GU.displayMessage(8, "What armor do", "you want to buy?", "", ["Leather (90)", "Steel (200)", "Gold (500)", "None"])
            elif GU.messageOption3.hits(posX, posY):
                GU.clearMessage()
        
        ### Shop sword statistics
        elif GU.messageId == 7:
            if GU.messageOption1.hits(posX, posY):
                GU.clearMessage()
                if app.player.addGold(-20): # Attempt purchase of the stone sword
                    app.player.swordFront.fill = "dimGray"
                    app.player.damageMultiplier = 1.3
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
                if app.player.addGold(-100): # Attempt purchase of the iron sword
                    app.player.swordFront.fill = "whiteSmoke"
                    app.player.damageMultiplier = 1.6
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption3.hits(posX, posY):
                GU.clearMessage() 
                if app.player.addGold(-300): # Attempt purchase of the gold sword
                    app.player.swordFront.fill = "goldenrod"
                    app.player.damageMultiplier = 2
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption4.hits(posX, posY):
                GU.clearMessage()
        
        ### Shop armor statistics
        elif GU.messageId == 8:
            if GU.messageOption1.hits(posX, posY):
                GU.clearMessage()
                if app.player.addGold(-90): # Attempt purchase of the leather armor
                    app.player.main.fill = "tan"
                    app.player.damageReduction = 0.8
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
                if app.player.addGold(-200): # Attempt purchase of the steel armor
                    app.player.main.fill = "darkGray"
                    app.player.damageReduction = 0.6
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption3.hits(posX, posY):
                GU.clearMessage() 
                if app.player.addGold(-500): # Attempt purchase of the gold armor
                    app.player.main.fill = "goldenrod"
                    app.player.damageReduction = 0.4
                else:
                    GU.displayMessage(0, "Not enough gold", "", "", [])
            elif GU.messageOption4.hits(posX, posY):
                GU.clearMessage
                
        elif GU.messageId == 9: # Reserved for entering Dungeon
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 5
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
                
        elif GU.messageId == 10: # Reserved for exiting Dungeon
            if GU.messageOption1.hits(posX, posY):
                app.eventId = 6
                app.player.fadePlaying = 1
                GU.clearMessage()
            elif GU.messageOption2.hits(posX, posY):
                GU.clearMessage()
                
        elif GU.messageId == 11:
            if GU.messageOption1.hits(posX, posY):
                GU.displayMessage(12, "Weapons multiply", "damage making", "dungeons easier.", ["[OK]"])
            elif GU.messageOption2.hits(posX, posY):
                GU.displayMessage(12, "Armor reduces", "damage taken by", "enemies.", ["[OK]"])
            elif GU.messageOption3.hits(posX, posY):
                GU.displayMessage(13, "Dungeons are", "at the upper", "left of the map.", ["[CONTINUE]"])
            elif GU.messageOption4.hits(posX, posY):
                GU.clearMessage()
        
        elif GU.messageId == 12:
            if GU.messageOption1.hits(posX, posY):
                GU.displayMessage(11, "What you want", "to learn about", "the game?", ["Weapons", "Armor", "Dungeons", "Nothing"])
                
        elif GU.messageId == 13:
            if GU.messageOption1.hits(posX, posY):
                GU.displayMessage(12, "These dungeons", "have enemies you", "can kill for gold.", ["[OK]"])



### Function that runs every frame
#
#   This function is used to control things like player health regeneration,
#   travel animations, sword animations, and enemy attacks. These need to be
#   placed here as there is no other way to control visual animations
#   simultaneously while also running the game.
#
def onStep():
    app.frameCount += 1 # This variable is used to control the time between things like enemy attacks
    
    # Player health regen
    if app.frameCount % 15 == 0 and app.player.hp < 100:
        app.player.hp += 1
        # Call to the damage function to update the health bar on screen, otherwise you wouldnt be able to see the regeneration
        app.player.damage(0)
        
    # Controlling the fade animation played when going inside buildings or dying
    if app.player.fadePlaying != 0:
        app.player.fadeAnim()
    
    # Sword swing animation played when the player swings their sword
    if app.swordSwing and app.player.sword.rotateAngle < app.playerShapes.rotateAngle + 60:
        app.player.swordFront.opacity = 100
        app.player.sword.rotateAngle += 8
    else:
        app.player.swordFront.opacity = 0
        app.player.sword.rotateAngle = app.playerShapes.rotateAngle + -60
        app.swordSwing = False
        
    # Enemy attacking player code
    for enemy in Enemy.enemyList:
        # Look through each enemy and see if they are ready to shoot, otherwise advance the arrow one step
        if enemy.nextShot < app.frameCount:
            enemy.attackPlayer()
        else:
            enemy.advanceArrow()

app.map = Group(mapBG, chest, borders, app.signsGroup, Enemy.enemyGroup)
app.map.toBack()
oceanBG.toBack()
GameUtils.titleScreen()

# Pond sign: 756, 1794
# house sign: 1448, 1980
# shop sign: 1534, 1350
