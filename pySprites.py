'''Author: Thomas Cheng
   Date: May 30, 2017
   Description: This is the module that contains all the frogger sprites required
   for the frogger game I created.
'''

import pygame, random

class Logs(pygame.sprite.Sprite):
    '''This Log class is used to create log objects for the user to interact with.
    This class inherits from pygame's Sprite class.'''
    
    def __init__(self, screen, center, speed, log_type):
        '''This function initializes the log object. This function accepts 4
        parameters. "screen": a copy of a pygame display object. "center": a tuple
        representing an xy co-ord. "speed": an integer value used to alter the
        log's centerx value. "log_type": an whole number between 1-3 inclusive
        used to determine what log is being intialized.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        # loading different log images
        self.__log_dimensions = []
        for log in xrange (3):
            self.__log_dimensions.append(pygame.image.load('./myImages/log' + str(log) + '.png'))

        self.image = self.__log_dimensions[log_type-1]
            
        self.image = self.image.convert()
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.__dx = speed
        self.__screen = screen
        
    def get_speed(self):
        '''This function serves as an accessor method for the logs center. This
        function accepts no values and will return the co-ordinates for the 
        logs center'''
        
        return self.__dx
    
    def update(self):
        '''This function will update the log's current centerx value by
        the "speed" paratmeter passed into the __init__ function. It will also
        reset the log's position once it has left the screen's boundaries. This 
        function accepts and returns no values.'''
        
        self.rect.centerx += self.__dx
        if (self.rect.right < 0):
            self.rect.left = self.__screen.get_width()
        elif self.rect.left > self.__screen.get_width():
            self.rect.right = 0
    
    def speed_up(self, factor):
        '''This function will increase the absolute value of self.__dx by a certain
        value. This function returns no values and accepts one parameter.
        "factor": an integer value used to alter the value of self.__dx.'''
    
        if self.__dx > 0:
            self.__dx += factor
        elif self.__dx < 0:
            self.__dx -= factor
            

class Frog(pygame.sprite.Sprite):
    '''This Frog class is used to create a player object for the use to interact
    with. This function inherits from pygame's Sprite class.'''
    
    def __init__(self, screen, bottom):
        '''This function initializes the Frog object. This function accepts 3
        parameters. "screen": a copy of a pygame display object. "bottom": a
        whole number used for the frog's rect.bottom value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        # loading the different frog images
        self.__frogimages = []
        for image in xrange(4):
            self.__frogimages.append(pygame.image.load('./myImages/frog' + str(image) + '.png'))
        self.image = self.__frogimages[0]
        
        self.__dx = 35
        self.__dy = 35
        self.__screen = screen 
        self.__max_bot = bottom
        self.__counter = 0
        
        # loading the different sound effects
        self.__hop = pygame.mixer.Sound('./mySounds/sound-frogger-hop.ogg')
        self.__hop.set_volume(0.7)
        self.__splash = pygame.mixer.Sound('./mySounds/splash.wav')
        self.__splash.set_volume(0.7)
        self.__squished = pygame.mixer.Sound('./mySounds/sound-frogger-squash.wav')
        self.__squished.set_volume(0.7)
        
        self.rect = self.image.get_rect()
        self.reset()
        
        self.__max_top = self.rect.top
        
    def move_up(self):
        '''This function moves the frog sprite up. This function accepts and
        returns no values.'''
        
        self.image = self.__frogimages[0]
        self.rect.centery -= self.__dy
        self.__hop.play()
        
    def move_down(self):
        '''This function moves the frog sprite down. This function accepts and
        returns no values.'''
        
        self.image = self.__frogimages[2]
        self.rect.centery += self.__dy
        self.__hop.play()
    
    def move_right(self):
        '''This function moves the frog sprite right. This function accepts and
        returns no values.'''
    
        self.image = self.__frogimages[1]
        self.rect.centerx += self.__dx
    
    def move_left(self):
        '''This function moves the frog sprite up. This function accepts and
        returns no values.'''
        
        self.image = self.__frogimages[3]
        self.rect.centerx -= self.__dx
    
    def hop_sound(self):
        '''This function plays the hopping sound effect once when it is called.
        This function does not accept or return any values.'''
        
        self.__hop.play()
        
    def splash_sound(self):
        '''This function plays the splash sound effect once when it is called.
        This function does not accept or return any values.'''
            
        self.__splash.play()   
        
    def squished_sound(self):
        '''This function plays the splash sound effect once when it is called.
        This function does not accept or return any values.'''
            
        self.__squished.play() 
        
    def reset(self):
        '''This function returns the frog sprite to it's starting position
        (the position where it was initialized), and resets the value for
        the frog's maximum distance traveled. This function accepts and returns
        no values'''
        
        self.rect.bottom = self.__max_bot
        self.rect.centerx = self.__screen.get_width()/2
        
    def reset_distance_travelled(self):
        '''This function resets the value stored in the instance variable
        "self.__max_top". This function accepts and returns no values.'''
        
        self.__max_top = self.rect.top
        
    def log_movement(self, direction):
        '''This function moves the frog centerx value by a certain value.
        This function returns no values and accepts 1 value. 
        "direction": an integer that is used to alter the frog's centerx value.'''
        
        self.rect.centerx += direction 
    
    def distance_comparison(self, position):
        '''This function compares the frog's current distance to it's maximum distance
        travelled. This function accepts one parameter. "position": a whole number
        representing the frog's current rect.top value. This function will return
        True if the frog's max position has changed, or False otherwise.'''
        
        if position < self.__max_top:
            self.__max_top = position
            return True
        else:
            return False
        
    def update(self):
        '''This function checks if the frog's edged has exceeded the screen's side
        edges or it's starting bottom value . This function accepts and returns
        no values.'''
        
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))
        
        # checks to see if the frog has reached it's max boundaries        
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
            
        if self.rect.bottom >= self.__max_bot:
            self.rect.bottom = self.__max_bot


