from pygame import *
from random import randint
from time import time as timer
 
#background music
mixer.init()
mixer.music.load('14.mp3')
mixer.music.play()
fire_sound = mixer.Sound('pottis.mp3')
clock = time.Clock()
 
#fonts and labels
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 25, 6))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)
num_fire = 0
rel_time = False
# we need these pictures:
img_back = "galaxy.jpg" # game background
img_hero = "rocket.png" # character
img_bullet = "bullet.png" # bullet
img_enemy = "dde.png" # enemy
 
score = 0 # ships hit
goal = 0
lost = 0 # ships missed
max_lost = 6 # lost if this many missed
life = 3
 
# parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)
 
        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# main player class
class Player(GameSprite):
    # method for controlling the sprite with keyboard arrows
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # the "fire" method (use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
# enemy sprite class   
class Enemy(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        # disappears if it reaches the edge of the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# bullet sprite class   
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -50:
            self.kill()


 
# Create the window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 100, randint(1, 5))
    monsters.add(monster)
 
bullets = sprite.Group()

# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# Main game loop:
run = True # the flag is cleared with the close window button
while run:
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        # press on the space bar event - the sprite fires
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire +=1
            if num_fire > 10 and rel_time == False:
                last_time = timer()
                rel_time = True

    collides = sprite.groupcollide(monsters,bullets,True,True)
    for c in collides:
        goal = goal+1
        monster = Enemy(img_enemy, randint(80, win_width -80), -40, 50, 100, randint(1, 5))
        monsters.add(monster)

    if sprite.spritecollide(ship, monsters,False) or lost >= max_lost:
        finish = True
        window.blit((10, 50))

    if goal == 10:
        finish = True
        window.blit(lose, (10 , 50))


    if not finish:
        # refresh background
        window.blit(background,(0,0))
 
        # writing text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        # producing sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        if rel_time == True:
            now_time = timer()
            
            if now_time - last_time < 3:
                reload = font2.render("Engi i need bulet",1, (150,0, 0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False   
 
        # updating them at a new location on each iteration of the loop
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
    
        display.update()
    clock.tick(30)