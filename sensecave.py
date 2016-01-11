#!/usr/bin/python

# Simple little game using Sense Hat for cave exploring
# 8 x 8 maze with 7 green emeraldss to find 
# Exit is bottom Right

# top - 128
# right - 64
# bottom - 32
# left - 16
# diamond - 1 and coloured green
# exit is white bottom right of maze

from sense_hat import SenseHat
import os
from time import sleep
# import pygame  # See http://www.pygame.org/docs
# from pygame.locals import *
from random import randint
import math


print("Press Escape to quit")
sleep(1)

# setting up pygame - will change to dummy later so can work headless
# os.environ["SDL_VIDEODRIVER"] = "dummy"
# pygame.init()
# pygame.display.set_mode((1,1))
# display = pygame.display.set_mode((320, 240))

sense = SenseHat()
sense.clear()  # Blank the LED matrix
sense.low_light = True

# Some colours not used yet
r = (255,0,0)
g = (0,255,0)
b = (0,0,0)
w = (255,255,255)
score = 0 # have you found 7 emeralds
running = True # is the program running
ingame = True # is a game being played

# starting x and y co-ordinates to define maze cell.
# for true x,y then y is first in maze[]
x = 1
y = 7

# starting x and y for players dot in a cell
dotx = 2
doty = 2

# Function to draw a single cell. With the openings if there are any
def draw_sense(cell):
    sense.clear()  # Blank the LED matrix
   
    for side in range (0,8):
		
        # add the gap in the side if the side is suppose to be open
        if side == 3 or side == 4:
            if( cell & 128) == 128:
                sense.set_pixel(side,0,255,0,0)
            else:
                sense.set_pixel(side,0,0,0,0)
		    
            if( cell & 32) == 32:
                sense.set_pixel(side,7,255,0,0)
            else:
                sense.set_pixel(side,7,0,0,0)
		    
            if( cell & 16) == 16:
                sense.set_pixel(0,side,255,0,0)
            else:
                sense.set_pixel(0,side,0,0,0)
		    
            if( cell & 64) == 64:
                sense.set_pixel(7,side,255,0,0)
            else:
                sense.set_pixel(7,side,0,0,0)
        else:
			sense.set_pixel(0,side,255,0,0)
			sense.set_pixel(7,side,255,0,0)
			sense.set_pixel(side,0,255,0,0)
			sense.set_pixel(side,7,255,0,0)
    # if a corner put an extra dot in the corner.
    if y == 0 and x == 0:
        sense.set_pixel(1,1,255,0,0)
    elif y == 0 and x == 7:
        sense.set_pixel(6,1,255,0,0)
    elif y == 7 and x == 0:
        sense.set_pixel(1,6,255,0,0)
    elif y == 7 and x == 7:
        sense.set_pixel(6,6,255,255,255)
            
    if maze[y][x] & 1 == 1: # draw diamond
        sense.set_pixel(3,3,0,255,0)


# Move between cells based on key press - not needed for game, but useful cheat
#def handle_event(event, x,y):
#    if event.key == pygame.K_DOWN:
#        y +=1
#        if y == 8:
#				y = 7
        
#    elif event.key == pygame.K_UP:
#        y -=1
#        if y == -1:
#				y = 0       

#    elif event.key == pygame.K_LEFT:
#        x -=1
#        if x == -1:
#				x = 0
                
#    elif event.key == pygame.K_RIGHT:
#        x +=1
#        if x == 8:
#				x = 7
   
        
#    elif event.key == pygame.K_RETURN:
#    return (x, y)       


# move the players dot around the SenseHat
def move_dot(pitch,roll,dotx,doty):
    new_dotx = dotx
    new_doty = doty
    if 1 < pitch < 170:
        new_dotx -= 1
    elif 359 > pitch > 189:
        new_dotx += 1
    if 1 < roll < 170:
        new_doty += 1
    elif 359 > roll > 189:
        new_doty -= 1
    if new_dotx < -1:
		new_dotx=-1
    if new_dotx > 8:
        new_dotx = 8
    if new_doty < -1:
        new_doty = -1
    if new_doty > 8:
        new_doty = 8
 
    return new_dotx,new_doty


def add_walls():
    # add 10 random walls to make the maze more interesting
    for extra in range (0,10):
        xrand = randint(0,7)
        yrand = randint(0,7)
	
        siderand = randint(0,3)

        print "xrand "+ str(xrand)
        print "yrand " + str(yrand)
        print "siderand " + str(siderand)
        print "siderand power is "+ str(int(math.pow(2, siderand+4)))
        print "maze before or "+ str(maze[yrand][xrand])
        if maze[yrand][xrand] + pow(2,siderand+4) != 240: # make sure no cell is completely blocked in
            maze[yrand][xrand] = maze[yrand][xrand] | int(math.pow(2,siderand+4))
            print "maze after or " + str(maze[yrand][xrand])
    
            if siderand == 0: # set cell to the left closed also
                if xrand != 0:
                    maze[yrand][xrand-1] = maze[yrand][xrand-1] | 64

            if siderand == 1: # set cell to the left closed also
                if yrand != 7:
                    maze[yrand+1][xrand] = maze[yrand+1][xrand] | 128

            if siderand == 2: # set cell to the left closed also
                if xrand !=7:
                    maze[yrand][xrand+1] = maze[yrand][xrand+1] | 16

            if siderand == 3: # set cell to the left closed also
                if yrand != 0:
                    maze[yrand-1][xrand] = maze[yrand-1][xrand] | 32

