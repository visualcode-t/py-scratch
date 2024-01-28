import json

from py_scratch import *
import time as pytime #for some reason pygame also has a time library
#physics variables
momentumx = 0.0

gravity =4
momentumy = gravity
gamespeed = 20 # higher this value is, the choppier+slower the physics runs
friction = 1.0
inAir = True
jumpPower = 9

lastframe = pytime.time()

def main():
    global lastframe, momentumx, friction, gravity, inAir, momentumy

    #game.img_add_image(".\\images\\platform.png",0,0,(255,255,255),"bg.png")
    game.img_add_image(".\\images\\mg.png",0,0,(255,255,255),"mg")
    game.img_add_image(".\\images\\death.png",0,0,(255,255,255),"death")
    
    delay = pytime.time() - lastframe
    if game.img_add_image(".\\images\\a.png",0,0,(255,255,255),"bmp") == True:
        try:
            game.img_set_x("bmp",50)
            game.img_set_y("bmp",200)
        except Exception as e:
            print (e)
            pass
    
    
    
    if delay > gamespeed/1000:
        touching = game.img_move_y("bmp", momentumy, False)
        game.img_move_x("bmp", momentumx, False)
        if momentumx !=0:
            if momentumx > 0:
                momentumx-=friction
            elif momentumx <0:
                momentumx += friction
            if momentumx < 0.2 and momentumx > -0.2:
                momentumx = 0
        if momentumy !=0:
            if momentumy > gravity:
                momentumy-=0.3
            elif momentumy <gravity:
                momentumy += 0.3
            if momentumy < gravity + 0.2 and momentumy >  gravity -0.2:
                momentumy = gravity
        lastframe = pytime.time()
        if touching == "death":
            game.img_set_x("bmp",50)
            game.img_set_y("bmp",200)
        if touching:
            inAir=False
            friction = 1
            momentumx = momentumx/50
            momentumy = gravity
            #print(momentumx)
        elif touching == False:
            inAir=True
            friction = 0.1
        print(momentumy)
    


def keys(key):
    global amount, amount2, gamespeed, momentumx, momentumy, inAir, jumpPower
    if key[K_RIGHT]:
        if momentumx < 5:
            momentumx +=2
    if key[K_LEFT]:
        if momentumx > -5:
            momentumx-=2
    if key[K_SPACE]:
        if inAir == False:
            if momentumy > -jumpPower:
                momentumy-=gravity + jumpPower
    #if key[K_UP]:
    #    game.img_move_y("bmp", -5, True)
    if key[K_DOWN]:
        game.img_move_y("bmp", 5, True)




amount = 50
amount2 = 50

game = pgDisplay()
game.d_title("Platformer")
game.d_set_bg("cyan")
game.d_watch_keys(keys)
game.d_start(main)
