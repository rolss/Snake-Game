import pygame as pg
import sys
import random as rand

pg.init()
WIDTH = 500
HEIGHT = 400
display = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Tron")
clock = pg.time.Clock()

class snake:
    def __init__(self, color, dark_color, coords):
        self.x=coords[-1][0]
        self.y=coords[-1][1]
        self.color = color
        self.dark_color = dark_color
        # TRACE: keeps a list of coordinates for each square of the body. self.size defines TRACE length
        self.trace=coords # initial coordinates
        self.size=3
    
    def move(self, xm, ym):
        self.trace.append([self.x,self.y])
        self.x = self.x + xm
        self.y = self.y + ym
    
    def draw(self):
        # Delete and erase last square of the tail
        erased = self.trace.pop(0)
        pg.draw.rect(display, color='black', rect=(erased[0],erased[1],10,10))

        # Draw head
        pg.draw.rect(display, color=self.dark_color, rect=(self.x,self.y,10,10))

        # Draw body, taking size into account
        for i in range(self.size):
            pg.draw.rect(display, color=self.color, rect=(self.trace[i][0], self.trace[i][1],10,10))
    
    def eat(self):
        # Increase size of snake, increase size of TRACE
        self.size +=1
        self.trace.append([self.x,self.y])
            

# Takes RGB for bright color, RGB for dark color, and initial coordinates
player = snake((40, 180, 99), (29, 131, 72), [[50,300],[60,300], [70,300]])
# Starts moving to the right
xm1=10
ym1=0

font = pg.font.Font("freesansbold.ttf",50)

# Select position of food randomly
food_coord_x = rand.randint(10,WIDTH//10 - 2)*10
food_coord_y = rand.randint(10,HEIGHT//10 - 2)*10

pg.draw.rect(display, color='red', rect=(food_coord_x,food_coord_y,10,10))
while True:
    for event in pg.event.get():
        # Player selects a direction to move on
        # Validates a player doesn't try to go on reverse
        if event.type == pg.KEYDOWN:
            # WASD Keys only
            if event.key == pg.K_w:
                if xm1 != 0 and ym1 != 10:
                    xm1=0
                    ym1=-10
            if event.key == pg.K_d:
                if xm1 != -10 and ym1 != 0:
                    xm1=10
                    ym1=0
            if event.key == pg.K_a:
                if xm1 != 10 and ym1 != 0:
                    xm1=-10
                    ym1=0
            if event.key == pg.K_s:
                if xm1 != 0 and ym1 != -10:
                    xm1=0
                    ym1=10
    
    # Move in the direction stated
    player.move(xm1,ym1)
    player.draw()
    
    # Eat
    if player.x == food_coord_x and player.y == food_coord_y:
        player.eat()
        pg.draw.rect(display, color='black', rect=(food_coord_x, food_coord_y,10,10))
        food_coord_x = rand.randint(10,WIDTH//10 - 2) * 10
        food_coord_y = rand.randint(10,HEIGHT//10 - 2) * 10
        pg.draw.rect(display, color='red', rect=(food_coord_x,food_coord_y,10,10))
    
    # Check collisions
    elif [player.x, player.y] in player.trace or player.x == WIDTH or player.x == -10 or player.y == HEIGHT or player.y == -10:
        text = font.render('Game over!', True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        display.blit(text, textRect)
        pg.display.update()
        pg.time.delay(2000)
        pg.quit()
        sys.exit()

    pg.display.update()
    clock.tick(10)