def add_diamonds():
    # Add 7 'diamonds' to find as number 1
    for diamond in range (0,7):
        xrand = randint(0,7)
        yrand = randint(0,7)
        # Keep picking new cells if a diamond is already in a cell or if the cell is enclosed.
        while (maze[yrand][xrand] & 1 == 1) or (maze[yrand][xrand] & 240 == 240):
            xrand = randint(0,7)
            yrand = randint(0,7)

        maze[yrand][xrand] = maze[yrand][xrand] | 1
    

while running:
    x = 1
    y = 7
    dotx = 3
    doty = 3
    score = 0
 
    ingame = True
    sleep(1)
    sense.show_message("Next Game in...", text_colour=[255,255,255])

    for loop in range (5,0,-1):
        sense.show_message(str(loop), text_colour=[255,255,255])

# blank empty edge
    maze = [[144,128,128,128,128,128,128,192],
            [16,0,0,0,0,0,0,64],
            [16,0,0,0,0,0,0,64],
            [16,0,0,0,0,0,0,64],
            [16,0,0,0,0,0,0,64],
            [16,0,0,0,0,0,0,64],
            [16,0,0,0,0,0,0,64],
            [48,32,32,32,32,32,32,96]]

# add the internal walls
    add_walls()

# add the diamonds
    add_diamonds()

    draw_sense(maze[y][x])
    sleep (2)
# main loop for program
    while ingame:
        print "dotx = " + str(dotx) + "  | doty " + str(doty)
        pitch = sense.get_orientation()['pitch']
        roll = sense.get_orientation()['roll']
#       print "pitch " + str(pitch)
#       print "roll " + str(roll )
        sense.set_pixel(dotx,doty,0,0,0)
        old_dotx = dotx
        old_doty = doty
        dotx,doty = move_dot(pitch,roll,dotx,doty)
        print "newdotx = " + str(dotx) + " | newdoty = " + str(doty)
        if (dotx > -1 and dotx <8) and (doty > -1 and doty <8):
            check_dot = sense.get_pixel(dotx, doty)
            if check_dot == [248,0,0]:
                print "red"
                dotx = old_dotx
                doty = old_doty
        
            if check_dot == [0,252,0]: # green
                score +=1
                sense.show_letter(str(score))
                sleep(1)
                maze[y][x] = maze[y][x] - 1
                sense.clear
                draw_sense(maze[y][x])
        
            # Have you found all 7
                if score == 7:
                    sense.clear
                    sense.show_message("Go to Exit!", text_colour=[255, 0, 0])
                    sense.clear
                    draw_sense(maze[y][x])
            
            if check_dot == [248, 252, 248 ] and score == 7: # white
                sense.clear
                sense.show_message("You have escaped with alll the emeralds!  Well done", text_colour=[255,255,255])
                ingame = False 
            
        
        
       # if at the edge - need to fix for 
        if (dotx == 8 or dotx == -1 or doty == 8 or doty== -1):
       
            print "I'm at the edge"    
            if doty == -1:
                print "doty inside = -1"
                doty = 7
                y -= 1
                if y == -1:
                    y = 0
                
            elif doty == 8:
                print "doty inside = 8"
                doty = 0
                y += 1
                if y == 8:
                    y = 7
                
            elif dotx == -1:
                print "dotx inside = -1"
                dotx = 7
                x -= 1
                if x == -1:
                    x = 0

            elif dotx == 8:
                print "dotx inside = 8"
                dotx = 0
                x += 1
                if x == 8:
                    x = 7
                
            if dotx != old_dotx or doty != old_doty:
                print "before drawing"
                print "x " + str(x)
                print "y " + str(y)
                draw_sense(maze[y][x])

            print "x " + str(x)
            print "y " + str(y)
            print "dotx " + str(dotx)
            print "doty " + str(doty)
        
        
            
        sense.set_pixel(dotx,doty,0,0,255)
        sleep(0.15)
#        pygame.event.pump()
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                ingame = False
#            if event.type == KEYDOWN:
#                print "KEY DOWN"
#                if event.key == K_ESCAPE:
#                    ingame = False
#                x,y = handle_event(event, x, y)
#                print x
#                print y
#                print maze[y][x]
           # draw the cell
#                draw_sense(maze[y][x])

               
           # if [return pressed] exit program
#                if event.key == K_RETURN:
#                    imgame = False
#                    running = False            

print "EXIT!"            
sense.clear()  # Blank the LED matrix
            
            



