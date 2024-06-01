# ~~~~~ Untitled RPG ~~~~~
# 
# Created by: NameIsMissing
# 
# Untitled RPG is an RPG made on my own using a tilepack found online for the
# art. The game has features like an expansive map, building interiors, combat
# enemy AI/movement, shops to buy items, dungeons for enemies, a save feature,
# fishing system, and much more.

import random
from cmu_graphics import *

# App related global variables
app.frameCount = 0          # Counting frames, used for some animations / player healing
app.stepsPerSecond = 0      # Frames per second of the app. This is set to 0 to simulate a pause, normally at 30
app.mainGradient = gradient(rgb(217, 190, 117), rgb(153, 138, 98), start = "center") # The gradient used for many of the game GUI's

# Map related global Variables
app.map = Group()
app.enemies = Group()
app.enemyList = []

# Global variables related to signs in game, used to display sign message to player
app.signsGroup = Group()
app.signsList = []
app.inSign = False

# Add a testing sign to the map, will be moved to a map initiation function soon.
sign1 = Circle(291, 111, 32, opacity = 0)
app.signsGroup.add(sign1)
app.signsList.append(sign1)

# Player related global variables
app.player = None
app.playerShapes = Group()
app.swordSwing = False
app.eventId = -1

# Map initialization
mapBorder = Polygon()
oceanBG = Image("cmu://842876/31169753/water.png", 0, 0)
mapBG = Image("cmu://842876/31169479/rpgMapPreFinal.png", 0, 0)
app.map = Group(mapBG, mapBorder, app.signsGroup, app.enemies)
app.map.toBack()
oceanBG.toBack()

