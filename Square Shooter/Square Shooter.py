import pygame
import random

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

class Gun:
    def __init__(self, screen_width, screen_height, full_height):
        imageUp = pygame.image.load("upGun.png").convert_alpha()
        imageDown = pygame.image.load("downGun.png").convert_alpha()
        imageLeft = pygame.image.load("leftGun.png").convert_alpha()
        imageRight = pygame.image.load("rightGun.png").convert_alpha()
        self.aim = [imageUp, imageLeft, imageDown, imageRight]
        
        shootUp = pygame.image.load("upGunShoot.png").convert_alpha()
        shootDown = pygame.image.load("downGunShoot.png").convert_alpha()
        shootLeft = pygame.image.load("leftGunShoot.png").convert_alpha()
        shootRight = pygame.image.load("rightGunShoot.png").convert_alpha()        
        self.flare = [shootUp, shootLeft, shootDown, shootRight]
        
        for i in range(4):
            self.aim[i] = pygame.transform.scale(self.aim[i], (50, 50)) 
            self.flare[i] = pygame.transform.scale(self.flare[i], (50, 50))
        self.center = [[screen_width/2 - 25 , (screen_height/2 + 5) + full_height], [screen_width/2 - 25, (screen_height/2 + 5) + full_height], [screen_width/2 - 25, (screen_height/2 + 5) + full_height], [screen_width/2 - 25, (screen_height/2 + 5) + full_height]]
        
        self.tip = [[screen_width/2 - 40 , (screen_height/2 - 25) + full_height], [screen_width/2 - 55, (screen_height/2 - 5) + full_height], [screen_width/2 - 35, (screen_height/2 + 35) + full_height], [screen_width/2 + 5, (screen_height/2 - 5) + full_height]]
        
        
class Heart:
    def __init__(self, screen_width):
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 30)) 
        heart1 = [screen_width - 250, 0]
        heart2 = [screen_width - 200, 0]
        heart3 = [screen_width - 150, 0]
        heart4 = [screen_width - 100, 0]
        heart5 = [screen_width - 50, 0]
        self.location = [heart1,heart2,heart3,heart4,heart5]
       
class Block(pygame.sprite.Sprite):  
    def __init__(self, color, width, height, speed, direction):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.direction = direction
        self.speed = speed
        
    def update(self):
        if self.direction == 0:
            self.rect.y += self.speed 
        elif self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == 2:
            self.rect.y -= self.speed    
        elif self.direction == 3:
            self.rect.x -= self.speed        
        
# Initialize Pygame
pygame.init()

# gun sound
gunSound = pygame.mixer.Sound("GDYN_Punching_Perc_PRO_SH - 8.aiff")

