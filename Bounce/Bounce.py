from tkinter import *
from random import *
from time import *
root = Tk()
s = Canvas(root, width=1100, height=700, background="white")
s.pack()



########################
#    INITIAL VALUES    #
########################

def drawMap(): #Creates the map and sets up the scoreboard
    global map1, map2, map3, map4, map5, map6, map7, map8, map9
    
    map1 = s.create_rectangle(-10,675, 1110,705, fill = "grey", outline = "grey")
    map2 = s.create_rectangle(440,0, 660,55, fill = "black", outline = "black")
    map3 = s.create_rectangle(445,0, 545,50, fill = "red", outline = "red")
    map4 = s.create_rectangle(555,0, 655,50, fill = "red", outline = "red")
    map5 = s.create_text(495,25, font = "Helv 25", text = "Score")
    map6 = s.create_text(605,25, font = "Helv 25", text = "Lives")
    map7 = s.create_rectangle(490,55, 610,100, fill = "black", outline = "black")
    map8 = s.create_rectangle(495,56, 545,95, fill = "red", outline = "red")
    map9 = s.create_rectangle(555,56, 605,95, fill = "red", outline = "red")


def setInitialValues(): #Set initial values
    global frame, player, xPos, yPos, yPosStart, xSpeed, ySpeed, ySpeedGravity, score, invisibleScore, life, gameStart, playAgain, endGame, needHelp1, needHelp2, modeSelect, mouseDown, shoot, subtractLife, newTarget, projectionLine, scoreboard1, scoreboard2

    frame = 0 #Frame count for moving ball in a parabola
    player = 0
    xPos = 540
    yPos = 660
    yPosStart = yPos #Starting y position of the parabolic motion
    xSpeed = 1
    ySpeed = 1
    ySpeedGravity = 0
    score = 0 #The displayed score
    invisibleScore = score #The score used to determine the gamemode
    life = 4
    gameStart = False #Initial boolean values
    playAgain = False
    endGame = False
    needHelp1 = False
    needHelp2 = False
    modeSelect = False
    mouseDown = False
    shoot = True
    subtractLife = False
    newTarget = True
    projectionLine = 0
    scoreboard1 = s.create_text(520,76, font = "Helv 30", text = score) #Draws starting score and lives
    scoreboard2 = s.create_text(580,76, font = "Helv 30", text = life)
    drawPlayer()



############################
#    KEY/MOUSE HANDLERS    #
############################

def keyDownHandler(event): #Closes game when "q" is pressed
    if event.keysym.upper() == "Q":
        root.destroy()


def mouseMotionDetector(event): #Checks the location of the mouse
    global xEnd, yEnd
    
    if mouseDown == True: #Updates the end point of the projection line ONLY if the mouse is being held down
        xEnd = event.x
        yEnd = event.y
    
    
def mouseClickHandler(event): #Checks when the mouse is clicked
    global xStart, yStart, xEnd, yEnd, mouseDown
                
    if shoot == False: #Clicking only registers if ball is not moving
        
        xStart = event.x #Updates the points of the projection line
        yStart = event.y
        xEnd = event.x
        yEnd = event.y
        mouseDown = True

    
def mouseReleaseHandler(event): #Checks when the mouse is released 
    global xEnd, yEnd, mouseDown, shoot, subtractLife, life, gameStart, needHelp1, needHelp2, playAgain, modeSelect, invisibleScore
    
    if gameStart == False: #Pre-Game screens
        
        if modeSelect == True: #Buttons for the mode selection screen
            
            if 900 < event.x < 1050 and 575 < event.y < 650:
                modeSelect = False
            elif 200 < event.x < 350 and 325 < event.y < 400:
                gameStart = True
                invisibleScore = 5
            elif 475 < event.x < 625 and 325 < event.y < 400:
                gameStart = True
            elif 750 < event.x < 900 and 325 < event.y < 400:
                gameStart = True
                invisibleScore = 15
            elif 75 < event.x < 625 and 425 < event.y < 500:
                gameStart = True
                invisibleScore = 30
                
        elif needHelp1 == False and needHelp2 == False: #Buttons for either of the help screens
            
            if 300 < event.x < 450 and 325 < event.y < 400:
                modeSelect = True
            elif 650 < event.x < 800 and 325 < event.y < 400:
                needHelp1 = True
                
        else: #Buttons for the main menu
            
            if 900 < event.x < 1050 and 575 < event.y < 650:
                needHelp1 = not needHelp1
                needHelp2 = not needHelp2
            elif 900 < event.x < 1050 and 50 < event.y < 125:
                needHelp1 = False
                needHelp2 = False
            

    if endGame == True: #Buttons for the Post-Game screen
        
        if 300 < event.x < 450 and 325 < event.y < 400:
            playAgain = True
        elif 650 < event.x < 800 and 325 < event.y < 400:
            root.destroy()
                
    if shoot == False and gameStart == True: #While the game is running
        
        xEnd = event.x #Sets the end position of the projection line where the mouse is released
        yEnd = event.y
        mouseDown = False
        shoot = True
        subtractLife = True
        playerMovement()
        s.delete(projectionLine)



