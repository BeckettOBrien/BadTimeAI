import pyglet
from pyglet.window import key
import random
import math

from attacks import *
import attackloader

gl_conf = pyglet.gl.Config(sample_buffers=1, samples=4)
pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST) 
pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)

pyglet.resource.path = ['Assets/']
pyglet.resource.reindex()

ATTACKS = ['sans_intro.csv', 'sans_bonegap1.csv', 'sans_bluebone.csv', 'sans_bonegap2.csv', 'sans_platforms1.csv',
           'sans_platforms2.csv', 'sans_platforms3.csv', 'sans_platforms4.csv', 'sans_platformblaster.csv',
           'sans_platforms4hard.csv', 'sans_bonegap1fast.csv', 'sans_boneslideh.csv', 'sans_bonegap2.csv',
           'sans_platformblasterfast.csv',
           random.choice(['sans_bonegap1fast.csv', 'sans_bonegap2.csv', 'sans_boneslideh.csv']), 'sans_spare.csv',
           'sans_multi1.csv', 'sans_randomblaster1.csv', 'sans_multi2.csv', 'sans_bonestab1.csv', 'sans_bonestab2.csv',
           'sans_randomblaster2.csv', 'sans_boneslidev.csv', 'sans_multi3.csv', 'sans_bonestab3.csv',
           random.choice(['sans_bonestab3.csv', 'sans_multi3.csv', 'sans_randomblaster2.csv']), 'sans_final.csv']


# Attacks have been added in order

class SansBattle(pyglet.window.Window):
    def __init__(self, width=640, height=480, fps=False, config=gl_conf, *args, **kwargs):
        super(SansBattle, self).__init__(width, height, vsync=True, *args, **kwargs)
        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self.keys = {}

        self.alive = 1
        self.dt = 0

        self.current_attack = 0
        self.in_attack = False
        #attackloader.load_attack(ATTACKS[self.current_attack])
        self.attackLines = []

        self.attack_sprites = pyglet.graphics.Batch()
        self.platforms = []

        self.box_bounds = {}

        self.player = Player()

    def start_attack(self):
        # attackloader.read_attack()
        for row in attackloader.get_current_rows():
            print(row)
        # self.in_attack = True

    def load_next_attack(self):
        attackloader.end_attack()
        if self.current_attack > len(ATTACKS):
            self.alive = 0
            return
        self.current_attack += 1
        self.in_attack = False
        attackloader.load_attack(ATTACKS[self.current_attack])
    
    def update_platforms(self):
        out_of_bounds_platforms = [] # I have to do this to avoid changing the size of platforms during iteration
        for p in self.platforms:
            p.update(self.box_bounds)
            p_bounds = p.get_bounds()
            if p.direction == 0:
                if p_bounds['left'] > self.box_bounds['right']:
                    out_of_bounds_platforms.append(p)
            if p.direction == 1:
                if p_bounds['top'] < self.box_bounds['bottom']:
                    out_of_bounds_platforms.append(p)
            if p.direction == 2:
                if p_bounds['right'] < self.box_bounds['left']:
                    out_of_bounds_platforms.append(p)
            if p.direction == 3:
                if p_bounds['bottom'] > self.box_bounds['top']:
                    out_of_bounds_platforms.append(p)
        
        for p in out_of_bounds_platforms:
            self.platforms.remove(p)
            print(self.platforms)
            # Kill off-screen instances

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modifiers):
        try:
            del self.keys[symbol]
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:  # [ESC]
            self.alive = 0
        elif symbol == key.SPACE:
            self.player.gravity = not self.player.gravity
            self.platforms.append(Platform([320, 130, 100, 2, 100, 1], self.attack_sprites))
            # print(self.player.is_on_ground(0, 0))
        self.keys[symbol] = True

    def render(self):
        self.clear()
        self.fps_display.draw();

        # Add stuff you want to render here.
        # Preferably in the form of a batch.
        self.draw_rect(self.player.box_center[0] - (self.player.box_size[0] / 2) - 5,
                       self.player.box_center[1] - (self.player.box_size[1] / 2) - 5,
                       self.player.box_size[0] + 10, self.player.box_size[1] + 10,
                       color=(255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255))
        self.draw_rect(self.player.box_center[0] - (self.player.box_size[0] / 2),
                       self.player.box_center[1] - (self.player.box_size[1] / 2),
                       self.player.box_size[0], self.player.box_size[1],
                       color=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

        # for p in self.platforms:
        #     p.render()
        # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST) 
        # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        self.attack_sprites.draw()
        self.player.sprite.draw()

        self.flip()
    
    def update(self, dt):
        if self.alive == 1:
            self.dt = dt
            self.dispatch_events()

            self.box_bounds = self.player.get_box_bounds()

            self.update_platforms()
            self.player.update(self.keys, self.platforms, self.dt)

            self.render()
        else:
            self.close()

    def start(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0);
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.app.run()


    def draw_rect(self, x, y, width, height, color):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]),
                             ('c3B', color))


