import pyglet
import math
import numpy as np

class Platform:
    def __init__(self, params, batch):
        # self.image = pyglet.resource.image('platform1.png')

        self.x = params[0]
        self.y = params[1]
        self.width = params[2]
        self.direction = params[3]
        self.speed = params[4]
        self.reverse = bool(params[5])

        self.height = 7

        # self.img_data = set_image_size(self.image, self.width, self.height)
        # self.image = pyglet.image.AbstractImage(self.width, self.height)
        # self.image.anchor_x = self.width / 2
        # self.image.anchor_y = self.height / 2
        # self.image.blit_into(img_data, 0, 0, 0)
        # self.sprite = pyglet.sprite.Sprite(self.image, self.x, self.y, batch=batch)
    
    def update(self, box_bounds):
        if self.reverse:
            bounds = self.get_bounds()
            if self.direction == 0:
                if bounds['right'] >= box_bounds['right']:
                    self.direction = 2
            if self.direction == 1:
                if bounds['bottom'] <= box_bounds['bottom']:
                    self.direction = 3
            if self.direction == 2:
                if bounds['left'] <= box_bounds['left']:
                    self.direction = 0
            if self.direction == 3:
                if bounds['top'] >= box_bounds['top']:
                    self.direction = 1
        self.x += math.cos(math.radians(self.direction*90))*self.speed/60
        self.y -= math.sin(math.radians(self.direction*90))*self.speed/60

        # self.sprite.update(self.x, self.y)
    
    def render(self):
        draw_rect(self.x - (self.width / 2),
                       self.y - (self.height / 2),
                       self.width, self.height,
                       (255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255))
        draw_rect(self.x - (self.width / 2) + 1,
                       self.y - (self.height / 2) + 1,
                       self.width-2, self.height-2,
                       (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def get_bounds(self):
        return {'left': self.x - (self.width/2), 'right': self.x + (self.width/2),
                'top': self.y + self.height/2, 'bottom': self.y - self.height/2}

def PlatformRepeat(params, batch):
    startx = params[0]
    starty = params[1]
    width = params[2]
    direction = params[3]
    speed = params[4]
    count = params[5]
    spacing = params[6]

    platforms = []

    for i in range(0, count):
        x = startx - math.cos(math.radians(direction*90))*spacing*i/60
        y = starty + math.sin(math.radians(direction*90))*spacing*i/60
        platforms.append(Platform(x, y, width, direction, speed))
    
    return platforms

def draw_rect(x, y, width, height, color):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]),
                             ('c3B', color))

def set_image_size(img, x, y):
    # This function lets me "tile" the middle row/column of the image to stretch it without loosing quality
    raw_img = img.get_image_data()
    format = 'RGBA'
    pitch = raw_img.width * len(format)
    rgba = np.array(list(img.get_image_data().get_data(format, pitch))).reshape(-1, raw_img.width, len(format))
    
    mid_y = rgba[round(raw_img.height/2),:] # This is needed to stretch along Y
    while rgba.shape[0] < y:
        rgba = np.insert(rgba, round(raw_img.height/2), mid_y, 0)
    mid_x = rgba[:,round(raw_img.width/2)] # This is needed to stretch along X
    while rgba.shape[1] < x:
        rgba = np.insert(rgba, round(raw_img.width/2), mid_x, 1)
    
    raw_img.set_data(format, pitch, ''.join(map(chr, rgba.tostring())))

    return raw_img