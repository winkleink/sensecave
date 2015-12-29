#!/usr/bin/python

# Simple lettle game using Sense Hat for cave exploring

from sense_hat import SenseHat
import os
import time
import pygame  # See http://www.pygame.org/docs
from pygame.locals import *
from random import randint
import math


print("Press Escape to quit")
time.sleep(1)

# setting up pygame - will change to dummy later so can work headless
pygame.init()
pygame.display.set_mode((640, 480))

sense = SenseHat()
sense.clear()  # Blank the LED matrix

# variable to stay in program
running = True


r = (255,0,0)
g = (0,255,0)
b = (0,0,0)
w = (255,255,255)

x = 1
y = 1

# Function to draw a single cell. Withe the opens if there
def draw_sense(cell):
    sense.clear()  # Blank the LED matrix
   
    for side in range (0,8):
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


# Move cells around based on key press
def handle_event(event, x,y):
    if event.key == pygame.K_DOWN:
        y +=1
        if y == 8:
				y = 7
        
    elif event.key == pygame.K_UP:
        y -=1
        if y == -1:
				y = 0       

    elif event.key == pygame.K_LEFT:
        x -=1
        if x == -1:
				x = 0
                
    elif event.key == pygame.K_RIGHT:
        x +=1
        if x == 8:
				x = 7
   
        
#    elif event.key == pygame.K_RETURN:
    return (x, y)       


# blank empty edge
maze = [[144,128,128,128,128,128,128,192],
        [16,0,0,0,0,0,0,64],
        [16,0,0,0,0,0,0,64],
        [16,0,0,0,0,0,0,64],
        [16,0,0,0,0,0,0,64],
        [16,0,0,0,0,0,0,64],
        [16,0,0,0,0,0,0,64],
        [48,32,32,32,32,32,32,96]]

for extra in range (0,10):
    xrand = randint(0,7)
    yrand = randint(0,7)
	
    siderand = randint(0,3)
    if True:
#    if maze[xrand][yrand] & 126 == False:
        print "xrand "+ str(xrand)
        print "yrand " + str(yrand)
        print "siderand " + str(siderand)
        print "siderand power is "+ str(int(math.pow(2, siderand+4)))
        print "maze before or "+ str(maze[yrand][xrand])
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
	
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            print "KEY DOWN"
            if event.key == K_ESCAPE:
                running = False
            x,y = handle_event(event, x, y)
            print x
            print y
            print maze[y][x]
            draw_sense(maze[y][x])
            if y == 0 and x == 0:
                sense.set_pixel(1,1,255,0,0)
            elif y == 0 and x == 7:
                sense.set_pixel(6,1,255,0,0)
            elif y == 7 and x == 0:
                sense.set_pixel(1,6,255,0,0)
            elif y == 7 and x == 7:
                sense.set_pixel(6,6,255,0,0)

            if event.key == K_RETURN:
                running = False            

print "EXIT!"            
sense.clear()  # Blank the LED matrix
            
            