class Player():
    def __init__(self):
        self.image = pyglet.resource.image('playerheart-sheet1.png')
        self.image.anchor_x = 8
        self.image.anchor_y = 8
        self.x = 400
        self.y = 200
        self.health = 92
        self.karma = 0
        self.gravity = False  # Graivty mode: 0 for off, x for down, y for up, etc. TODO: Find out which number should corrospond to which direction
        self.slammed = False
        self.angle = 90

        self.left_box_collide = False
        self.right_box_collide = False
        self.top_box_collide = False
        self.bottom_box_collide = False

        self.on_platform = False

        self.platforms = []

        self.speed = 150  # Change this to change move speed
        self.dx = 0
        self.dy = 0

        self.jump_strength = 180
        self.jumphold_cutoff = 30
        self.max_fall_speed = 750

        self.box_center = [320, 165]
        self.box_size = [576, 144]
        self.center_position()

        self.prev_keys = {}

        self.sprite = pyglet.sprite.Sprite(img=self.image, x=self.x, y=self.y)

    def update(self, keys, platforms, dt):

        self.detect_collisions()

        self.platforms = platforms

        if self.on_ground():
            if self.slammed:
                self.slammed = False
                #TODO: Implement shake here

        if not self.gravity:
            self.dx = 0
            self.dy = 0
            if key.LEFT in keys:
                self.dx = -self.speed
            if key.RIGHT in keys:
                self.dx = self.speed
            if key.UP in keys:
                self.dy = -self.speed
            if key.DOWN in keys:
                self.dy = self.speed

            if key.UP in keys and key.DOWN in keys:
                self.dy = 0
            if key.LEFT in keys and key.RIGHT in keys:
                self.dx = 0

            self.sprite.color = (255, 0, 0)
        else:
            downspeed = 0
            grav = 0

            if self.on_ground():
                if self.angle == 0 or self.angle == 180:
                    self.dx = 0
                if self.angle == 90 or self.angle == 270:
                    self.dy = 0
            
            if self.angle == 0:
                if (key.LEFT in keys) and (key.LEFT not in self.prev_keys):
                    self.jump()
                if (key.LEFT not in keys) and (key.LEFT in self.prev_keys) and self.dx < -self.jumphold_cutoff:
                    self.dx = -self.jumphold_cutoff
                downspeed = self.dx
            if self.angle == 90:
                if (key.UP in keys) and (key.UP not in self.prev_keys):
                    self.jump()
                if (key.UP not in keys) and (key.UP in self.prev_keys) and self.dy < -self.jumphold_cutoff:
                    self.dy = -self.jumphold_cutoff
                downspeed = self.dy
            if self.angle == 180:
                if (key.RIGHT in keys) and (key.RIGHT not in self.prev_keys):
                    self.jump()
                if (key.RIGHT not in keys) and (key.RIGHT in self.prev_keys) and self.dx > self.jumphold_cutoff:
                    self.dx = self.jumphold_cutoff
                downspeed = -self.dx
            if self.angle == 270:
                if (key.DOWN in keys) and (key.DOWN not in self.prev_keys):
                    self.jump()
                if (key.DOWN not in keys) and (key.DOWN in self.prev_keys) and self.dy > self.jumphold_cutoff:
                    self.dy = self.jumphold_cutoff
                downspeed = -self.dy
            
            if downspeed < 240 and downspeed > 15:
                grav = 540
            if downspeed <= 15 and downspeed > -30:
                grav = 180
            if downspeed <= -30 and downspeed > -120:
                grav = 450
            if downspeed <= -120:
                grav = 180
            
            x = round(math.cos(math.radians(self.angle)))
            y = round(math.sin(math.radians(self.angle)))
            if not self.on_ground():
                self.dx += x*grav*dt
                self.dy += y*grav*dt
                if self.angle == 0 and self.dx > self.max_fall_speed:
                    self.dx = self.max_fall_speed
                if self.angle == 90 and self.dy > self.max_fall_speed:
                    self.dy = self.max_fall_speed
            
            if self.angle == 0 or self.angle == 180:
                self.dy = 0
                if key.UP in keys and key.DOWN not in keys:
                    self.dy = -self.speed
                if key.DOWN in keys and key.UP not in keys:
                    self.dy = self.speed
            if self.angle == 90 or self.angle == 270:
                self.dx = 0
                # Platform Logic Here
                p = self.get_platform_overlap()
                if p != False:
                    if self.dy >= 0:
                        self.dx = (round(math.cos(math.radians(p.direction * 90))) * p.speed) * 1
                        self.dy = 0
                        self.y = p.get_bounds()['top'] + 8.5
                        self.on_platform = True
                if p == False or self.dy < 0:
                    self.on_platform = False
                if key.LEFT in keys and key.RIGHT not in keys:
                    self.dx -= self.speed
                if key.RIGHT in keys and key.LEFT not in keys:
                    self.dx += self.speed
            
            self.sprite.color = (0, 24, 255)

        if self.slammed:
            self.dx = round(math.cos(math.radians(self.angle))) * self.max_fall_speed
            self.dy = round(math.sin(math.radians(self.angle))) * self.max_fall_speed

        self.x += self.dx/60
        self.y -= self.dy/60

        self.collide_box()

        self.sprite.update(x=self.x, y=self.y, rotation=self.angle)

        self.prev_keys = keys.copy()

    def collide_box(self):
        box_bound_left = self.box_center[0] - (self.box_size[0] / 2) + 8
        box_bound_right = self.box_center[0] + (self.box_size[0] / 2) - 8
        box_bound_top = self.box_center[1] + (self.box_size[1] / 2) - 8
        box_bound_bottom = self.box_center[1] - (self.box_size[1] / 2) + 8

        self.detect_collisions()

        if self.left_box_collide:
            self.x = box_bound_left
        if self.right_box_collide:
            self.x = box_bound_right
        if self.top_box_collide:
            self.y = box_bound_top
        if self.bottom_box_collide:
            self.y = box_bound_bottom

    
    def detect_collisions(self):
        box_bound_left = self.box_center[0] - (self.box_size[0] / 2) + 8
        box_bound_right = self.box_center[0] + (self.box_size[0] / 2) - 8
        box_bound_top = self.box_center[1] + (self.box_size[1] / 2) - 8
        box_bound_bottom = self.box_center[1] - (self.box_size[1] / 2) + 8
        if self.x <= box_bound_left:
            self.left_box_collide = True
        else:
            self.left_box_collide = False
        if self.x >= box_bound_right:
            self.right_box_collide = True
        else:
            self.right_box_collide = False
        if self.y >= box_bound_top:
            self.top_box_collide = True
        else:
            self.top_box_collide = False
        if self.y <= box_bound_bottom:
            self.bottom_box_collide = True
        else:
            self.bottom_box_collide = False

    def center_position(self):
        self.x = self.box_center[0]
        self.y = self.box_center[1]

    def rotate(self, rotation):
        self.angle = rotation
        self.image = self.image.get_transform(rotate=rotation)

    def heart_check_solid(self, x, y):
        player_left = self.x + x - 8
        player_right = self.x + x + 8
        player_top = self.y - y + 8
        player_bottom = self.y - y - 8

        # Detect Box Collisions
        box_bound_left = self.box_center[0] - (self.box_size[0] / 2) + 8
        box_bound_right = self.box_center[0] + (self.box_size[0] / 2) - 8
        box_bound_top = self.box_center[1] + (self.box_size[1] / 2) - 8
        box_bound_bottom = self.box_center[1] - (self.box_size[1] / 2) + 8
        if (player_right > box_bound_right) | (player_left < box_bound_left) | \
                (player_top > box_bound_top) | (player_bottom < box_bound_bottom):
            return True
        return False
    
    def on_ground(self):
        if self.angle == 0:
            return self.right_box_collide
        elif self.angle == 90:
            # p = self.get_platform_overlap()
            # if p != False:
            #     return self.on_platform
            return self.bottom_box_collide or self.on_platform
        elif self.angle == 180:
            return self.left_box_collide
        elif self.angle == 270:
            return self.top_box_collide
    
    def get_platform_overlap(self):
        if self.angle != 90:
            return False
        for p in self.platforms:
            p_bounds = p.get_bounds()
            bounds = self.get_bounds()
            if (bounds['left'] < p_bounds['right']) and (bounds['right'] > p_bounds['left']) and (
                bounds['bottom'] <= p_bounds['top'] + 2) and (bounds['bottom'] >= p_bounds['top'] - 2):
                return p
        return False
        
        return False
    
    def jump(self):
        x = round(math.cos(math.radians(self.angle)))
        y = round(math.sin(math.radians(self.angle)))
        if self.on_ground():
            self.dx -= x*self.jump_strength
            self.dy -= y*self.jump_strength

    def slam(self, direction):
        self.angle = direction * 90
        self.slammed = True
    
    def get_box_bounds(self):
        box_bound_left = self.box_center[0] - (self.box_size[0] / 2) + 8
        box_bound_right = self.box_center[0] + (self.box_size[0] / 2) - 8
        box_bound_top = self.box_center[1] + (self.box_size[1] / 2) - 8
        box_bound_bottom = self.box_center[1] - (self.box_size[1] / 2) + 8

        return {'left': box_bound_left, 'right': box_bound_right, 'top': box_bound_top, 'bottom': box_bound_bottom}
    
    def get_bounds(self):
        return {'left': self.x - 8, 'right': self.x + 8, 'top': self.y + 8, 'bottom': self.y - 8}