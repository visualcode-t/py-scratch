from pygame import *
import sys
from timeit import default_timer
import random
import os.path
import math

from copy import copy

#Fix shade
#Fix size

#Collision:
    #Consider sprite groups
    #Need a method of restricting movement into and through objects
    #auto-collision - Alerts similar to mouse and key
    # *any* is used for internal collision and needs to be expanded for edges and more.


#changing of image needs a fn so that we don't lose things like the mask and etc
#fix shade (coloreffect)
#fix size


#Backgrounds - Build an image that fits the screen, allow stretch or tile

#mouse
    #Callback made
    #need button status

#Need image cache


class pgDisplay():
    running = False
    fps = 60
    clock = time.Clock()
    images = {}
    bgcolor = (255,0,0)
    keys = 0
    mouse = 0
    collide_list = sprite.Group()
    def __init__(self):
        init()
        self.i_disp = display.set_mode((640,480))
    def d_watch_keys(self,keyfn):
        self.keys = keyfn
    def d_watch_mouse(self,mousefn):
        self.mouse = mousefn
    def d_title(self, pgTitle):
        display.set_caption(pgTitle)
    def d_start(self, game_loop):
        if self.running == True:
            self.__bad_message("d_start cannot be called twice.")
        self.running = True
        while self.running:
            for c_e in event.get():
                if c_e.type == QUIT:
                    self.__d_shutdown()
            if not self.keys ==0:
                self.keys(key.get_pressed())
            if not mouse == 0:
                self.__check_mouse()
            game_loop()
            self.__d_dobg()
            self.__draw_images()
            display.flip()
            self.clock.tick(self.fps)
    def d_get_title(self):
        return display.get_caption()
    def d_set_frame_rate(self,rate):
        self.fps = rate
    def d_get_frame_rate(self,rate):
        return self.fps
    def d_set_bg(self,bg):
        self.bgcolor = bg
    def d_get_bg(self,bg):
        return self.bgcolor
    def img_change_rotate(self,img,r,allow=True):
        self.__validate_img(img)
        cr = self.images[img].rotation
        if r >=360 or r <= -360:
            self.__bad_message("Cannot rotate by: " + str(r))
        self.images[img].rotation +=r
        if self.images[img].rotation >=360:
            self.images[img].rotation -=360
        self.__apply_image_effect(img)
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rotation = cr
            self.__apply_image_effect(img)
    def img_set_rotate(self,img,r,allow=True):
        self.__validate_img(img)
        if r >=360 or r <= -360:
            self.__bad_message("Cannot rotate by: " + str(r))
        cr = self.images[img].rotation
        self.images[img].rotation =r
        if self.images[img].rotation >=360:
            self.images[img].rotation -=360
        self.__apply_image_effect(img)
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rotation = cr
            self.__apply_image_effect(img)
    def img_add_image(self,img,x,y,transparent=(255,255,255),name="default"):
        if (name[:1]) == "*": # * is special
            return False
        if not name in self.images:
            new_image = pgSprite()
            new_image.set_image(img,x,y)
            self.images[name] = new_image
            self.collide_list.add(new_image)
            if transparent != 0:
                if not img[-4:] == ".png":
                    new_image.image.set_colorkey(transparent)
                new_image.mask = mask.from_surface(new_image.image)
            return True
        return False
    def img_move(self,img,val,allow=True):
        self.__validate_img(img)
        temp = self.images[img].rect.copy()
        angle = self.images[img].rotation * math.pi /180
        self.images[img].rect.x += math.cos(angle) * val
        self.images[img].rect.y -= math.sin(angle) * val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect = temp
    def img_move_x(self,img,val,allow = True):
        self.__validate_img(img)
        self.images[img].rect.x += val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect.x -= val
    def img_move_y(self,img,val,allow=True):
        self.__validate_img(img)
        self.images[img].rect.y += val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect.y -= val
    def img_get_x(self,img):
        self.__validate_img(img)
        return self.images[img].rect.x
    def img_get_y(self,img):
        self.__validate_img(img)
        return self.images[img].rect.y
    def img_get_size(self,img):
        self.__validate_img(img)
        return self.images[img].size
    def img_get_rotation(self,img):
        self.__validate_img(img)
        return self.images[img].rotation
    def img_delete(self,img):
        self.__validate_img(img)
        self.images.pop(img)
    def img_touching(self,img1,img2):
        self.__validate_img(img1)
        cur_img_rect = self.__get_stretched_rect(img1)
        if img2.upper() == "*ANY*":
            for obj in self.images:
                if obj != img1:
                    if sprite.collide_mask(self.images[img1],self.images[obj]):
                        return obj
        elif img2.upper() == "*EDGE*":
            if cur_img_rect.x < 0:
                return "Left"
            elif cur_img_rect.x + cur_img_rect.width > self.i_disp.get_width():
                return "Right"
            elif cur_img_rect.y < 0: 
                return "Top"
            elif cur_img_rect.y + cur_img_rect.height > self.i_disp.get_height():
                return "Bottom"
        elif img2.upper() == "*MOUSE*":
            m_pos = mouse.get_pos()
            m_x = m_pos[0] - self.images[img1].rect.x
            m_y = m_pos[1] - self.images[img1].rect.y
            try:
                return cur_img_rect.collidepoint(mouse.get_pos()) and self.images[img1].mask.get_at((m_x,m_y))
            except:
                return False
        else:
            self.__validate_img(img2)
            if sprite.collide_mask(self.images[img1],self.images[img2]):
                return img2
        return False
    def img_set_color_effect(self,img,color):
        self.__validate_img(img)
        if not self.images[img].shade == color:
            self.images[img].shade= color
            self.__apply_image_effect(img)
    def img_get_color_effect(self,img):
        self.__validate_img(img)
        return self.images[img].shade
    def img_layer_front(self,img):
        self.__validate_img(img)
        cur = self.images[img]
        self.images.pop(img)
        self.images[img] = cur
    def img_layer_back(self,img):
        self.__validate_img(img)
        cur = self.images[img]
        self.images.pop(img)
        new_dict = {img: cur}
        self.images = new_dict | self.images
    def img_layer_forward(self,img):
        self.__validate_img(img)
        d1 = {}
        d2 = {}
        d3 = {}
        stage = 0
        for d in self.images:
            if stage == 0:
                d1[d] = self.images[d]
                if d == img:
                    stage = 1
                    d1.pop(img)
            elif stage == 1:
                d2[d] = self.images[d]
                d2[img] = self.images[img]
                stage = 2
            elif stage == 2:
                d3[d] = self.images[d]
        if stage == 1:
            d1[img] = self.images[img]
        self.images = d1 | d2 | d3
    def img_layer_backward(self,img):
        self.__validate_img(img)
        d1 = {}
        last = ""
        for d in self.images:
            if d == img:
                d1[img] = self.images[img]
            if last != "":
                d1[last] = self.images[last]
                last = ""
            if d != img:
                last = d
        if last !="":
            d1[last] = self.images[last]
        self.images = d1
    def img_set_size(self,img,val):
        self.__validate_img(img)
        self.images[img].size = val
    def img_change_size(self,img,val,allow=True):
        self.__validate_img(img)
        self.images[img].size += val
        if allow == False and self.img_touching(img,"*any*"):
            self.img_move[img].size -=val
    def __draw_images(self):
        for d in self.images:
            self.i_disp.blit(self.images[d].image,self.images[d].rect)
    def __validate_img(self,img):
        if not img in self.images:
            self.__bad_message("No such image: " + img + "\nFirst call img_add_image")
    def __bad_message(self,msg):
        print(msg)
        self.__d_shutdown()
    def __d_shutdown(self):
        quit()
        sys.exit()
    def __d_dobg(self):
        self.i_disp.fill(self.bgcolor)
    def __check_mouse(self):
        if self.mouse == 0:
            return
        for d in self.images:
            cur_img = self.__get_stretched_rect(d)
            if cur_img.collidepoint(mouse.get_pos()):
                self.mouse(d,mouse.get_pos)
    def __get_stretched_rect(self,img):
        new_rect = self.images[img].rect
        new_rect = new_rect.scale_by(self.images[img].size/100)
        return new_rect
    def __apply_image_effect(self,img):
        ck = self.images[img].image.get_colorkey()
        orig_width = self.images[img].image.get_rect().width
        orig_height = self.images[img].image.get_rect().height
        self.images[img].image = transform.rotate(self.images[img].base_image,self.images[img].rotation)
        new_width = self.images[img].image.get_rect().width
        new_height = self.images[img].image.get_rect().height
        self.images[img].rect.x -= int((new_width - orig_width) /2)
        self.images[img].rect.y -= int((new_height - orig_height)/2)
        if self.images[img].shade != 0:
            self.images[img].image.fill(self.images[img].shade,special_flags = BLEND_RGBA_MULT)
            self.images[img].image.set_colorkey(self.images[img].shade)
        else:
            self.images[img].image.set_colorkey(self.images[img].shade)
        self.images[img].image.set_colorkey(ck)
        self.images[img].mask = mask.from_surface(self.images[img].image)
class pgSprite(sprite.Sprite):
    shade = 0
    rotation = 0
    size = 100
    def __init__(self):
        super().__init__()
    def set_image(self,img,x,y):
        self.image = image.load(img)
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