# Points used to denote the border of the map so the player cannot walk off of it
pointList = [[32, 156],    [414, 156],   [414, 220],   [1184, 220],  [1184, 285],
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
             
for point in pointList:
    mapBorder.addPoint(point[0], point[1])

mapBorder.opacity = 0
mapBorder.left = 0
mapBorder.top = 0

class Enemy:
    def __init__(self, name, hp, positionX, positionY):
        self.name = name
        self.hp = hp
        self.totalHealth = hp
        self.arrowShot = False
        self.toPlayerAngle = 0
        self.arrow = Rect(-10, -10, 5, 5, opacity = 0)
        self.nextShot = -1
        posX = app.map.left + positionX
        posY = app.map.top + positionY
        self.body = Group(Circle(posX, posY, 15, fill = "red", border = "black", borderWidth = 3))
        backBar = Rect(posX - 30, posY - 30, 60, 5, fill = "black")
        self.hpBar = Rect(posX - 29, posY - 29, 58, 3, fill = "crimson")
        self.sprite = Group(self.body, backBar, self.hpBar)
        app.enemies.add(self.sprite)
        app.enemyList.append(self)
        
    def damage(self, amount):
        if amount <= 0:
            return
        elif amount >= self.hp:
            self.kill()
            return
        self.hpBar.width -= amount * (58 / self.totalHealth)
        self.hp -= amount
        
    def kill(self):
        app.player.addGold(10)
        app.enemies.remove(self.sprite)
        app.enemyList.remove(self)
        self.sprite.clear()
        del self
        
    def getPlayerAngle(self):
        return angleTo(self.body.centerX, self.body.centerY, app.playerShapes.centerX, app.playerShapes.centerY)
        
    def getPlayerDistance(self):
        return distance(self.body.centerX, self.body.centerY, app.playerShapes.centerX, app.playerShapes.centerY)
        
    def attackPlayer(self):
        toPlayerDist = self.getPlayerDistance()
        if toPlayerDist < 160 and not self.arrowShot:
            self.toPlayerAngle = self.getPlayerAngle() + randrange(-8, 8)
            self.arrow = Rect(self.body.centerX, self.body.centerY, 1, 10, opacity = 100, align = "center", rotateAngle = self.toPlayerAngle)
            self.arrowShot = True
            self.sprite.add(self.arrow)
            self.nextShot = app.frameCount + randrange(60, 70)
            
    def resetArrow(self):
            self.arrowShot = False
            self.sprite.remove(self.arrow)
            self.arrow.centerX = self.body.centerX
            self.arrow.centerY = self.body.centerY
            self.arrow.opacity = 0
            
    def advanceArrow(self):
        if distance(self.arrow.centerX, self.arrow.centerY, self.body.centerX, self.body.centerY) < 160 and self.arrowShot:
            self.arrow.centerX, self.arrow.centerY = getPointInDir(self.arrow.centerX, self.arrow.centerY, self.toPlayerAngle, 5)
            if self.arrow.hitsShape(app.player.collide):
                app.player.damage(15)
                self.resetArrow()
        else:
            self.resetArrow()

class Player:
    def __init__(self, name, hp, color):
        # Important Attributes
        self.name = name
        self.hp = hp
        self.totalHp = hp
        self.gold = 0
        self.bank = 0
        # Body Shape Creation
        main = Rect(190, 190, 20, 20, fill = color)
        facing = Line(200, 205, 200, 195, lineWidth = 1, arrowEnd = True, fill = "red")
        self.collide = Rect(190, 190, 20, 20, opacity = 0)
        boundingBox = Rect(main.centerX, main.centerY, 150, 150, align = "center", opacity = 0)
        body = Group(main, facing, self.collide, boundingBox)
        # Sword Shape Creation
        self.swordFront = Rect(main.centerX, main.centerY, 5, 40, fill = "red", align = "bottom", opacity = 0)
        swordBack = Rect(main.centerX, main.centerY, 5, 40, align = "top", opacity = 0)
        self.sword = Group(self.swordFront, swordBack)
        self.sword.rotateAngle = -60
        self.swordArc = Arc(main.centerX, main.centerY, 90, 90, -60, 120, opacity = 0)
        # Bow shape creation
        self.posX = main.centerX
        self.posY = main.centerY
        self.gui = self.drawGui()
        self.fadeAnimation = Rect(0, 0, 400, 400, opacity = 0)
        self.fadePlaying = 0 # 0: not playing, 1: rising, 2: falling
        app.playerShapes = Group(body, self.sword, self.swordArc)
        
    def drawGui(self):
        goldBG = Rect(0, 0, 70, 20, fill = app.mainGradient, borderWidth = 2, border = rgb(99, 99, 49))
        self.goldLabel = Label(str(self.gold) + " g", 35, 10, size = 12, font = "montserrat")
        healthBG = Rect(200, 0, 200, 20, fill = app.mainGradient, borderWidth = 2, border = rgb(99, 99, 49))
        barBack = Rect(205, 5, 190, 10, fill = "black")
        self.healthBar = Rect(207, 7, 186, 6, fill = "darkRed")
        return Group(goldBG, self.goldLabel, healthBG, barBack, self.healthBar)
        
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
    
    def addGold(self, amount):
        if amount < 0:
            # purchasing an item
            if self.gold + amount < 0:
                print("not enough gold.")
                return
            else:
                print("purchase successful!")
                self.gold += amount
        else:
            # source of gold (adding gold to player)
            self.gold += amount
        self.goldLabel.value = str(self.gold) + " g"
        
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
        elif amount < self.gold:
            self.bank += amount
            self.gold -= amount
        self.addGold(0) # Updates the display number that is shown to the player
        
    def damage(self, amount):
        if amount <= 0:
            self.healthBar.width = self.hp / (self.totalHp / 186)
            return
        elif amount >= self.hp:
            self.kill()
            return
        self.hp -= amount
        self.healthBar.width = self.hp / (self.totalHp / 186)
        
    def kill(self):
        #do something? maybe send back to 'safehouse' and display a you died screen?
        self.gold //= 2
        self.addGold(0)
        return
    
    def move(self, steps, angle):
        newPosX, newPosY = getPointInDir(app.map.centerX, app.map.centerY, angle, steps)
        changeX = newPosX - app.map.centerX
        changeY = newPosY - app.map.centerY
        self.attemptMove(changeX, 0)
        self.attemptMove(0, changeY)
    
    def attemptMove(self, dx, dy):
        app.map.centerX += dx
        app.map.centerY += dy
        if app.player.collide.hitsShape(mapBorder):
            app.map.centerX -= dx
            app.map.centerY -= dy
            
    def clearPlayer(self):
        app.playerShapes.clear()
        self.gui.clear()
        del self

class GameUtils:
    
    displayScreen = Group()
    
    titleActive = False
    playButton = Group()
    loadSaveButton = Group()
    creditsButton = Group()
    
    message = Group()
    messageId = -1
    messageOption1 = Group()
    messageOption2 = Group()
    messageOption3 = Group()
    messageOption4 = Group()
    
    continued = False
    paused = False
    menuButton = Group()
    resumeButton = Group()
    okButton = Group()
    
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
    
    def clearMessage():
        GameUtils.message.clear()
        GameUtils.message = Group()
        GameUtils.messageId = -1
    
    def titleScreen():
        GameUtils.displayScreen.clear()
        app.stepsPerSecond = 0
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 20)
        title = Label("Untitled RPG", 200, 80, size = 42, font = "cinzel", bold = True, fill = "white", border = "black", borderWidth = 1)
        GameUtils.titleActive = True
        
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
                                        
        GameUtils.displayScreen = Group(bg, title, GameUtils.playButton, GameUtils.loadSaveButton, GameUtils.creditsButton)
    
    def getSaveCode():
        playerGold = app.player.gold
        playerBank = app.player.bank
        return str(playerGold) + "!" + str(playerBank) + "@"
    
    def loadSave(saveString):
        try:
            playerGold = int(saveString[0:saveString.index("!")])
            playerBank = int(saveString[saveString.index("!") + 1:saveString.index("@")])
            GameUtils.continued = True
            GameUtils.playGame()
            app.player.addGold(playerGold)
            app.player.bank = playerBank
        except:
            GameUtils.displayScreen.add(Label("Invalid Save Code", 310, 380, size = 20, fill = "red"))
            print("Invalid Save Code")
    
    def playGame():
        GameUtils.titleActive = False
        GameUtils.displayScreen.clear()
        app.player = Player("testname", 100, "white")
        if GameUtils.continued:
            print("do something")
        else:
            app.map.centerX = 519
            app.map.centerY = -408
        app.stepsPerSecond = 30
        
    def pause():
        GameUtils.displayScreen.clear()
        GameUtils.paused = True
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 50)
        pauseText = Label("Game Paused", 200, 80, size = 28, font = "monospace", fill = "white")
        GameUtils.resumeButton = Group(Rect(120, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"), Label("Resume", 120, 280, fill = "black", font = "monospace"))
        GameUtils.menuButton = Group(Rect(280, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"), Label("Menu", 280, 280, fill = "black", font = "monospace"))
        GameUtils.displayScreen = Group(bg, pauseText, GameUtils.resumeButton, GameUtils.menuButton)
        app.stepsPerSecond = 0
        
    def unpause():
        GameUtils.paused = False
        GameUtils.displayScreen.clear()
        app.stepsPerSecond = 30
        
    def returnToMenu():
        GameUtils.displayScreen.clear()
        bg = Rect(0, 0, 400, 400, fill = "black", opacity = 50)
        save = Group(Label("Save Code:", 200, 80, size = 28, font = "monospace", fill = "white"), 
                     Label(GameUtils.getSaveCode(), 200, 110, size = 18, font = "monospace", fill = "white"), 
                     Label("(Save this to keep your progress!)", 200, 140, size = 18, font = "monospace", fill = "white"))
        GameUtils.okButton = Group(Rect(200, 280, 80, 30, fill = "white", borderWidth = 2, border = "black", align = "center"), Label("OK", 200, 280, fill = "black", font = "monospace"))
        GameUtils.displayScreen = Group(bg, save, GameUtils.okButton)
        app.player.clearPlayer()
        
    def triggerEvent(num):
        if num == 1:
            app.map.centerX = -128
            app.map.centerY = -392
        elif num == 2:
            print("transport to shop")
    

def onKeyHold(key):
    if "w" in key:
        app.player.move(-3, app.playerShapes.rotateAngle)
    if "s" in key:
        app.player.move(3, app.playerShapes.rotateAngle)
    if "d" in key:
        app.playerShapes.rotateAngle += 3
        app.player.collide.rotateAngle = 0
    if "a" in key:
        app.playerShapes.rotateAngle -= 3
        app.player.collide.rotateAngle = 0
    if app.signsGroup.hits(app.playerShapes.centerX, app.playerShapes.centerY) and not app.inSign:
        GameUtils.displayMessage(0, "this is a sign", "you are reading", "it right now.", [])
        app.inSign = True
    app.inSign = app.signsGroup.hits(app.playerShapes.centerX, app.playerShapes.centerY)
        
def onKeyPress(key):
    if key == "space" and not app.swordSwing:
        app.swordSwing = True
        if app.enemies.hitsShape(app.player.swordArc):
            for enemy in app.enemyList:
                if enemy.sprite.hitsShape(app.player.swordArc):
                    enemy.damage(20)
    elif key == "p":
        if not GameUtils.paused:
            GameUtils.pause()
        else:
            GameUtils.unpause()
        
def onMousePress(posX, posY):
    # This code is so awful but its kinda required because this is the only
    # way for the engine to interpret mouse presses /shrug
    
    # Detecting clicks on the title screen
    if GameUtils.titleActive:
        if GameUtils.playButton.hits(posX, posY):
            GameUtils.continued = False
            GameUtils.playGame()
        elif GameUtils.loadSaveButton.hits(posX, posY):
            try:
                saveString = app.getTextInput("Please enter save code or \"X\" to cancel.")
            except:
                return
            if saveString == "" or saveString.lower() == "x":
                return
            GameUtils.loadSave(saveString)
        elif GameUtils.creditsButton.hits(posX, posY):
            return
    elif GameUtils.paused:
        if GameUtils.resumeButton.hits(posX, posY):
            GameUtils.unpause()
        elif GameUtils.menuButton.hits(posX, posY):
            GameUtils.returnToMenu()
        elif GameUtils.okButton.hits(posX, posY):
            GameUtils.paused = False
            GameUtils.titleScreen()
    
    # Displaying response messages based on what option the player has clicked in a dialogue box
    elif GameUtils.messageId != -1:
        if GameUtils.messageId == 0: # Default text box, has an ok button this will clear it.
            if GameUtils.messageOption1.hits(posX, posY):
                GameUtils.clearMessage()
        elif GameUtils.messageId == -2: # Negative values are reserved for testing dialogue
            GameUtils.clearMessage()
            if GameUtils.messageOption1.hits(posX, posY):
                GameUtils.displayMessage(0, "you just pressed", "the continue button!", "cool.", [])
            elif GameUtils.messageOption2.hits(posX, posY):
                GameUtils.displayMessage(0, "i was testing", "", "", [])
            elif GameUtils.messageOption3.hits(posX, posY):
                GameUtils.displayMessage(-3, "greetings. how are", "you on this fine", "day???", ["good", "alright"])
        elif GameUtils.messageId == -3: # Negative values are reserved for testing dialogue
            GameUtils.clearMessage()
            if GameUtils.messageOption1.hits(posX, posY):
                GameUtils.displayMessage(0, "that is nice", "", "", [])
            elif GameUtils.messageOption2.hits(posX, posY):
                GameUtils.displayMessage(0, "just alright?", "fine.", "", [])
                
def onStep():
    app.frameCount += 1 # This variable is used to control the time between things like enemy attacks
    
    # Player health regen
    if app.frameCount % 15 == 0 and app.player.hp < 100:
        # Health should always be an even number to prevent healing over 100hp
        if app.player.hp % 2 != 0:
            app.player.hp += 1
        else:
            app.player.hp += 2
        # Call to the damage function to update the health bar on screen, otherwise you wouldnt be able to see the regeneration
        app.player.damage(0)
    
    # Sword swing animation played when the player swings their sword
    if app.swordSwing and app.player.sword.rotateAngle < app.playerShapes.rotateAngle + 60:
        app.player.swordFront.opacity = 100
        app.player.sword.rotateAngle += 8
    else:
        app.player.swordFront.opacity = 0
        app.player.sword.rotateAngle = app.playerShapes.rotateAngle + -60
        app.swordSwing = False
        
    # Enemy attacking player code
    for enemy in app.enemyList:
        # Look through each enemy and see if they are ready to shoot, otherwise advance the arrow one step
        if enemy.nextShot < app.frameCount:
            enemy.attackPlayer()
        else:
            enemy.advanceArrow()
            
    if app.player.fadePlaying != 0:
        app.player.fadeAnim()
        
GameUtils.titleScreen()
cmu_graphics.run()

#Enemy("thing", 100, 430, 370)
        
#   Main Goals:
#   1. make map better (mostly finished)
#   2. Dialogue Box w/ option picker (basically done)
#   3. Weapon/Damage system (basically done)
#   4. Building Interiors w/ shops?
#   5. Dungeons?
#   6. Inventory System (not happening)
#   7a.Saving system using save codes (mostly finished)
#   7b.Loading previous saves using save codes. (mostly finished)
#   8. Fishing system
#   9. Enemy AI/movement (have them move toward players?) (optional)