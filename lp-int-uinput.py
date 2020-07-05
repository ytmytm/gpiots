
import pygame
import os
import random
import time
import sys
import uinput

PAL_LINE_LENGTH=64
LP_DEVICE="/dev/gpiots0"

# screensize
SCREEN_WIDTH=640
SCREEN_HEIGHT=480

# setup
os.putenv("SDL_FBDEV","/dev/fb0")
os.putenv('SDL_VIDEODRIVER', 'fbcon')
BLACK = (0,0,0)
WHITE = (192,192,192)

# uinput setup
events = (
    uinput.ABS_X + (0, SCREEN_WIDTH, 0, 0),
    uinput.ABS_Y + (0, SCREEN_HEIGHT, 0, 0),
    uinput.BTN_LEFT,
    uinput.BTN_JOYSTICK
    )

# screen setup
pygame.init()
pygame.mouse.set_visible(True)
lcd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
lcd.fill(BLACK)
pygame.display.update()

font_big = pygame.font.Font(None, 48)

text_surface = font_big.render('Hello', True, WHITE)
but_surface = font_big.render("Fire!", True, WHITE)

def get_raw_coords():
    with open(LP_DEVICE) as f:
        line = f.readline().strip().split(",")
        return [ int(x) for x in line ]

def get_on_button_release():
        but = 1
        while but==1:
            (col,line,but) = get_raw_coords()
        while but==0:
            (col,line,but) = get_raw_coords()
        return (col,line)

def cal_box_draw(x,y,text):
    rect = (x,y,64,64)
    text_surface = font_big.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    lcd.fill(BLACK)
    pygame.draw.rect(lcd,(64,64,64),rect)
    lcd.blit(text_surface, text_rect)
    pygame.display.update()


print("top left")
cal_box_draw(0,0,"top left")
cal_topleft = get_on_button_release()
print("top left is "+str(cal_topleft))

print("top right")
cal_box_draw(SCREEN_WIDTH-64,0,"top right")
cal_topright = get_on_button_release()
print("top right is "+str(cal_topright))

print("bottom right")
cal_box_draw(SCREEN_WIDTH-64,SCREEN_HEIGHT-64,"bottom right")
cal_botright = get_on_button_release()
print("bottom right is "+str(cal_botright))

print("bottom left")
cal_box_draw(0,SCREEN_HEIGHT-64,"bottom left")
cal_botleft = get_on_button_release()
print("bottom left is "+str(cal_botleft))

print("center")
cal_box_draw(SCREEN_WIDTH/2-64/2,SCREEN_HEIGHT/2-64/2,"center")
cal_center = get_on_button_release()
print("center is "+str(cal_center))

pygame.quit()

#
# XXX calibration parameters - 8x unsigned ints
# XXX in case I would rewrite whole thing as a kernel module then all parameters
# XXX (see the loop below) are already integers
# XXX there must be an interface to setup calibration parameters from userspace
#     (through a dedicated program, like this one)
# XXX kernel should calculate x/y raw positions from vsync/timing, convert to screen x/y and push as a touch event
#
cal_offsx = cal_topleft[0]
cal_rangex = abs(cal_botright[0]-cal_topleft[0])
cal_scalex = int(256*SCREEN_WIDTH/(cal_rangex)) # 16 bit precision fixed-point integer (8.8)
cal_offsy = cal_topleft[1]
cal_rangey = abs(cal_botright[1]-cal_topleft[1]) # 16 bit precision fixed-point integer (8.8)
cal_scaley = int(256*SCREEN_HEIGHT/(cal_rangey))

# XXX separate calibration for each screen quarter, this is TL-BR diagonal only
print("scaling:")
print("offset\tx = "+str(cal_offsx)+"\t\t y = "+str(cal_offsy))
print("range\tx = "+str(cal_rangex)+"\t\t y = "+str(cal_rangey))
print("scale\tx = "+str(cal_scalex)+"\t y = "+str(cal_scaley))

lastbut = 1
with uinput.Device(events) as device:
  with open(LP_DEVICE) as f:
    for line in f:
#        print(line)
        line = line.strip().split(",")
        (col,line,but) = [ int(x) for x in line ]
        # bitshift to go from 8.8 fixed-point to integers
        y = max(min(((line-cal_offsy)*cal_scaley) >> 8, SCREEN_HEIGHT), 0)
        x = max(min(((col-cal_offsx)*cal_scalex) >> 8, SCREEN_WIDTH), 0)

#        print("x="+str(x)+",y="+str(y)+"\tline="+str(line)+",col="+str(col)+"\n")
        if but!=lastbut:
            device.emit(uinput.BTN_LEFT, 1-but)
#        if ((but==0) and (lastbut==1)):
#            device.emit_click(uinput.BTN_LEFT, syn=False)
#            device.emit_click(uinput.BTN_JOYSTICK, syn=False)
        device.emit(uinput.ABS_X, x, syn=False)
        device.emit(uinput.ABS_Y, y)
        lastbut = but
