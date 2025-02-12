import pygame
import random
import os
import serial.tools.list_ports

WIDTH = 480
HEIGHT = 600

FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# set up assets locations
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

pygame.init() # initializes pygames and creates window
pygame.font.init() # initializes font for pygame
pygame.mixer.init() # intializes mixer for pygames for music and sound

#Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # dictates the window size of the window
pygame.display.set_caption("Pulse Rush") # sets window name
clock = pygame.time.Clock() # sets up clock speed for game
background = pygame.image.load(os.path.join(img_folder, "background.png")).convert()

#font
this_font = pygame.font.SysFont('Consolas', 28)

all_sprites = pygame.sprite.Group() # creates a sprite group
mobs = pygame.sprite.Group() # creates a mob sprite group
bullets = pygame.sprite.Group() # creates a bullet sprite group
mob_bullets = pygame.sprite.Group()



class Player(pygame.sprite.Sprite):
    def __init__(self): # Constructor
        pygame.sprite.Sprite.__init__(self) # Constructor
        self.image = pygame.image.load(os.path.join(img_folder, "player.png")).convert() # where sprite is located
        self.image.set_colorkey(WHITE) # hides the color black on the sprite
        self.rect = self.image.get_rect() # hitbox for sprite
        self.rect.centerx = (WIDTH / 2) # places sprite at WIDTH / 2 (center of screen)
        self.rect.bottom = (HEIGHT) # places bottom of sprite at HEIGHT (bottom of screen)
        self.difficulty = 0 # based off HR, keep at 1 for debugging
        self.x_speed = 0 # x_speed for sprite
        self.y_speed = 0 # y speed for sprite
        self.time_last_shot = pygame.time.get_ticks()

    def update(self):
        self.x_speed = 0
        keystate = pygame.key.get_pressed()
        # player movement events
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]: # if the player presses left or a
            self.x_speed = -5 # move the player left -5 pixels
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]: # if the player presses right or d
            self.x_speed = 5 # move the player right 5 pixels
        if keystate[pygame.K_LEFT] and keystate[pygame.K_RIGHT] or keystate[pygame.K_a] and keystate[pygame.K_d]: # if the player presses both left and right or a and d
            self.x_speed = 0 # the player stays in place

        if self.rect.right > WIDTH: # if the player attempts to move right, out of bounds
            self.rect.right = WIDTH # keep player's right at width
        if self.rect.left < 0: # if the player attempts to move left, out of bounds
            self.rect.left = 0 # keep the player's right at 0

        self.rect.x += self.x_speed # modifies the player's x position based on x speed

    def shoot(self): # this function occurs when the player shoots
        now = pygame.time.get_ticks()
        if now - self.time_last_shot > 10:
            bullet = Bullet(self.rect.centerx, self.rect.top) # this determines where the bullet is spawned
            all_sprites.add(bullet) # adds the bullet to the sprite list
            bullets.add(bullet) # adds the bullet to the bullets sprite list
            self.time_last_shot

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -50

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite): # creates a mob object
    def __init__(self, id): # constructor
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.image = pygame.image.load(os.path.join(img_folder, "enemy.png")).convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect() # hitbox of sprite equal to dimension of spite
        self.rect.x = random.randrange(WIDTH - self.rect.width) # this determines
        self.rect.y = random.randrange(-100, -50)
        self.y_speed = random.randrange(5, 8) 
        self.x_speed = random.randrange(-5, 5)
        #self.cool_down = 100
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if self.rect.top > HEIGHT + 50 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.y_speed = random.randrange(5, 8)
            self.x_speed = random.randrange(-5, 5)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > 2000:
            bullet = Mob_Bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            mob_bullets.add(bullet)
            self.last_shot_time = now
    
class Mob_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = 25
    
    def update(self):
        self.rect.y += self.y_speed
        if self.rect.top > HEIGHT:
            self.kill()

player = Player() # creates player object
all_sprites.add(player) # adds player object to sprite group


for i in range(8):
    m = Mob(i)
    all_sprites.add(m)
    mobs.add(m)

#opens and listens to COM4 port
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM4"
serialInst.open()

def main_menu():
	menu_font = pygame.font.Font(None, 36)
	menu_items = ["Start", "High Score", "Exit"]
	selected_item = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					selected_item = (selected_item + 1) % len(menu_items)
				elif event.key == pygame.K_UP:
					selected_item = (selected_item - 1) % len(menu_items) 
				elif event.key == pygame.K_RETURN:
					if menu_items[selected_item] == "Start":
						return
					elif menu_items[selected_item] == "High Score":
						print("High Score not implemented yet")
					elif menu_items[selected_item] == "Exit":
						pygame.quit()
						quit() 

		screen.fill(WHITE)
		for i, item in enumerate(menu_items):
			color = GREEN if i == selected_item else BLACK
			text = menu_font.render(item, True, color)
			text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
			screen.blit(text, text_rect)

		pygame.display.flip()
		clock.tick(FPS)

main_menu()
# Game Loop
running = True
while running:
    # Update heart rate
    file = open("D:\Archive Storage\python\pulse rulse\log.txt", "r")
    heart_rate = int(file.read())
    file.close()

    if serialInst.in_waiting:
        packet = serialInst.readline()
        heart_rate = int(packet.decode('utf'))
        file1 = open("D:\Archive Storage\python\pulse rulse\log.txt", "w")
        file1.write(str(heart_rate))
        file1.close()

    # Process Input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:  # player hits [X] on window
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()  # updates all sprites in group

    # check to see if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob(hit)
        all_sprites.add(m)
        mobs.add(m)

    # makes the mobs fire every shot
    for mob in mobs:
        mob.update()
        if random.random() < 0.01:
             mob.shoot()

    hits = pygame.sprite.spritecollide(player, mob_bullets, True)
    if hits:
        running = False

    # checks to see if mob collides with player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Draw / Render
    screen.blit(background, (0, 0))

    all_sprites.draw(screen)
    screen.blit(this_font.render(str(heart_rate), False, YELLOW), (430, 0))

    # after drawing everything, flip the display
    pygame.display.flip()

    # keep loop running at the right speed
    clock.tick(30)  # 60 updates every second


    


pygame.quit()                                           # closes the window