##################
#    UPDATING    #
##################

def playerMovement(): #Uses the difference between where the mouse was clicked and released to calculate the speed and direction the ball with move in
    global xSpeed, ySpeed

    xSpeed = -(xEnd - xStart) / 40 
    ySpeed = (yEnd - yStart) / 40
    
    if xSpeed > 10: #Limits the maximum speed
        xSpeed = 10
    elif xSpeed < -10:
        xSpeed = -10
    if ySpeed > 10:
        ySpeed = 10
    elif ySpeed < -9:
        ySpeed = -9

    
def updatePosition():
    global xPos, yPos, shoot, frame, xSpeed, ySpeed, yPosStart, ySpeedGravity
    
    if yStickyPlatform1 <= yPos <= yStickyPlatform1+100 and xPos <= 15 and shoot == False: #Checks if the ball is on the sticky platforms
        frame = 0
        yPosStart = yPos
        ySpeedGravity = (675 - yPosStart)/60 #Adds speed to the ball based on height(because of gravity)

    elif yStickyPlatform2 <= yPos <= yStickyPlatform2+100 and xPos >= 1085 and shoot == False:
        frame = 0
        yPosStart = yPos
        ySpeedGravity = (675 - yPosStart)/60

    elif yPos < 661 and shoot == True: #Updates the position of the ball
        frame = frame + 1
        xPos = xPos + xSpeed

        if xPos >= 1085: #Wall detection for the left and right edges of the screen
            xPos = 1085
            xSpeed = -xSpeed
        elif xPos <= 15:
            xPos = 15
            xSpeed = -xSpeed
            
        yPos = 0.05*frame**2 - ySpeed*frame + yPosStart
        
    else: #Updates values when the ball bounces on the ground
        frame = 0
        yPos = 660
        yPosStart = yPos
        ySpeed = ySpeed - ySpeedGravity 
        if ySpeed < -12: #Limits the maximum speed
            ySpeed = -12
        if ySpeed < 0:
            ySpeed = ySpeed* -1
            ySpeedGravity = 0
        elif ySpeed > 1 or xSpeed > 1: #Reduces the speed to 60% of the original speed
            xSpeed = xSpeed * 0.6  
            ySpeed = ySpeed * 0.6
        else: #Stops the ball from moving once its x and y speed is less than 1
            xSpeed = 0
            ySpeed = 0
            shoot = False


def pointScored():
    global newTarget, points, score, invisibleScore, life, subtractLife
    
    if yTarget-25 < yPos < yTarget+25 and xTarget-25 < xPos < xTarget+25: #Hit detection for ball on target
        score = score + 1
        invisibleScore = invisibleScore + 1 #Update score
        newTarget = True
        subtractLife = False
        if life < 4: #Adds a life if the target is hit with a maximum of 4 lives at a time
            life = life + 1
        drawScore()

    
def missedShot():
    global life, subtractLife, endGame
        
    if subtractLife == True and frame == 0 and xSpeed == 0 and ySpeed == 0: #After the balls stops bouncing, checks if target was not hit
        life = life - 1
        subtractLife = False
        drawScore()
        if life <= 0: #Ends game if you run out of lives
            endGame = True
    

def bounce():
    global xSpeed, ySpeed, frame, yPos, yPosStart, shoot
    
    if xBouncyPlatform <= xPos <= xBouncyPlatform+100 and yPos >= 660: #Checks if the ball touched the bouncy platform
        frame = 0
        yPos = 660
        yPosStart = yPos
        ySpeed = ySpeed * 1.8 #Increase speed by 180%
        xSpeed = xSpeed * 1.8
        if xSpeed > 13: #Limits the maximum speed
            xSpeed = 13
        elif xSpeed < -13:
            xSpeed = -13
        if ySpeed > 12:
            ySpeed = 12
        elif ySpeed < -12:
            ySpeed = -12

    elif yStickyPlatform1 <= yPos <= yStickyPlatform1+100 and xPos <= 15 and shoot == True: #Checks if the ball touched the sticky platform
        xSpeed = 0 #Stops the ball from moving
        ySpeed = 0
        shoot = False

    elif yStickyPlatform2 <= yPos <= yStickyPlatform2+100 and xPos >= 1085 and shoot == True:
        xSpeed = 0
        ySpeed = 0
        shoot = False



