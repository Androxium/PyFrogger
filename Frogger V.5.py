'''Author: Thomas Cheng
   Date: May 30, 2017
   Description: This is the the Frogger game. Below are the different additions made
       to pyFrogger.
   
   v.1 - Added basic sprite objects to the game, and movement to the log and car
       sprite objects
   v.2 - Added collision detection so for the vehicles as well as log
   v.3 - Added a timer at the bottom of the screen
   v.4 - Added a life system that displays the player's lives as circles
   v.5 - Added functional score to the game
   v.6 - Added highscore to the game 
   v.7 - Added a start screen to the game
   v.8 - Added frog, log, life, and vehicle sprites to the game
   v.9 - Added music and sound effects to the game
   v.10 - Added a snake obstacle the player must dodge
'''

# Import and Initialize 
import pygame, pySprites, random
pygame.init()
pygame.mixer.init()

def start_screen(highscore):
    ''''''
    
    # Dispay
    screen = pygame.display.set_mode((660, 624))
    pygame.display.set_caption('pyFrogger!')
    
    # Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # BACKGROUNG SPRITES
    # create the river
    river = pySprites.River((screen.get_width(), 216), 65, 0)
    
    # create the grass zones
    bottom_position = [589, 309, 64]
    grass = []
    for iteration in xrange (3):
        grass.append(pySprites.Grass(screen, (0, 100, 0), bottom_position[iteration]))
    
    highScore = pySprites.HighScore(highscore)
    
    # creating the frog sprite
    frog = pySprites.Frog(screen, 589)
    
    allSprites = pygame.sprite.OrderedUpdates(river, grass, frog, highScore)
    
    # title font and label
    titleFont =  pygame.font.Font("./myTexts/PixelFlag.ttf", 90)
    titleText = titleFont.render('{FROGGER}', 1, (255, 255, 255))
    
    # flashing "press space to continue" label
    messageFont = pygame.font.Font('./myTexts/PixelFlag.ttf', 35)
    
    # load background music
    pygame.mixer.music.load('./mySounds/Frogger-Menu-Music.mp3')
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
    
    # Action via ALTER
       
    # Assign
    clock = pygame.time.Clock()
    keepGoing = True
    colour = 255
    factor = 3    

    pygame.mouse.set_visible(False)
       
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Events
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.mixer.music.fadeout(1000)
                return False                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    frog.hop_sound()
                    frog.move_right()
                elif event.key == pygame.K_LEFT:
                    frog.hop_sound()
                    frog.move_left()
                elif event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    pygame.mixer.music.fadeout(1000)
                    return False
                elif event.key == pygame.K_SPACE:
                    keepGoing = False
                    pygame.mixer.music.fadeout(1000)
                    return True             
        
        # make the continue message blink
        messageText = messageFont.render('(PRESS SPACEBAR TO CONTINUE)', 1, (colour, colour, colour))        
        colour -= factor 
        if colour <= 0 or colour >= 255:
            factor = -factor  
            
        # Refresh
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)        
        
        screen.blit(titleText, (135, 126))
        screen.blit(messageText, (141, 465))
        
        pygame.display.flip()        

    pygame.time.delay(1500)
    
