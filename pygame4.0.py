# 1 - Import library
import pygame
import math
import random
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
width, height = 800,800
screen = pygame.display.set_mode((width,height))
mouthpos = [160,250]
m = 0
tongues = []
food = [[800,100]]
foodtimer = 70
foodtimer1 = 0
trash = [[800,100]]
trashtimer = 100
trashtimer1 = 0
healthvalue = 194
running = 1
score = 0
pygame.mixer.init()

# 3 - Load images
mouth = pygame.image.load("resources/images/mouth.png")
background = pygame.image.load("resources/images/grass.png")
tongue = pygame.image.load("resources/images/tongue.png")
foodimg = pygame.image.load("resources/images/food.png")
trashimg = pygame.image.load("resources/images/trash.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
timeup = pygame.image.load("resources/images/timeup.png")
# 3.1 - Load audio
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - Keep looking through
while running:
    foodtimer -= 1
    trashtimer -= 1
    exitcode = 1
     # 5 - clear the screen before drawing it again
    screen.fill(0)
     # 6 - draw the screen elements
    # draw background
    screen.blit(background,(0,0))
   
    # set rotation
    position = pygame.mouse.get_pos()
    # angle = math.atan2(position[1] - (playerpos[1]+32), position[0]-(playerpos[0]+26))
    angle = 0
    if m != 0:
        angle = math.atan2(position[1] - (mouthpos[1]+mouthrot.get_rect().height/2), position[0]-(mouthpos[0]+mouthrot.get_rect().width/2)) # plus half the width and height so that it uses the center
    else:
        m = 1
    mouthrot = pygame.transform.rotate(mouth, 90-angle*57.29) #BALLBALL: now it looks like the mouth follows your mouse. you can change it back to 270-angle*57.29, it looks wierd
    # print mouthrot
    mouthpos1 = (mouthpos[0]-(mouthrot.get_rect().width-545)/2, mouthpos[1]-(mouthrot.get_rect().height-545)/2) #mouthpos
    screen.blit(mouthrot, mouthpos1)

    # draw tongue
    for tongu in tongues:
        index = 0
        tongu[0] += math.cos(tongu[2])*30
        tongu[1] += math.sin(tongu[2])*30
        if tongu[0] > width or tongu[0] < 0 or tongu[1] > height or tongu[1] < 0:
            tongues.pop(index)
        else:
            index += 1
    for tongu in tongues:
        tongue1 = pygame.transform.rotate(tongue, 90 - tongu[2]*57.29)
        screen.blit(tongue1, (tongu[0], tongu[1]))

    # draw food
    # food loop
    if foodtimer == 0:
        food.append([800,random.randint(50,500)])
        foodtimer = 100 - (foodtimer1 * 2)
        if foodtimer1 >= 35:
            foodtimer1 = 35
        else:
            foodtimer1 += 5

    # define food_rect (here comes the food)
    index1 = 0
    for sandwich in food:    
        foodrect = pygame.Rect(foodimg.get_rect())
        foodrect.top = sandwich[1]
        foodrect.left = sandwich[0]
        foodrect.bottom = sandwich[1] + foodimg.get_height()
        foodrect.right = sandwich[0] + foodimg.get_width()
        if foodrect.left < 150 or foodrect.top < 0 or foodrect.bottom > height:
            food.pop(index1)
        else:
            sandwich[0] -= 10
            index1 += 1

    for sandwich in food:
        screen.blit(foodimg, (sandwich[0],sandwich[1]))

    # draw trash
    # trash loop
    if trashtimer == 0:
        trash.append([800,random.randint(50,450)])
        trashtimer = 80 - (trashtimer1 * 2)
        if trashtimer1 >= 20:
            trashtimer1 = 20
        else:
            trashtimer1 += 5

    # define trash_rect (here comes the trash)
    index2 = 0
    for box in trash:    
        trashrect = pygame.Rect(trashimg.get_rect())
        trashrect.top = box[1]
        trashrect.left = box[0]
        trashrect.right = box[0] + trashimg.get_width()
        trashrect.bottom = box[1] + trashimg.get_height()
        if trashrect.right < 150 or trashrect.top < 0 or trashrect.bottom > height or trashrect.right < 0:
            trash.pop(index2)
        else:
            box[0] -= 5
            index2 += 1

    index2 = 0#trash
    for box in trash:
        screen.blit(trashimg, (box[0],box[1]))
        trashrect.top = box[1]
        trashrect.left = box[0]
        trashrect.right = box[0] + trashimg.get_width()
        trashrect.bottom = box[1] + trashimg.get_height()
        # eat trash (collisions)
        index4 = 0 #tongue
        collide = False
        for tongu in tongues:
            # define tongue_rect
            tongurect = pygame.Rect(tongue.get_rect())
            tongurect.left = tongu[0] 
            tongurect.top = tongu[1]
            tongurect.right = tongu[0] + tongue.get_width()
            tongurect.bottom = tongu[1] + tongue.get_height()
            
            if trashrect.colliderect(tongurect):
               trash.pop(index2)
               tongues.pop(index4)
               healthvalue -= random.randint(10,20)
           
            else:
               index4 += 1
               collide = True
        if collide == False:
             index2 += 1


    index3 = 0 #food
    for sandwich in food:
        screen.blit(foodimg, (sandwich[0],sandwich[1]))
        foodrect.top = sandwich[1]
        foodrect.left = sandwich[0]
        foodrect.bottom = sandwich[1] + foodimg.get_height()
        foodrect.right = sandwich[0] + foodimg.get_width()
        # eat food (collisions)
        index1 = 0 #tongue
        collide = False
        for tongu in tongues:
            # define tongue_rect
            tongurect = pygame.Rect(tongue.get_rect())
            tongurect.left = tongu[0] 
            tongurect.top = tongu[1]
            tongurect.right = tongu[0] + tongue.get_width()
            tongurect.bottom = tongu[1] + tongue.get_height()
            
            if foodrect.colliderect(tongurect):
               food.pop(index3)
               tongues.pop(index1)
               collide = True
               score += 1
        
            else:
               index1 += 1
               collide = True
        if collide == False:
             index3 += 1

    # draw clock
    font = pygame.font.Font(None,24)
    survivedtext = font.render(str((60000-pygame.time.get_ticks())/60000)+":"+str((60000-pygame.time.get_ticks())/1000%60).zfill(2),True,(255,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [795,5]
    screen.blit(survivedtext, textRect)

    # draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range (healthvalue):
        screen.blit(health,(health1+8,8))

    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        # action to get food
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            tongues.append([mouthpos[0]+mouth.get_width()/2,mouthpos[1]+mouth.get_height()/2,angle]) #BALLBALL: I guess if you size down your image and play around with the coordinator of these tongues, it would look better

    # 10 - Win/lose check
    if pygame.time.get_ticks() >= 60000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0

    # 11 - win/lose display
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Score: "+str(score), True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Score: "+str(score), True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(timeup, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()