#################
#    DRAWING    #
#################
        
def drawPlatform(): #Draws the bouncy/sticky platforms
    global xBouncyPlatform, bouncyPlatform, yStickyPlatform1, yStickyPlatform2, stickyPlatform1, stickyPlatform2
    
    if newTarget == True: #If the target was hit, changes the position of the bouncy/sticky platforms
        xBouncyPlatform = randint(100,900)
        yStickyPlatform1 = randint(50,500)
        yStickyPlatform2 = randint(50,500)
        
    bouncyPlatform = s.create_line(xBouncyPlatform,675, xBouncyPlatform+100,675, width = 5, fill = "green")
    stickyPlatform1 = s.create_line(3,yStickyPlatform1, 3,yStickyPlatform1+100, width = 5, fill = "red")
    stickyPlatform2 = s.create_line(1100,yStickyPlatform2, 1100,yStickyPlatform2+100, width = 5, fill = "red")

    
def drawPlayer(): #Draws the player(blue ball)
    global player
    
    player = s.create_oval(xPos-15, yPos-15, xPos+15, yPos+15, fill = "blue", outline = "blue")


def drawProjection(): 
    global projectionLine
    
    if mouseDown == True: #Draws the projection line only if the mouse is held down
        s.delete(projectionLine)
        projectionLine = s.create_line(xStart,yStart, xEnd,yEnd, fill = "black", width = 2)


def drawTarget(): #Drawing and updating the target
    global xTarget, yTarget, newTarget, target, xTargetOriginal, yTargetOriginal, xTargetSpeed, yTargetSpeed
    
    if newTarget == True: #If the target was hit, creates a new target at a random position
        xTarget = randint(160,940)
        yTarget = randint(200,450)
        xTargetOriginal = xTarget
        yTargetOriginal = yTarget
        newTarget = False

        #Changes target movement based off the score
        if invisibleScore >= 30: 
            xTargetSpeed = randint(0,5)
            yTargetSpeed = randint(0,5)
        
        elif invisibleScore >= 25:
            xTargetSpeed = 3
            yTargetSpeed = 2
            
        elif invisibleScore >= 20:
            xTargetSpeed = 2
            yTargetSpeed = 3
            
        elif invisibleScore >= 15:
            xTargetSpeed = 1
            yTargetSpeed = 2
            
        elif invisibleScore >= 10:
            xTargetSpeed = 3
            yTargetSpeed = 0
            
        elif invisibleScore >= 5:
            xTargetSpeed = 1
            yTargetSpeed = 0

        else:
            xTargetSpeed = 0
            yTargetSpeed = 0

    xTarget = xTarget + xTargetSpeed #Updates target position
    yTarget = yTarget + yTargetSpeed
    
    if xTargetOriginal - xTarget >= 150 or xTarget - xTargetOriginal >= 150: #Keeps the target without a certain area of its original starting position
        xTargetSpeed = xTargetSpeed * -1

    if yTargetOriginal - yTarget >= 75 or yTarget - yTargetOriginal >= 75:
        yTargetSpeed = yTargetSpeed * -1

    target = s.create_rectangle(xTarget-10,yTarget-10, xTarget+10,yTarget+10, fill = "#15E406", outline = "#15E406")


def drawScore(): #Updates the score and life count onto the scoreboard
    global scoreboard1, scoreboard2
    
    s.delete(scoreboard1, scoreboard2)
    scoreboard1 = s.create_text(520,76, font = "Helv 30", text = score)
    scoreboard2 = s.create_text(580,76, font = "Helv 30", text = life)



######################
#    MENU SCREENS    #
######################

def menu(): #Shows the Pre-Game screens

    if modeSelect == True:
        modeScreen()
    elif needHelp1 == True:
        helpScreen1()
    elif needHelp2 == True:
        helpScreen2()
    else:
        homeScreen()