def main_gameloop(highscore):
    '''This is the main function for the Frogger game. This function accepts one
    parameter. "highscore": a whole number used to display the player's current
    high score. This function returns one value. A whole number stored in 
    the scorekeeper class.'''
    
    # Dispay
    screen = pygame.display.set_mode((660, 624))
    pygame.display.set_caption('pyFrogger!')
    
    # Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    
    # BACKGROUNG SPRITES
    # create the river
    river = pySprites.River((screen.get_width(), 213), 65, 0)
    
    # create the grass zones
    bottom_position = [589, 309, 64]
    grass = []
    for iteration in xrange (3):
        grass.append(pySprites.Grass(screen, (0, 100, 0), bottom_position[iteration]))
    
    botSprites = pygame.sprite.OrderedUpdates(river, grass)
    
    
    # MOVING / MIDDLE SPRITES
    # creating the frog sprite
    frog = pySprites.Frog(screen, 589)
    
    velocities = [-2, 3, -4, 2, -5, -3, 4]
    
    # create the logs
    log_centers = [[(119, 259), (450, 259)], [(461, 224), (91, 224)], [(550, 189)],\
                [(50, 154), (407, 154)], [(105, 119), (525, 119)], [(48, 84), (425, 84)]]
    logs = []
    for log_row in xrange (len(log_centers)):
        log_speed = velocities[random.randrange(0, len(velocities))]
        for log in xrange (len(log_centers[log_row])):
            logs.append(pySprites.Logs(screen, log_centers[log_row][log], \
                                       log_speed, random.randint(1, 3)))
    logGroup = pygame.sprite.OrderedUpdates(logs)
    
    # creates the vehicles
    vehicle_centers = [[(450, 539)], [(100, 504), (500, 504)], \
                [(300, 469)], [(50, 434), (450, 434)], \
                [(79, 399), (450, 399)], [(300, 364)], [(485, 329), (150, 329)]]
    vehicles = []
    for vehicle_row in xrange (len(vehicle_centers)):
        car_speed = velocities[random.randrange(0, len(velocities))]
        for car in xrange (len(vehicle_centers[vehicle_row])):
            vehicles.append(pySprites.Vehicle(screen, \
                                        vehicle_centers[vehicle_row][car], car_speed))
    vehicleGroup = pygame.sprite.OrderedUpdates(vehicles)
    
    snake = pySprites.Snake(screen, 294)
    
    # creating the midSprites group that will hold all the middle sprites
    midSprites = pygame.sprite.OrderedUpdates(logGroup, vehicleGroup, snake, frog)
    
    
    # HIGH SPRITES
    # creating the timer
    timer_bar = pySprites.Timer_Bar((450, 10), 600, 545, 1)
    timer_text = pySprites.Timer_Text(555, screen.get_height())
    
    # create the score keeper
    scorekeeper = pySprites.ScoreKeeper(10)
    
    # displays the players lives
    life_right_pos = [646, 621, 595]
    lives = []
    for iteration in xrange (len(life_right_pos)):
        lives.append(pySprites.LifeKeeper(7, life_right_pos[iteration]))
    lifeGroup = pygame.sprite.Group(lives)
    
    life_text = pySprites.Life_Text(0, 567)
    
    highScore = pySprites.HighScore(highscore)
    
    # creating the highSprites group that will hold all the middle sprites
    highSprites = pygame.sprite.OrderedUpdates(timer_bar, timer_text, scorekeeper,\
                                    lives, life_text, highScore)
        
    # putting all the sprite groups into one allSprites group
    allSprites = pygame.sprite.OrderedUpdates(botSprites, midSprites, highSprites)
    
    # load background music
    pygame.mixer.music.load('./mySounds/Frogger-Main-Theme.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)    
    
    # Action via ALTER
    
    # Assign
    clock = pygame.time.Clock()
    keepGoing = True
    life_index = 0
    lost_life = False
    
    pygame.mouse.set_visible(False)
    
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.mixer.music.fadeout(1000)
            # checks for if the player has pressed the directional keys
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    frog.hop_sound()
                    frog.move_up()
                    # checks to see if the frog has passed it's current max distance
                    if frog.distance_comparison(frog.rect.top):
                        scorekeeper.add_points()
                elif event.key == pygame.K_DOWN:
                    frog.hop_sound()
                    frog.move_down()
                elif event.key == pygame.K_RIGHT:
                    frog.hop_sound()
                    frog.move_right()
                elif event.key == pygame.K_LEFT:
                    frog.hop_sound()
                    frog.move_left()      
        
        # checks to see if the snake is moving along the middle grass section
        if not snake.is_moving():
            if random.randrange(0, 100) == 19:
                snake.start_moving()
                
        # checks to see if the player has timed out
        if timer_bar.has_reset():
            frog.reset()        
            
        # checks to see if the frog has collided with a vehicle
        if pygame.sprite.spritecollide(frog, vehicleGroup, False) and not lost_life:
            frog.squished_sound()
            frog.reset() 
            lost_life = True
            timer_bar.reset()
            
        # checks to see if the frog has collided with the snake
        if snake.rect.colliderect(frog.rect):
            lost_life = True    
        
        # checks to see if the frog has landed on a log    
        log_hitList = pygame.sprite.spritecollide(frog, logGroup, False)
        for log in log_hitList:
            
            if (frog.rect.centery == log.rect.centery):
                if (frog.rect.left >= log.rect.left) and (frog.rect.right <= log.rect.right):
                    logSpeed = log.get_speed()
                    frog.log_movement(logSpeed)
        
        # checks to see if the player missed the log                    
        if not log_hitList and frog.rect.colliderect(river.rect):
            frog.splash_sound()
            frog.reset() 
            lost_life = True
            timer_bar.reset()

        # checks to see if the frog has reached the grass patch located at the
        # top of the screen, and has landed on that patch
        if frog.rect.centery == grass[-1].rect.centery:
            if (frog.rect.left >= grass[-1].rect.left) and \
              (frog.rect.right <= grass[-1].rect.right):
                
                for log in xrange (len(logs)):
                    logs[log].speed_up(1)      
                for car in xrange (len(vehicles)):
                    vehicles[car].speed_up(2)
                grass[-1].half_grass()
                scorekeeper.crossing_complete()
                
            else:
                lost_life = True
            
            frog.reset()
            timer_bar.reset()
        
        # checks to see if the player has lost a life
        if lost_life:
            lives[life_index].kill() 
            life_index += 1
            lost_life = False
            frog.reset_distance_travelled()
            
        # Refresh
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)        
        
        pygame.display.flip()
        
        # FOLLOWING CODE IS NOT PART OF THE REFRESH SECTION
        # It is there to avoid the image flickering once game ends
        
        # checks to see if the player has lost all of their lives    
        if len(lifeGroup) == 0:
            pygame.time.delay(750)
            endgame_message(allSprites, screen, background, 'GAME OVER') 
            pygame.mixer.music.fadeout(1000)
            keepGoing = False
            
        # checks to see if the player has successfully made it to the oter side 3 times
        if scorekeeper.beat_game():
            pygame.time.delay(750)
            endgame_message(allSprites, screen, background, 'WINNER!')
            pygame.mixer.music.fadeout(1000)
            keepGoing = False        
            
    pygame.mouse.set_visible(True)
    pygame.time.delay(1500)
    
    return scorekeeper.get_score()

def endgame_message(allSprites, screen, background, message):
    '''This function is used to display the endgame message. This function returns
    no values and accpets four parameters. "allSprites": a pygame.Group object.
    "screen": a copy of the pygame.screen object. "background": a copy of the
    pygame.Surface object. "message": a string value.'''
        
    allSprites.clear(screen, background)
    
    display_font = pygame.font.Font('./myTexts/Abstract.TTF', 25)
    display_label = display_font.render(message, 1, (255, 255, 255))
    
    screen.blit(display_label, (25, 224))
    
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    '''This is the main function that will call the start screen function and
    main_gameloop function.'''
    
    current_highscore = 0
    keepPlaying = True
    while keepPlaying:
        keepPlaying = start_screen(current_highscore)
        if keepPlaying:
            highscore = main_gameloop(current_highscore)
            current_highscore = max(highscore, current_highscore)
    pygame.quit()

main()