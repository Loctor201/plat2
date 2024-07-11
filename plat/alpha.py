import pygame, random, sys, math, time
pygame.init()

WIDTH, HEIGHT = 1920, 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('cat jumper')
pygame.display.set_icon(pygame.image.load('pl.png'))




gravity = 3
speed = 5
jump = False

ship = [] 
walls = []
wallsblock = []

size = 40

wallspeed = 0








class Pl:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))
        self.vx, self.vy = 0, 0

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))



class Wall:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))

    def move(self):
        self.rect.x += wallspeed

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))



class Ship:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))

    def move(self):
        self.rect.x += wallspeed

    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))


def OpenWalls(name_map):
    walls = []
    ship = [] 
    wallsblock = []
    with open(name_map, 'r') as map:
        row, col = 0, 0
        for line in map.read().split('\n'):
            x = list(line)
            col = 0
            for i in x:
                if i == '1':
                    walls.append(Wall(col * size, row * size, size, size, 'wall.png'))
                if i == '2':
                    ship.append(Ship(col * size, row * size, size, size,'ship.png'))
                if i == '3':
                    wallsblock.append(Wall(col * size, row * size, size, size,'pl.png'))
                col += 1
            row += 1  
    return walls, ship, wallsblock

walls,ship,wallsblock = OpenWalls('map.txt')


pl = Pl(160,HEIGHT-80,size,size,"pl.png")
fon = Wall(0,0,WIDTH,HEIGHT,'fon.png')


direction = 'none'


while True:
    fon.draw()



    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()

            if e.key == pygame.K_a:
                direction = 'left'

            elif e.key == pygame.K_d:
                direction = 'right'

            elif e.key == pygame.K_SPACE:
                if jump:
                    pl.vy=-speed*2
                    jump=False
        elif e.type == pygame.KEYUP:
            
            direction = 'none'


    if direction == 'none':
        pl.vx = 0
        wallspeed = 0
    if direction == 'left':
        if pl.rect.x >= 160:
            pl.vx = -speed
            wallspeed = 0
        else:
            wallspeed = speed
            pl.vx = 0
    if direction == 'right':
        if pl.rect.x <= WIDTH - 160:
            pl.vx = speed
            wallspeed = 0
        else:
            wallspeed = -speed
            pl.vx = 0



    for s in ship:
        if pl.collide(s):
            walls,ship,wallsblock = OpenWalls('map.txt')
            pl = Pl(160,HEIGHT-80,40,40,"pl.png")


    for wall in walls:
        if pl.collide(wall):
            jump=True
            if pl.rect.y >= wall.rect.y-40:
                pl.rect.y -= gravity 


    for wall in walls:
        wall.draw()

    is_collide_wall = False
    for wall1 in wallsblock:
        wall1.draw()
        
        if pl.collide(wall1):
            is_collide_wall = True
            break

        
    if not is_collide_wall:
        for wall1 in wallsblock:
            wall1.rect.x += wallspeed
        for wall in walls:
            wall.rect.x += wallspeed

    if pl.vy<0:
        pl.vy+=0.1

    
    pl.rect.y+=pl.vy+gravity

    if not is_collide_wall:
        pl.rect.x += pl.vx
    else:
        pl.rect.x += wallspeed * 3

    
    pl.draw()
    pygame.display.update()
    clock.tick(60)