def homeScreen(): #Draws the main menu
    
    background = s.create_rectangle(0,0, 1100,700, fill = "black")
    title = s.create_text(550,200, font = "Helv 50 bold", fill = "white", text = "Bounce")
    playButton = s.create_rectangle(300,325, 450,400, fill = "red", activefill = "yellow", outline = "dark red", width = 8) #Play button
    playButtonText = s.create_text(375,358, font = "Helv 40", text = "\u25B6", fill = "black", activefill = "white")
    helpButton = s.create_rectangle(650,325, 800,400, fill = "blue", activefill = "yellow", outline = "dark blue", width = 8) #Help button
    helpButtonText = s.create_text(725,364, font = "Monaco 40", text = "\u003F", fill = "black", activefill = "white")

    s.update()
    s.delete(background, title, playButton, playButtonText, helpButton, helpButtonText)
    

def modeScreen(): #Draws the mode selection screen
    
    background = s.create_rectangle(0,0, 1100,700, fill = "black")
    title = s.create_text(550,200, font = "Helv 50 bold", fill = "white", text = "Select a Mode")
    backButton = s.create_rectangle(900,575, 1050,650, fill = "red", activefill = "yellow", outline = "dark red", width = 8) #Back button
    backButtonText = s.create_text(975,608, font = "Helv 40", text = "\u27F5", fill = "black", activefill = "white")
    sidewaysButton = s.create_rectangle(200,325, 350,400, fill = "blue", activefill = "white", outline = "dark blue", width = 8)
    sidewaysButtonText = s.create_text(275,361, font = "Helv 25", text = "Sideways", fill = "black")
    classicButton = s.create_rectangle(475,325, 625,400, fill = "red", activefill = "white", outline = "dark red", width = 8)
    classicButtonText = s.create_text(550,362, font = "Helv 24", text = "Classic", fill = "black")
    allwaysButton = s.create_rectangle(750,325, 900,400, fill = "green", activefill = "white", outline = "dark green", width = 8)
    allwaysButtonText = s.create_text(825,362, font = "Helv 24", text = "All Ways", fill = "black")
    randomButton = s.create_rectangle(475,425, 625,500, fill = "yellow", activefill = "white", outline = "dark orange", width = 8)
    randomButtonText = s.create_text(550,462, font = "Helv 24", text = "Random", fill = "black")
    
    s.update()
    s.delete(background, title, backButton, backButtonText, classicButton, classicButtonText, sidewaysButton, sidewaysButtonText, allwaysButton, allwaysButtonText, randomButton, randomButtonText)
    
    
def helpScreen1(): #Draws the first help screen
    
    background = s.create_rectangle(0,0, 1100,700, fill = "black")
    title = s.create_text(550,100, font = "Helv 50 bold", fill = "white", text = "HELP 1")
    homeButton = s.create_rectangle(900,50, 1050,125, fill = "blue", activefill = "yellow", outline = "dark blue", width = 8) #Home button
    homeButtonText = s.create_text(975,86, font = "Helv 40", text = "\u2302", fill = "black", activefill = "white")
    forwardButton = s.create_rectangle(900,575, 1050,650, fill = "red", activefill = "yellow", outline = "dark red", width = 8) #Forward button
    forwardButtonText = s.create_text(975,608, font = "Helv 40", text = "\u27F6", fill = "black", activefill = "white")
    instruction = s.create_text(550,280, font = "Helv 15", fill = "white", text = "The goal of the game is to aim and shoot the ball to hit the box on the screen.\nUse the click and release of the mouse to choose the power and direction of your shot. \n\nAs you hit more boxes, the box will begin to move around quicker and in more irregular patterns. \nYou get a life when you hit a target and can have a max of 4 lives at once. \nThe game ends when you run out of lives or press Q to exit the game.")
    #"Screenshots" of the game
    sbBack1 = s.create_rectangle(430,390, 670,510, fill = "white") 
    sbBack2 = s.create_rectangle(440,400, 660,455, fill = "black", outline = "black")
    sbMid1 = s.create_rectangle(445,400, 545,450, fill = "red", outline = "red")
    sbMid2 = s.create_rectangle(555,400, 655,450, fill = "red", outline = "red")
    sbText1 = s.create_text(495,425, font = "Helv 25", text = "Score")
    sbText2 = s.create_text(605,425, font = "Helv 25", text = "Lives")
    sbBack3 = s.create_rectangle(490,455, 610,500, fill = "black", outline = "black")
    sbMid3 = s.create_rectangle(495,456, 545,495, fill = "red", outline = "red")
    sbMid4 = s.create_rectangle(555,456, 605,495, fill = "red", outline = "red")
    score1 = s.create_text(520,476, font = "Helv 30", text = "6")
    score2 = s.create_text(580,476, font = "Helv 30", text = "3")
    player = s.create_oval(250, 440, 280, 470, fill = "blue", outline = "blue")
    target = s.create_rectangle(825,445, 845,465, fill = "#15E406", outline = "#15E406")
    text1 = s.create_text(265,520, font = "Helv 25", fill = "white", text = "Ball")
    text2 = s.create_text(835,520, font = "Helv 25", fill = "white", text = "Target")
    text3 = s.create_text(550,560, font = "Helv 25", fill = "white", text = "Scoreboard")
    
    s.update()
    s.delete(background, title, homeButton, homeButtonText, forwardButton, forwardButtonText, instruction, sbBack1, sbBack2, sbMid1, sbMid2, sbText1, sbText2, sbBack3, sbMid3, sbMid4, score1, score2, player, target, text1, text2, text3)