class Grass(pygame.sprite.Sprite):
    '''This Grass class is used to create a grass object that will be used as
    the player's spawning / safe / end - zone. This clas inherits from
    pygame.sprite.Sprite.'''
    
    def __init__(self, screen, colour, bottom_position):
        '''This function initializes the grass object by calling it's "create_grass"
        function. This function returns no values and accepts 3 parameters.
        "screen": a copy of a pygame display object. "colour": an RGB tuple.
        "bottom_position": a whole number used for the grass' rect.bottom value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__width = screen.get_width()
        self.__colour = colour
        self.__bottom_position = bottom_position
        self.__screen = screen
        
        self.create_grass()
        
    def create_grass(self):
        '''This function creates the surface object used for the grass object.
        This functiom accepts and returns no values.'''
        
        self.image = pygame.Surface((self.__width, 30))
        self.image = self.image.convert()
        self.image.fill(self.__colour)
        
        self.rect = self.image.get_rect()
        self.rect.bottom = self.__bottom_position 
        self.rect.centerx = self.__screen.get_width()/2
        
    def half_grass(self):
        '''This function reduces the width of the grass object by half each time
        this function is called. This function accepts and returns no values.'''
        
        self.__width = self.__width / 2
        self.create_grass()


class Vehicle(pygame.sprite.Sprite):
    '''This class defines the Vehicle objects that the player must dodge. This class
    inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, screen, center, speed):
        '''This function initializes the car object. This function returns no 
        values and accepts 3 parameters. "screen": a copy of a pygame display object.
        "center": an xy tuple for the car's center co-ordinates. "speed": an
        integer value used to alter the car's centerx value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__vehicles = []
        for vehicle in xrange (6):
            self.__vehicles.append(pygame.image.load('./myImages/vehicle' + str(vehicle) + '.png'))
        
        # randomly selecting a vehicle image
        if speed > 0:
            vehicle_image = random.randint(0, 2)
        elif speed < 0:
            vehicle_image = random.randint(3, 5)
            
        self.image = self.__vehicles[vehicle_image]
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.__screen = screen
        self.__dx = speed
        
    def update(self):
        '''This function will alter the car's centerx value by the number of pixels
        passed in as "speed". It will also reset the car's position once the car
        has esceeded the screen's limits. This function accepts and returns no values.'''
        
        self.rect.centerx += self.__dx
        if (self.rect.right < 0):
            self.rect.left = self.__screen.get_width()
        elif self.rect.left > self.__screen.get_width():
            self.rect.right = 0
            
    def speed_up(self, factor):
        '''This function will increase the absolute value of self.__dx by a certain
        value. This function returns no values and accepts one parameter.
        "factor": an integer value used to alter the value of self.__dx.'''
        
        if self.__dx > 0:
            self.__dx += factor
        elif self.__dx < 0:
            self.__dx -= factor


