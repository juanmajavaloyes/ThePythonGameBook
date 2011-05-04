# -*- coding: utf-8 -*-
"""
step007.py
loading images (from subfolder) and dirtyrects
url: http://thepythongamebook.com/en:part2:pygame:step007
author: horst.jens@spielend-programmieren.at

press p to toggle painting of pretty background
press d to toggle dirtyrect painting 
press c to restore the ugly image

pretty Venus image from:
http://en.wikipedia.org/wiki/File:La_naissance_de_V%C3%A9nus.jpg
http://commons.wikimedia.org/wiki/Sandro_Botticelli

ugly image from Horst JENS
"""
import pygame
import random
import os
pygame.init()
screen=pygame.display.set_mode((800,470)) # try out larger values and see what happens !
screenrect = screen.get_rect()
# mypicture = pygame.image.load("picturefile.jpg") # simple method if picture in same folder
folder = "data" # replace with "." if pictures lay in the same folder as program
prettybackground = pygame.image.load(os.path.join(folder, "800px-La_naissance_de_Venus.jpg"))
prettybackground = prettybackground.convert()  #convert (no alpha! because no tranparent parts) for faster blitting
uglybackground = pygame.image.load(os.path.join(folder, "background800x470.jpg"))
uglybackground = uglybackground.convert() # no alpha !
background = uglybackground.copy() # the actual background
snakesurface = pygame.image.load(os.path.join(folder,"snake.gif")) # with tranparent colour
snakesurface = snakesurface.convert_alpha()
snakerect = snakesurface.get_rect()
x = 1     # start position for the snake surface (topleft corner)
y = 1             
dx,dy  = 40, 85                    # speed of ball surface in pixel per second !
screen.blit(uglybackground, (0,0))     #blit the background on screen (overwriting all)
screen.blit(snakesurface, (x, y))  #blit the ball surface on the screen (on top of background)
clock = pygame.time.Clock()        #create pygame clock object
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0
painting = False # do not overpaint the ugly background yet
dirty = False # do clear dirty part of screen

while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC

            elif event.key == pygame.K_c: # restore old background
                background = uglybackground.copy() # the old ugly background
                screen.blit(uglybackground,(0,0))
                print "ugly background restored!"
            elif event.key == pygame.K_p: # paint pretty background
                painting = not painting # toggle
                print "painting is now set to %s" % painting
            elif event.key == pygame.K_d:
                dirty = not dirty # toggle
                print "dirty is now set to %s" % dirtyrect
                
    
    
    pygame.display.set_caption("[FPS]: %.2f dx:%i dy:%i p:"
    "toggle paint, d: toggle dirtyrect, c: restore" % (clock.get_fps(), dx, dy))
    #this would repaint the whole screen (secure, but slow)
    #screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    #this only repaints the "dirty" part of the screen
    if not dirty: # calculate dirtyrect and blit it
        dirtyrect = background.subsurface((x,y,snakerect.width, snakerect.height))
        screen.blit(dirtyrect, (x,y))
    x += dx * seconds # float, since seconds passed since last frame is a decimal value
    y += dy * seconds 
    # bounce snake if out of screen
    if x < 0:
        x = 0
        dx *= -1 
        dx += random.randint(-15,15) # new random direction
    elif x + snakerect.width >= screenrect.width:
        ballx = screenrect.width - snakerect.width
        dx *= -1 
        dx += random.randint(-15,15) 
    if y < 0:
        y = 0
        dy *= -1
        dy += random.randint(-15,15) 
    elif y + snakerect.height >= screenrect.height:
        y = screenrect.height - snakerect.height
        dy *= -1 
        dy += random.randint(-15,15) 
    # paint the snake
    screen.blit(snakesurface, (x,y))
    # TV corner: paint a subsurface on the screen of this part of prettybackground
    # where snake is at the moment (rect argument)
    try:
        tvscreen = prettybackground.subsurface((x,y,snakerect.width, snakerect.height))
    except:
        print "some problem with subsurface"
    screen.blit(tvscreen, (0,0)) # blit into screen like a tv 
    if painting:
        background.blit(tvscreen, (x,y)) # blit from pretty background into background
    pygame.display.flip()          # flip the screen 30 times a second
print "This 'game' was played for %.2f seconds" % playtime