def helpScreen2(): #Draws the second help screen
    
    background = s.create_rectangle(0,0, 1100,700, fill = "black")
    title = s.create_text(550,100, font = "Helv 50 bold", fill = "white", text = "HELP 2")
    homeButton = s.create_rectangle(900,50, 1050,125, fill = "blue", activefill = "yellow", outline = "dark blue", width = 8) #Home button
    homeButtonText = s.create_text(975,86, font = "Helv 40", text = "\u2302", fill = "black", activefill = "white")
    backButton = s.create_rectangle(900,575, 1050,650, fill = "red", activefill = "yellow", outline = "dark red", width = 8) #Back button
    backButtonText = s.create_text(975,608, font = "Helv 40", text = "\u27F5", fill = "black", activefill = "white")
    instruction = s.create_text(550,280, font = "Helv 15", fill = "white", text = "On the floor and walls of the map, green and red platforms will appear. \nThe green platforms act as bouncy platforms and increase the speed of the ball. \nThe red platforms act as sticky platforms and stop the ball from moving left and right, \nresulting in an almost certain loss of a life.")
    bouncyPlatform = s.create_line(300,450, 400,450, width = 5, fill = "green")
    stickyPlatform = s.create_line(750,400, 750,500, width = 5, fill = "red")
    text1 = s.create_text(350,550, font = "Helv 25", fill = "white", text = "Bouncy Platform")
    text2 = s.create_text(750,550, font = "Helv 25", fill = "white", text = "Sticky Platform")

    s.update()
    s.delete(background, title, homeButton, homeButtonText, backButton, backButtonText, instruction, bouncyPlatform, stickyPlatform, text1, text2)


def endScreen(): #Draws the Post-Game end screen
    
    background = s.create_rectangle(0,0, 1100,700, fill = "black")
    title = s.create_text(550,200, font = "Helv 50 bold", fill = "white", text = "THANKS FOR PLAYING")
    playAgainButton = s.create_rectangle(300,325, 450,400, fill = "red", activefill = "yellow", outline = "dark red", width = 8) #Play Again button
    playAgainButtonText = s.create_text(375,358, font = "Helv 40", text = "\u27F3")
    quitButton = s.create_rectangle(650,325, 800,400, fill = "blue", activefill = "yellow", outline = "dark blue", width = 8) #Quit button
    quitButtonText = s.create_text(725,362, font = "Helv 25", text = "\u2715")

    s.update()
    s.delete(background, title, playAgainButton, playAgainButtonText, quitButton, quitButtonText)



################################
#    MAIN RUN GAME FUNCTION    #
################################
    
def runGame(): #Main runGame function
    global playAgain
    playAgain = True #Allows the main loop to start
    
    while playAgain == True: #Main Loop 
        
        drawMap()
        setInitialValues()
        
        while gameStart == False: #Pre-Game screens loop
            menu()
            
        s.delete(player)
        
        while life > 0 and gameStart == True: #Game Loop
            
            drawPlatform()
            drawTarget()
            drawPlayer()
            drawProjection()
            updatePosition()
            bounce()
            pointScored()
            missedShot()
            s.update()
            sleep(0.01)
            s.delete(player, target, bouncyPlatform, stickyPlatform1, stickyPlatform2)

        s.delete(map1, map2, map3, map4, map5, map6, map7, map8, map9, scoreboard1, scoreboard2) #Deletes everything remaining
        
        while playAgain == False: #Post-Game screen loop
            endScreen()

    
        
#####################
#    KEY BINDING    #
#####################

root.after(100, runGame)
s.bind("<Key>",  keyDownHandler )
s.bind("<Motion>", mouseMotionDetector)
s.bind("<Button-1>", mouseClickHandler)
s.bind("<ButtonRelease-1>", mouseReleaseHandler) 

s.focus_set()
s.pack()
root.mainloop()