class River(pygame.sprite.Sprite):
    '''This class defines the River object that will be used to for the second   
    half of the game. This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, dimensions, top_position, left_position):
        '''This function initalizes the car object. This function accepts three
        values. "dimensions": a tuple used for the river object's surface size.
        "top_position": a whole number used for the river's rect.top.
        "left_position": a whole number used for the river's rect.left.
        This function returns no values.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface(dimensions)
        self.image = self.image.convert()
        self.image.fill((0, 0, 155))
        
        self.rect = self.image.get_rect()
        self.rect.top = top_position
        self.rect.left = left_position
        
        
class Timer_Bar(pygame.sprite.Sprite):
    '''This class defines the Timer_Bar object that will be used as the countdown
    timer. This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, dimensions, top_position, right_position, deduction_value):
        '''This function initalizes the Timer_Bar object. This function accepts four
        values. "dimensions": a tuple used for the timer object's surface size.
        "top_position": a whole number used for the timer's rect.top.
        "left_position": a whole number used for the timer's rect.left.
        "deduction_value": a whole number used to alter the timer's length.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__counter = 0
        self.__dimensions = dimensions
        self.__timer_width = dimensions[0]
        self.__top_position = top_position
        self.__right_position = right_position
        self.__deduction_value = deduction_value
        
        self.timer_update(self.__dimensions)
    
    def timer_update(self, dimensions):
        '''This function is used to both create the initial timer bar, as well as
        update the timer bar's length each time this function is called. This funtion
        returns no values and accepts one parameter. "dimensions": a tuple representing
        the timer's dimensions.'''
        
        self.image = pygame.Surface(dimensions)
        self.image = self.image.convert()
        self.image.fill((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.right = self.__right_position
        self.rect.top = self.__top_position        
    
    def has_reset(self):
        '''This function's purpose is to determine whether the timer has reset to
        it's initial length. This function accepts no parameters. If the timer has
        reset, this function will return True, or False otherwise.'''
        
        if (self.__timer_width == self.__dimensions[0] or self.__timer_width == 0)\
          and self.__counter != 0:
            return True
        else:
            return False
    
    def reset(self):
        '''This function's purpose is to reset the timer's length by calling
        timer_update and passing in the original timer dimensions. This function
        accepts and returns no values.'''
        
        self.__timer_width = self.__dimensions[0]
        self.timer_update(self.__dimensions)
        
    def update(self):
        '''This function keeps track of the amount of time that has passed. After
        each second, it will call timer_update, passing in a smaller timer dimension.
        This function will also call the reset function once the timer length has
        reached zero. This function accepts and returns no values.'''
        
        self.__counter += 1
        if (self.__counter % 2 == 0):
            self.__timer_width -= self.__deduction_value
            
        if self.has_reset():
            self.reset()
        else:
            self.timer_update((self.__timer_width, self.__dimensions[1]))
                

class Timer_Text(pygame.sprite.Sprite):
    '''This class defines the text that will be displayed beside the timmer bar.
    This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, left_position, bot_position):
        '''This function will initialize the timer_text object. This function returns
        no values and accepts 2 parameters. "left_position": a whole number used for
        the text's rect.left value. "bot_position": a whole number used for the text's
        rect.bottom value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font('./myTexts/Pixeled.ttf', 15)
        self.image = self.__font.render('Timer', 1, (255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.left = left_position
        self.rect.bottom = bot_position


class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines the ScoreKeeper object which will be used to display
    the player's current game score. This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, add_points): 
        '''This function initializes the scorekeeper object. This function returns
        no values and accepts one parameter. "add_points": a whole number used
        to add to the player's points.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font('./myTexts/Pixeled.ttf', 11)
        self.__score = 0
        self.__add_points = add_points
        self.__levelCompletion = 0
    
    def add_points(self):
        '''This function will add points to the player's overall score. This
        function accepts and returns no values.'''
        
        self.__score += self.__add_points
    
    def get_score(self):
        '''This function is used as an accessor method for the player's points.
        This function accepts no parameters and returns one value. 
        "self.__score": a whole number representing the player's score.'''
        
        return self.__score
    
    def crossing_complete(self):
        '''This function will add 1 to the instance variable "self.__levelCompletion"
        each time it is called. This function accepts and returns no values.'''
        
        self.__levelCompletion += 1
        
    def beat_game(self):
        '''This function checks if "self.__levelCompletion" is equal to 3. If that
        is the case, this function returns True, and False otherwise. This function
        accepts no parameters.'''
        
        if self.__levelCompletion == 3:
            return True
        else:
            return False
        
    def update(self):
        '''This function will render the player's score and display it in the
        position specified by the user. This function accepts and returns no 
        values.'''
        
        self.__message = 'Score: %d' % self.__score
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        
        # position the score in the top left corner
        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.top = 0        


class HighScore(pygame.sprite.Sprite):
    '''This class defines the HighScore object that will keep track of the most
    recent highscore obtained by the player. This class inherits from
    pygame.sprite.Sprite.'''
    
    def __init__(self, highscore):
        '''This function initializes the highscore class. This function returns 
        no values, and accepts one parameter. "highscore": a whole number representing 
        the most recent highscore obtained by the player.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font('./myTexts/PixelFlag.ttf', 27)
        self.__highscore = highscore
            
    def update(self):
        '''This function will render the player's highscore and display it in the
        position specified by the user. This function accepts and returns no 
        values.'''
        
        self.__message = '{High Score: %d}' % self.__highscore
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        
        # position the score in the top left corner
        self.rect = self.image.get_rect()
        self.rect.left = 280
        self.rect.top = 5    
        
        
class LifeKeeper(pygame.sprite.Sprite):
    '''This class defines the LifeKeeper object used to display the player's
    remaining lives. This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self,top_position, right_position):
        '''This function initializes the LifeKeeper object. This function returns
        no values and accepts two parameters. "top_position": a whole number used 
        for the lifekeeper's rect.top value. "left_position": a whole number used for
        the lifekeeper's rect.left value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('./myImages/Life.png')
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.top = top_position
        self.rect.right = right_position
        
        
class Life_Text(pygame.sprite.Sprite):
    '''This class defines the Life_Text object that will be displayed beside
    the LifeKeeper object. This class inherits from pygame.sprite.Sprite.'''
    
    def __init__(self, top_position, right_position):
        '''This function initializes the Life_Text object. This function returns
        no values and accepts two parameters. "top_position": a whole number used 
        for the life_text's rect.top value. "left_position": a whole number used for
        the life_text's rect.left value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font('./myTexts/Pixeled.ttf', 11)
        self.image = self.__font.render('Lives', 1, (255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.right = right_position
        self.rect.top = top_position
        
        
class Snake(pygame.sprite.Sprite):
    '''This Snake class is used to create log objects for the user to interact with.
    This class inherits from pygame's Sprite class.'''
    
    def __init__(self, screen, centery):
        '''This function initializes the log object. This function accepts 4
        parameters. "screen": a copy of a pygame display object. "center": a tuple
        representing an xy co-ord. "speed": an integer value used to alter the
        log's centerx value.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('./myImages/snake.png')
        
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.left = screen.get_width()
        
        self.__dx = -5
        self.__screen = screen
        self.__movementToggle = False
    
    def reset(self):
        '''This function returns the snake sprite to it's starting position
        (the position where it was initialized), and sets a boolean variable to
        False. This function accepts and returns no values'''
        
        self.rect.left = self.__screen.get_width()
        self.__movementToggle = False
        
    def start_moving(self):
        '''This function sets a boolean toggle to True, causing the snake sprite
        to being moving across the screen. This function accepts and returns no
        values.'''
        
        self.__movementToggle = True
        
    def is_moving(self):
        '''This function serves as an accessor method and will return the boolean 
        value of the movement toggle instance variable.'''
        
        return self.__movementToggle
        
    def update(self):
        '''This function will check if the movement toggle is true and if so, will
        move the snake sprite across the screen. This function will also reset the
        snake once it has reached the other side of the screen and set the movement
        toggle to False. This function accepts no parameters and returns no values.'''
        
        if self.__movementToggle:
            self.rect.centerx += self.__dx
            
        if self.rect.right < 0:
            self.rect.left = self.__screen.get_width()
            self.__movementToggle = False            