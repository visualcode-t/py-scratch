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
    ###Stretched images do not work with collision###
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
        '''Sets or changes the callback for key handling.

        Parameters:
            keyfn (Function): The function to be called for monitoring key-presses.
        '''
        self.keys = keyfn
    def d_watch_mouse(self,mousefn):
        '''Sets or changes the callback for mouse handling.

        Parameters:
            mousefn (Function): The function to be called for monitoring mouse control.
        '''
        self.mouse = mousefn
    def d_title(self, pgTitle):
        '''Sets or changes the window title.

        Parameters:
            pgTitle (String): The new window title.
        '''
        display.set_caption(pgTitle)
    def d_start(self, game_loop):
        '''Starts the program.

        Parameters:
            game_loop (Function): The function that will be called each frame.
        '''
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
        '''
        Return:
            title (String): The current window title.
        '''
        return display.get_caption()
    def d_set_frame_rate(self,rate):
        '''Sets the frame rate for the program.

        Parameters:
            rate (Int): The number of frames to process per second.
        '''
        self.fps = rate
    def d_get_frame_rate(self,rate):
        '''
        Return:
            rate (Int): The current frame rate.
        '''
        return self.fps
    def d_set_bg(self,bg):
        '''Sets the window background color.

        Parameters:
            bg (ColorValue): The new background color.
        '''
        self.bgcolor = bg
    def d_get_bg(self,bg):
        '''Get the current background color.
        Return:
            bg (ColorValue): The current background color.
        '''
        return self.bgcolor
    def img_change_rotate(self,img,r,allow=True):
        '''Rotate the image.

        Parameters:
            img (String): The name of the sprite you would like to control.
            r (Int): Rotation amount in degrees.
            allow (Boolean): Whether to allow collision when moving.
        '''
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
        '''Rotate the image.

        Parameters:
            img (String): The name of the sprite you would like to control.
            r (Int): The new rotation amount in degrees.
            allow (Boolean): Whether to allow collision when moving.
        '''
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
        '''Creates a sprite.

        Parameters:
            img (string): The location of the image file
            transparent (tuple): The color to make transparent.
                0 should be provided for pngs with built-in transparency.
            name (String): The name that will later be used to reference the sprite.
        '''
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
        '''Move the sprite based on the direction it is facing.

        Parameters:
            img (String): The name of the sprite you would like to control.
            val (Int): The amount to move the sprite.
            allow (Boolean): Whether to allow collision when moving.
        '''
        self.__validate_img(img)
        temp = self.images[img].rect.copy()
        angle = self.images[img].rotation * math.pi /180
        self.images[img].rect.x += math.cos(angle) * val
        self.images[img].rect.y -= math.sin(angle) * val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect = temp
    def img_move_x(self,img,val,allow = True):
        '''Change the sprite's x position..

        Parameters:
            img (String): The name of the sprite you would like to control.
            val (Int): The amount to move the sprite.
            allow (Boolean): Whether to allow collision when moving.
        '''
        self.__validate_img(img)
        self.images[img].rect.x += val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect.x -= val
    def img_move_y(self,img,val,allow=True):
        '''Change the sprite's y position..

        Parameters:
            img (String): The name of the sprite you would like to control.
            val (Int): The amount to move the sprite.
            allow (Boolean): Whether to allow collision when moving.
        '''
        self.__validate_img(img)
        self.images[img].rect.y += val
        if allow == False and self.img_touching(img,"*any*"):
            self.images[img].rect.y -= val
    def img_get_x(self,img):
        '''Get the sprite's x position..

        Parameters:
            img (String): The name of the sprite you would like to access.
        
        Return:
            x (Int): The current sprite's x position.
        '''
        self.__validate_img(img)
        return self.images[img].rect.x
    def img_get_y(self,img):
        '''Get the sprite's y position..

        Parameters:
            img (String): The name of the sprite you would like to access.
        
        Return:
            y (Int): The current sprite's y position.
        '''
        self.__validate_img(img)
        return self.images[img].rect.y
    def img_get_size(self,img):
        '''Get the sprite's size.

        Parameters:
            img (String): The name of the sprite you would like to access.
        
        Return:
            size (Int): The current sprite's size.
        '''
        self.__validate_img(img)
        return self.images[img].size
    def img_get_rotation(self,img):
        '''Get the sprite's current direction.

        Parameters:
            img (String): The name of the sprite you would like to access.
        
        Return:
            r (Int): The current sprite's direction in degrees.
        '''
        self.__validate_img(img)
        return self.images[img].rotation
    def img_delete(self,img):
        '''Remove the sprite.

        Parameters:
            img (String): The name of the sprite you would like to access.
        '''
        self.__validate_img(img)
        self.images.pop(img)
    def img_touching(self,img1,img2):
        '''Check whether the sprite is touching another entity.

        Parameters:
            img1 (String): The name of the sprite you would like to check.
            img2 (String): The name of the sprite you would like to check against.
                *ANY* Check all sprites
                *EDGE* Check all edges
                *LEFT*,*RIGHT*,*TOP*,*BOTTOM* Check against a specific edge.
                *MOUSE* Check overlap with the cursor.
        
        Return:
            r (Various): Returns what was touched.
                *THIS fn IS IN PROCESS*
        '''
        self.__validate_img(img1)
        cur_img_rect = self.__get_stretched_rect(img1)
        if img2.upper() == "*ANY*":
            for obj in self.images:
                if obj != img1:
                    if sprite.collide_mask(self.images[img1],self.images[obj]):
                        return obj
        elif img2.upper() == "*EDGE*":
            #adjust to work with mask
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
        '''Set the sprite's color effect.

        Parameters:
            img (String): The name of the sprite you would like to change.
        '''
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
    def img_set_x(self,img,val):
        self.__validate_img(img)
        self.images[img].rect.x = val
    def img_set_y(self,img,val):
        self.__validate_img(img)
        self.images[img].rect.y = val
    def img_change_size(self,img,val,allow=True):
        self.__validate_img(img)
        self.images[img].size += val
        self.__apply_image_effect(img)
    def __draw_images(self):
        for d in self.images:
            #nloc = self.images[d].rect.copy()
            #nloc.x += self.images[d].offsetx
            #nloc.y += self.images[d].offsety
            #self.i_disp.blit(self.images[d].image,nloc)
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
        self.images[img].image = self.images[img].base_image.copy()
        self.images[img].image = transform.scale(self.images[img].image,(self.__get_stretched_rect(img).width,self.__get_stretched_rect(img).height))
        a =  self.images[img].image.get_rect()
        self.images[img].image = transform.rotate(self.images[img].image,self.images[img].rotation)
        b= (self.images[img].image.get_rect())
        wd = a.width - b.width
        hd = a.height - b.height
        ox = math.floor(wd/2)
        oy = math.floor(hd/2)
        self.images[img].rect.x -= self.images[img].offsetx
        self.images[img].rect.y -= self.images[img].offsety
        self.images[img].offsetx = ox
        self.images[img].offsety = oy
        self.images[img].rect.x += self.images[img].offsetx
        self.images[img].rect.y += self.images[img].offsety
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
    offsetx = 0
    offsety = 0
    def __init__(self):
        super().__init__()
    def set_image(self,img,x,y):
        self.image = image.load(img)
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y