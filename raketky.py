import pyglet
import math
import random
HEIGHT = 640
WIDTH = 480

ROTATION_SPEED = 200
ACCELERATION = 300

MAX_SPEED = 500

def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

spaceship_imgs = [
    load_image('PNG/playerShip2_red.png'),
    load_image('PNG/playerShip2_blue.png'),
    load_image('PNG/playerShip2_green.png'),
    ]

asteroid_imgs = [
    load_image('PNG/Meteors/meteorGrey_big1.png'),
    load_image('PNG/Meteors/meteorGrey_big2.png'),
    load_image('PNG/Meteors/meteorGrey_big3.png'),
    load_image('PNG/Meteors/meteorGrey_big4.png'),
    ]

def  circle(x,y,radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dx = radius, 0
    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glWertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()

def distance(a,b,wrap_size):
    result = abs(a - b)
    if result > wrap_size /2:
        result = wrap_size - result
    return result

def overlaps(a,b):
    distance_squared = (distance(a.x,b.x, window.width) **2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

class SpaceObject:
    def __init__(self, window):
        self.window = window
        self.x = None
        self.y = None
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0

def tick(self, dt):
    # okraje
    if self.x < 0:
        self.x += self.window.width
    if self.y <0:
        self.y += self.window.height
    if self.x > self.window.width:
        self.x -= self.window.width
    if self.y > self.window.height:
        self.y -= self.window.hight

class Spaceship(SpaceObject):
    def __init__(self, window):
        super().__init__(window)
        self.x = window.width/ 2
        self.y = window.height/ 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 180
        self.sprite = pyglet.sprite.Sprite(random.choice(spaceship_imgs))
        self.window = window
        self.radius = 47

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += ROTATION_SPEED * dt
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= ROTATION_SPEED * dt
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)

        # omezení rychlosti raketky
        self.x_speed = min(self.x_speed, MAX_SPEED)
        self.x_speed = max(self.x_speed, -MAX_SPEED)
        self.y_speed = min(self.y_speed, MAX_SPEED)
        self.y_speed = max(self.y_speed, -MAX_SPEED)


        # výpočet nových souřadnic
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt

        super().tick(dt)

        for obj in objects:
            if obj != self:
                if overlaps (self, obj):
                    self.delete()
    def delete(self):
        objects.remove(self)


class Asteroid(SpaceObject):
    def __init__(self, window):
        super(). __init__(window)
        self.sprite = pyglet.sprite.Sprite(random.choice(asteroid_imgs))
        # import random
        strana = random.randrange(4)
        if strana == 0:
            self.x = 0
            self.y = random.randrange(window.height)
        elif strana == 1:
            self.x = window.width
            self.y = random.randrange(window.height)
        elif strana == 2:
            self.x = random.randrange(window.width)
            self.y = 0
        else:
            self.x = random.randrange(window.width)
            welf.y = window.HEIGHT

        #ASTEROID_SPEED=200

        #rychlost asteroidu
        self.x_speed = random.uniform (-ASTEROID_SPEED, ASTEROID_SPEED)
        self.y_speed = random.uniform (-ASTEROID_SPEED, ASTEROID_SPEED)
        self.radius = 50

window = pyglet.window.Window(height = HEIGHT, width = WIDTH)

objects = []

objects.append(Spaceship(window))
for i in range(4):
    objects.append(Asteroid(window))

def draw():
    window.clear()
    spaceship.sprite.draw()

def tick(dt):
    spaceship.tick(dt)

pressed_keys = set()

def key_pressed(key, mod):
    pressed_keys.add(key)

def key_released(key, mod):
    pressed_keys.discard(key)

window.push_handlers(
    on_draw=draw,
    on_key_press=key_pressed,
    on_key_release=key_released,
)

pyglet.clock.schedule(tick)

pyglet.app.run()