#music
song1 = pygame.mixer.Sound("Motel_Rock.aiff")
song1.play(-1)
# Set the height and width of the screen
screen_width = 600
screen_height = 600
full_height = 35
screen = pygame.display.set_mode([screen_width, screen_height + full_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite. 
# All blocks 
all_sprites_list = pygame.sprite.Group()

#size of rectangles
width = 25
height = 25




# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Black bar on top of screen 
statusBar = pygame.Surface([screen_width, full_height])
statusBar.fill(BLACK)

#Namw Window
pygame.display.set_caption("Square Shooter")

#Initializes gun
midGun = Gun(screen_width, screen_height, full_height)

#Initializes heart
life = Heart (screen_width)



font = pygame.font.Font(None, 32) 

start_message = 'Press space bar to start game. C for controls'
retry_message = font.render("Press space bar to retry", True, BLACK, WHITE)


highscore = 0
#How long the gun shoots
shootTime = 3
#Increases rate of blocks
difficulty = 0
#Squares hit
score = 0
#Direction of gun
direction = 0
# block speed
speed = 3
#life
hearts = 5
#Number of loops
loops = 0

shooting = False
answer = False
updated_score = False
instructions = False
lost = False

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 
        elif not answer:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    answer = True
                elif event.key == pygame.K_c:
                    instructions = True 
                    instruct = pygame.image.load("Instructions.png")        
                    instruct = pygame.transform.scale(instruct, (screen_width + 50, screen_height)) 
                    screen.fill(WHITE)
                    screen.blit(instruct,(-50,0))                    
        elif event.type == pygame.KEYDOWN and answer:
            if event.key == pygame.K_w:
                direction = 0
            elif event.key == pygame.K_a:
                direction = 1
            elif event.key == pygame.K_s:
                direction = 2
            elif event.key == pygame.K_d:  
                direction = 3
            elif event.key == pygame.K_UP:
                direction = 0
            elif event.key == pygame.K_LEFT:
                direction = 1
            elif event.key == pygame.K_DOWN:
                direction = 2
            elif event.key == pygame.K_RIGHT:     
                direction = 3
            if event.key == pygame.K_SPACE and not lost:
                shooting = True
                gunSound.play()
                for block in block_list:
                    if direction == 0:
                        if block.rect.y < height + 3 + full_height and block.rect.x > (screen_width/2) - (width*2) and block.rect.x < (screen_width/2) + (width*2):
                            block_list.remove(block)
                            all_sprites_list.remove(block) 
                            score += 1
                     
                    elif direction == 1:
                        if block.rect.x < width + 5 and block.rect.y > (screen_height/2 + full_height) - (height*2) and block.rect.y < (screen_height/2 + full_height) + (height*2):
                            block_list.remove(block)
                            all_sprites_list.remove(block)
                            score += 1
                       
                    elif direction == 2:
                        if block.rect.y > screen_height + full_height - (height+ 5) and block.rect.x > (screen_width/2) - (width*3) and block.rect.x < (screen_width/2) + (width*2):
                            block_list.remove(block)
                            all_sprites_list.remove(block)  
                            score += 1
                           
                    elif direction == 3:
                        if block.rect.x > screen_width - (width + 5) and block.rect.y > (screen_height/2 + full_height) - (height*2) and block.rect.y < (screen_height/2 + full_height) + (height*3):
                            block_list.remove(block)
                            all_sprites_list.remove(block) 
                            score += 1
                            
            elif event.type == pygame.KEYDOWN and lost:
                #Reinitialize everything
                if event.key == pygame.K_SPACE:
                    shooting = False
                    for item in block_list:
                        block_list.remove(item)
                    for item in all_sprites_list:
                        all_sprites_list.remove(item)                       
                    shootTime = 3
                    difficulty = 0
                    
                    score = 0
                    loops = 0
                    direction = 0
                    
                    # block speed
                    speed = 3
                    
                    #life
                    hearts = 5
                    answer = False
                    
                    instructions = False
                    lost = False
                    updated_score = False
                        
    if not answer and not instructions:
        screen.fill(WHITE)
        start = font.render(start_message, True, BLACK, WHITE)
        screen.blit(start, (50,screen_height/2))   
        
    elif answer and not lost:
        if hearts <= 0:
            lost = True
        
        if loops == 0:
            # Set location for the block
            randNum = random.randrange(4)
                    
            
            # This represents a block
            block = Block(BLUE, width, height,speed, randNum)    
            if randNum == 0:
                block.rect.x = 0
                block.rect.y = full_height
            elif randNum == 1:
                block.rect.x = 0
                block.rect.y = screen_height + full_height - (height + 1) 
            elif randNum == 2:
                block.rect.x = screen_width - (width + 1)
                block.rect.y = screen_height + full_height - (height + 1)
            elif randNum == 3:
                block.rect.x = screen_width - (width + 1)
                block.rect.y = full_height
                
            # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)    
        
        # Clear the screen
        screen.fill(WHITE)
        
        #Status Bar
        screen.blit(statusBar,(0,0))
        #message
        text = font.render('Score: ' + str(score), True, WHITE, BLACK)
        screen.blit(text, (0,0))
        
        #Show hearts
        for i in range(hearts):
            screen.blit(life.image, life.location[i])
            
        #Shoot Gun
        if (shooting):
            screen.blit(midGun.flare[direction], midGun.tip[direction])
            shootTime -= 1
            if shootTime == 0:
                shootTime = 5
                shooting = False
                
        #Makes squares move
        screen.blit(midGun.aim[direction], midGun.center[direction])
        
        # Remove the block if it flies up off the screen
        for block in block_list: 
            if block.rect.y < -10 + full_height:
                block_list.remove(block)
                all_sprites_list.remove(block)    
                hearts -= 1
            elif block.rect.y > screen_height + 10 + full_height:
                block_list.remove(block)
                all_sprites_list.remove(block)     
                hearts -= 1
            elif block.rect.x > screen_width + 10:
                block_list.remove(block)
                all_sprites_list.remove(block)       
                hearts -= 1
            elif block.rect.x < -10:
                block_list.remove(block)
                all_sprites_list.remove(block)           
                hearts -= 1
        
        #Moves blocks
        all_sprites_list.update()
        # Draw all the sprites
        all_sprites_list.draw(screen)
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # Limit to 60 frames per second
        clock.tick(50)
        
        loops += 1
        
        #Increase difficulty
        if score == 5:
            difficulty = 20
            speed = 5
        elif score == 10:
            speed = 7
            difficulty = 40  
        elif score == 25:
            difficulty = 50
    
        elif score == 34:
            difficulty = 55      
            
        elif score == 50:
            difficulty = 60  
            
            
        elif score == 70:
            difficulty = 65 
            
        elif score == 100:
            speed = 8
            
        elif score == 130:
            speed = 9 
            
        elif score == 160:
            speed = 10
            
        elif score == 200:
            difficulty = 70 
            
        if loops > 90 - difficulty:
            loops = 0
    elif lost:
        screen.fill(WHITE)
        if highscore >= score and not updated_score:
            endMessage = font.render("Final score: " + str(score), True, BLACK, WHITE)
            leaderboard = font.render("High score: " + str(highscore), True, BLACK, WHITE)
        else:
            if not updated_score:
                highscore = score
                updated_score = True
            
            endMessage = font.render("New Highscore!", True, BLACK, WHITE)
            leaderboard = font.render("High score: " + str(highscore), True, BLACK, WHITE)

        screen.blit(leaderboard, (50,screen_height/3 + 50))
        screen.blit(endMessage, (50,screen_height/3)) 
        screen.blit(retry_message, (50,screen_height/2))
    pygame.display.update() 
            
        
pygame.quit()