# Basic infrastructure for Bubble Shooter

import simplegui
import random
import math

# Global constants
WIDTH = 800
HEIGHT = 600
FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC = 0.02
BUBBLE_RADIUS = 20
COLOR_LIST = ["Red", "Green", "Blue", "White"]
LINE_WIDTH = 1
SPEED_FACTOR = 4
shooting_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")

# global variables
firing_angle = math.pi / 2
firing_angle_vel = 0
bubble_stuck = True


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# class defintion for Bubbles
class Bubble:
    
    def __init__(self, sound = None):
        self.pos = list(FIRING_POSITION)
        self.vel = [0, 0]
        self.color = random.choice(COLOR_LIST)
        self.sound = sound
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if (self.pos[0] - BUBBLE_RADIUS <= 0 or 
        self.pos[0] + BUBBLE_RADIUS > WIDTH): 
            self.vel[0] = -self.vel[0] 
        elif (self.pos[1] - BUBBLE_RADIUS <= 0 or 
           self.pos[1] > HEIGHT):
            self.vel[1] = -self.vel[1]
            
    def fire_bubble(self, vel):
        self.vel = vel
        if self.sound:
            self.sound.rewind()
            self.sound.play()
        
    def is_stuck(self): 
        pass

    def collide(self, bubble):
        pass
            
    def draw(self, canvas):
        canvas.draw_circle(self.pos, BUBBLE_RADIUS, LINE_WIDTH, self.color, self.color)
        

# define keyhandlers to control firing_angle
def keydown(key):
    global a_bubble, firing_angle_vel, bubble_stuck
    if key == simplegui.KEY_MAP["left"]:
        firing_angle_vel += FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP["right"]:
        firing_angle_vel -= FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP["space"]:
        bubble_stuck = False
        vel = angle_to_vector(firing_angle)
        a_bubble.fire_bubble([vel[0]*SPEED_FACTOR, -vel[1]*SPEED_FACTOR])		
        
def keyup(key):
    global firing_angle_vel
    firing_angle_vel = 0
    
# define draw handler
def draw(canvas):
    global firing_angle, a_bubble, bubble_stuck
    
    # update firing angle
    firing_angle += firing_angle_vel
    direction = angle_to_vector(firing_angle)
    upper_point = [FIRING_POSITION[0] + direction[0]*FIRING_LINE_LENGTH, 
                   FIRING_POSITION[1] - direction[1]*FIRING_LINE_LENGTH]

    # draw firing line
    canvas.draw_line(FIRING_POSITION, upper_point, 4, 'Yellow')
    # update a_bubble and check for sticking
    a_bubble.update()
    a_bubble.is_stuck()
    # draw a bubble and stuck bubbles
    a_bubble.draw(canvas)
 
# create frame and register handlers
frame = simplegui.create_frame("Bubble Shooter", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# create initial buble and start frame
a_bubble = Bubble(shooting_sound)
frame.start()