import pygame, random, sys, math, time
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
gravity =3
class Pl:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))
        self.vx = 0
        self.vy = 0
    def collide(self, obj):
        return self.rect.colliderect(obj.rect)
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))
class Wall:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))
        self.x_speed = 0
        self.y_speed = 0

    def move(self):
        self.rect.x += WS

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))
class Ship:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.orig_img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.orig_img, (w, h)) 
    def move(self):
        self.rect.x += WS
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))
ship = [] 
walls = []
wallsblock = []
exitpy = []
clock = pygame.time.Clock()
speed = 5
pl = Pl(WIDTH/2,HEIGHT-80,40,40,"pl.png")
fon = Wall(0,0,WIDTH,HEIGHT,'fon.png')
size = 40
def OpenWalls(name_map):
    walls = []
    ship = [] 
    wallsblock = []
    exitpy = []
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
                    wallsblock.append(Wall(col * size, row * size, size, size,'wallblock.png'))
                if i == '4':
                    exitpy.append(Wall(col * size, row * size, size, size,'pl.png'))
                col += 1
            row += 1  
    return walls,ship,wallsblock,exitpy
walls,ship,wallsblock,exitpy = OpenWalls('map.txt')
WS=0
pygame.display.set_caption('cat jumper')
pygame.display.set_icon(pygame.image.load('pl.png'))
jump=True
mapscore=1
while True:
    fon.draw()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                pl.vx = -speed
            elif e.key == pygame.K_d:
                pl.vx = speed

            elif e.key == pygame.K_SPACE:
                if jump:
                    pl.vy=-speed*3.75
                    jump=False
        elif e.type == pygame.KEYUP:
            if not e.key == pygame.K_SPACE:
                pl.vx = 0
                WS = 0
            
    for s in ship:
        if pl.collide(s):
            pl = Pl(160*3,HEIGHT-80,40,40,"pl.png")
            if mapscore == 1:
                walls,ship,wallsblock,exitpy = OpenWalls('map.txt')
            elif mapscore == 2:
                walls,ship,wallsblock,exitpy = OpenWalls('map2.txt')
            
    for wall in walls:
        if pl.collide(wall):
            jump=True
            if pl.rect.y>=wall.rect.y-40:
                pl.rect.y+=-gravity    
    for wall in walls:
        wall.draw()
        wall.rect.x += WS
    for wall1 in wallsblock:
        wall1.draw()
        wall1.rect.x += WS
        if pl.collide(wall1):
            pl = Pl(160*3,HEIGHT-80,40,40,"pl.png")
            if mapscore == 1:
                walls,ship,wallsblock,exitpy = OpenWalls('map.txt')
            elif mapscore == 2:
                walls,ship,wallsblock,exitpy = OpenWalls('map2.txt')
    if pl.vy<0:
        pl.vy+=0.1
    for s in ship:
        s.draw()
        s.rect.x += WS
    if pl.rect.x >=160*3:
       pass
    else:
        pl.vx = 0
        pl.rect.x=160*3
        WS = 5
    if pl.rect.x <=WIDTH-160*3:
        pass
    else:
        pl.rect.x=WIDTH-160*3
        pl.vx = 0
        WS = -5
    if pl.rect.y<=50:
        pl.rect.y=50
    pl.rect.y+=pl.vy+gravity
    pl.rect.x+=pl.vx
    for e in exitpy:
        e.draw()
        e.rect.x+=WS
        if pl.collide(e):
            pl = Pl(160*3,HEIGHT-80,40,40,"pl.png")
            if mapscore == 1:
                walls,ship,wallsblock,exitpy = OpenWalls('map2.txt')
                mapscore+=1
            elif mapscore == 2:
                walls,ship,wallsblock,exitpy = OpenWalls('map.txt')
                mapscore=1
    pl.draw()
    pygame.display.update()
    clock.tick(60)