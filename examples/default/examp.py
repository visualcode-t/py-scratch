import json

from py_scratch import *


def main():
    if game.img_add_image(".\\images\\a.bmp",0,0,(255,255,255),"bmp") == True:
        try:
            data = open(".\\images\\bmp.txt")
            data = json.load(data)
            print (data)
            game.img_set_x("bmp",data["bmp"]["X"])
            game.img_set_y("bmp",data["bmp"]["Y"])
        except Exception as e:
            print (e)
            pass
    game.img_add_image(".\\images\\a.bmp",500,100,(255,255,255),"bmp2")
    game.img_add_image(".\\images\\a.png",300,300,(255,255,255),"png")
    data = {
        "bmp": {
            "X": game.img_get_x("bmp"),
            "Y": game.img_get_y("bmp"),
        }
    }
    with open ("bmp.txt",'w') as write:
        json.dump(data,write)


def keys(key):
    global amount, amount2
    if key[K_LEFT]:
        if amount >= 5:
            game.img_change_rotate("bmp",5,False)
            amount -= 5
            amount2 += 5
    if key[K_RIGHT]:
        if amount2 >= 5:
            game.img_change_rotate("bmp",-5,False)
            amount2-=5
            amount +=5
    if key[K_UP]:
        game.img_move("bmp",5,False)
    if key[K_DOWN]:
        game.img_move("bmp",-5,False)
    if key[K_LSHIFT]:
        game.img_change_size("bmp",-5,False)
    if key[K_RSHIFT]:
        game.img_change_size("bmp",+5,False)

amount = 50
amount2 = 50
game = pgDisplay()
game.d_title("Example")
game.d_set_bg("Green")
game.d_watch_keys(keys) 
game.d_start(main)
