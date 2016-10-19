# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
spaceship_angle = 0
spaceship_angle_vel = 0
spaceship_pos = [WIDTH / 2, HEIGHT / 2]
spaceship_vel = [0, 0]
spaceship_angle_vel_inc = 0.05
speed_factor = 0.1
friction = 0.02
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
soundtrack.set_volume(.2)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# define a helper function that draws and updates each sprite in the group
def process_sprite_group(canvas, my_set):
    rs = set()
    for s in my_set:
        s.draw(canvas)
        if s.update():
            rs.add(s)
    my_set.difference_update(rs)
        
# define a helper function group_collide
def group_collide(group, other_object):
    ind = 0 # True or False indicator
    rs = set() # remov_set
    for s in group:
        if s.collide(other_object):
            ind = 1
            rs.add(s)
            explosion_group.add(Sprite(s.pos, [0, 0], 0, 0, explosion_image,
                                      explosion_info, explosion_sound))
    group.difference_update(rs)
    return ind
    
# define a helper function group_group_collide
def group_group_collide(group1, group2):
    num = 0 # initiate point
    for s in set(group1):
        if group_collide(group2, s):
            num += 1
            group1.discard(s)
    return num

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def set_thrust(self, value):
        self.thrust = value
        if self.thrust:
            self.image_center[0] *= 3
            ship_thrust_sound.play()
        else:
            self.image_center[0] /= 3
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def shoot(self):
        direction = angle_to_vector(self.angle)
        vel = list(self.vel)
        pos = [self.pos[0] + direction[0]*40, self.pos[1] + direction[1]*40]
        for i in range(2):
            pos[i] += vel[i]
            vel[i] += direction[i]*5
        missile_group.add(Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    def update(self):
        # update orientation
        self.angle += spaceship_angle_vel
        direction = angle_to_vector(self.angle)
        # update position
        self.pos[0] += self.vel[0]
        self.pos[0] = self.pos[0] % WIDTH # modular arithmetics
        self.pos[1] += self.vel[1]
        self.pos[1] = self.pos[1] % HEIGHT
        self.vel[0] *= (1 - friction) # apply the effect of friction
        self.vel[1] *= (1 - friction)
        if self.thrust:
            self.vel[0] += direction[0]*speed_factor
            self.vel[1] += direction[1]*speed_factor 
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated:
            current_explosion_index = (self.age % self.radius) // 1
            current_explosion_center = [self.image_center[0] +  current_explosion_index * self.image_size[0], 
                                        self.image_center[1]]
            canvas.draw_image(explosion_image, current_explosion_center, self.image_size, 
                              self.pos, self.image_size)
            self.age += 0.2
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
        
    def collide(self, other_object):
        pos1 = self.pos
        rad1 = self.radius
        pos2 = other_object.get_position()
        rad2 = other_object.get_radius()
        if dist(pos1, pos2) < (rad1 + rad2):
            return True
        else:
            return False
    
    def update(self):
        # update rotation
        self.angle += self.angle_vel
        # update position
        self.pos[0] += self.vel[0]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
           
def draw(canvas):
    global time, rock_group, missile_group, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    
    # update rocks, missiles and explosions
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # check collisions between spaceship and rocks and update lives
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    # check collisions between missiles and rocks and update scores
    if group_group_collide(rock_group, missile_group):
        score += 1
        
    # update score and lives
    canvas.draw_text("Lives", [40, 40], 24, "White")
    canvas.draw_text(str(lives), [40, 64], 24, "White")
    canvas.draw_text("Score", [WIDTH - 80, 40], 24, "White")
    canvas.draw_text(str(score*10), [WIDTH - 80, 64], 24, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.pause()
        soundtrack.rewind()
        
    # update to reset game
    if lives == 0 and started:
        started = False
        rock_group = set()
        missile_group = set()
        lives = 3
        score = 0

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group
    if not started: return
    else:                
        if len(rock_group) < 12:
            pos = [random.random()*WIDTH, random.random()*HEIGHT] 
            while dist(my_ship.get_position(), pos) < 60:
                pos = [random.random()*WIDTH, random.random()*HEIGHT]
            a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, 
                            asteroid_image, asteroid_info)
            a_rock.pos = pos
            a_rock.vel = angle_to_vector(random.random()*2*math.pi)
            a_rock.angle_vel = random.random()*0.1
            rock_group.add(a_rock)
        soundtrack.play()
    
# define keyhandlers to control spaceship
def keydown(key):
    global spaceship_angle_vel
    if key == simplegui.KEY_MAP["left"]:
        spaceship_angle_vel -= spaceship_angle_vel_inc
    elif key == simplegui.KEY_MAP["right"]:
        spaceship_angle_vel += spaceship_angle_vel_inc
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    global spaceship_angle_vel
    if (key == simplegui.KEY_MAP["left"] or 
        key == simplegui.KEY_MAP["right"]):
        spaceship_angle_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)
        
def click(pos):
    global started
    if dist(pos, [WIDTH/2, HEIGHT/2]) < 250:
        started = True
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship(spaceship_pos, spaceship_vel, spaceship_angle, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set()
rock_group = set()
explosion_group = set()

# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
