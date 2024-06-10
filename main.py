import sys
import pygame
import random
from dinozavrik import DinoObject
from settings import Settings 
from cactus import Cactus
from cloud import Cloud
import time
from time import monotonic

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (63, 224, 7)
        self.settings = Settings()
        self.screen = self.settings.screen
        #self.btn_sound
    
    def draw(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(self.screen, self.inactive_color,(x, y, self.width, self.height))
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(self.screen, self.active_color,(x, y, self.width, self.height))
                if click[0] == 1:
                    """pygame.mixer.Sound.play(self.btn_sound)
                    pygame.time.delay(300)"""
                    if action is not None:
                        action()

class DinoGame:
    """Керування ресурсами, поведінкою гри"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = self.settings.screen
        pygame.display.set_caption("Dino")
        icon = pygame.image.load("kaktus.png")
        pygame.display.set_icon(icon)
        #self.bg_color = self.settings.bg_color
        self.dinosaur = DinoObject(self)
        self.make_jump = False
        self.counter_jump = 30
        self.usr_width = 40
        self.usr_height = 30
        self.usr_x = self.settings.screen_width//3
        self.usr_y = self.settings.screen_height-self.usr_height - 140
        self.cactus_arr = []
        self.clock = pygame.time.Clock()
        self.cactus_images = [pygame.image.load('kaktus.png'), pygame.image.load('kaktus.png'), pygame.image.load('kaktus.png')]
        self.cactus_size = [20, 485, 20, 485, 20, 485]
        self.cloud_image = pygame.image.load('cloud.png')
        self.cloud_width = 80
        self.clouds = []
        self.scores = 0
        self.above_cactus = False        
        pygame.mixer.music.load("sounds/Атмосфера войны во Вьетнаме или любая другая современная война.mp3")
        self.jump_sound = pygame.mixer.Sound('sounds/Bdish.wav')
        pygame.mixer.music.set_volume(0.25)

        self.scores = 0 
        self.max_score = 0
        self.max_above = 0
        self.showmenu = True
        self.menu_image = pygame.image.load('desert.jpg')
    
    def show_menu(self):
        start_btn = Button(200, 50)
        exit_btn = Button(200, 50)
        while self.showmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.blit(self.menu_image, (0, 0))
            self.print_text("BEGI DINOZAVRIK BEGI", 400, 100)
            start_btn.draw(470, 300, self.run_game)
            self.print_text("START", 500, 300)
            exit_btn.draw(470, 380, quit)
            self.print_text("QUIT", 500, 380)
            pygame.display.update()
                    
    
    
    def run_game(self):
        pygame.mixer.music.play(-1)
        self.array_cactus()
        #x = self.settings.screen_width
        #cl = Cloud(x, y, self.cloud_width, self.cloud_image, 1)
        for i in range(3):
            x = random.randrange(50, 1780)
            y = random.randint(0, 67)
            self.clouds.append(Cloud(x, y, self.cloud_width, self.cloud_image, 1))
        mode_game = True
        t = monotonic()
        while mode_game:

                if monotonic() - t > 1:
                    #print()
                    t = monotonic()
                    self.scores += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                keys = pygame.key.get_pressed()
                if keys [pygame.K_SPACE]:
                    self.make_jump = True
                if keys [pygame.K_ESCAPE]:
                    self.pause()
                if self.make_jump:
                    self.jump()
                #self.screen.fill(self.bg_color)
                self.screen.blit(self.settings.fon, (0, 0))
                for i in self.clouds:
                    i.move_cloud()
                self.dinosaur.blitme()
                self.draw_cactus_arr()
                self.clock.tick(59)
                if self.check_collision():
                    pygame.mixer.music.stop()
                    if self.scores > self.max_score:
                        self.max_score = self.scores
                    self.print_text("Game over, press Enter to play again, Esc to exit", 125, 300)
                    self.print_text('Max scores' + str(self.max_score), 225, 340)
                    pygame.display.update()
                    mode_game = self.game_over()
                self.print_text("Scores:" + str(self.scores), 850, 10)
                pygame.display.update()
                pygame.display.flip()
                #self.clock.tick(59)
                
    
    def jump(self):
        if self.counter_jump >= -30:
            if self.counter_jump == 30:
                pygame.mixer.Sound.play(self.jump_sound)
            self.dinosaur.rect.y -= self.counter_jump//2
            self.counter_jump -= 1
        else:
            self.dinosaur.rect.y = self.settings.screen_height//2+75
            self.counter_jump = 30
            self.make_jump = False
    
    
    def array_cactus(self):
        for i in range(3):
            choice = random.randrange(0,3)
            img = self.cactus_images[choice]
            width = self.cactus_size[choice*2]
            height = self.cactus_size[choice*2+1]
            self.cactus_arr.append(Cactus(self.settings.screen_width+300, height, width, img, 4))
    
    
    def draw_cactus_arr(self):
        for cactus in self.cactus_arr:
            check = cactus.move()
            if not check:
                radius = self.find_radius()
                choice = random.randrange(0, 3)
                img = self.cactus_images[choice]
                width = self.cactus_size[choice*2]
                height = self.cactus_size[choice*2+1]
                cactus.return_cactus(radius, height, width, img,)
               
    
    def find_radius(self):
        maximum = max ([self.cactus_arr[0].x, self.cactus_arr[1].x, self.cactus_arr[2].x])
        if maximum < self.settings.screen_width:
            radius = self.settings.screen_width
            if radius - maximum < 35:
                radius += 3
        else:
            radius = maximum
        choice = random.randrange(0, 5)
        if choice == 0:
            radius = random.randrange(10,15)
        else:
            radius = random.randrange(900,1000)
        return radius
    
    
    def print_text(self, message, x, y, font_color = (0, 0, 0), font_type = 'font/beer money.ttf', font_size = 30):
        self.screen = self.settings.screen
        self.message = message
        self.x = x
        self.y = y
        self.font_color = font_color
        self.font_type = pygame.font.Font(font_type, font_size)
        self.message = self.font_type.render(message, True, self.font_color)
        self.screen.blit(self.message, (self.x, self.y))
        #self.clock.tick(15)
        
    
    
    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                keys = pygame.key.get_pressed()
                self.print_text('Paused, press Enter to continue', 125, 300)
                if keys[pygame.K_RETURN]:
                    paused = False
    
    
    def check_collision(self):
        """for barrier in self.cactus_arr:
            if barrier.y <= self.dinosaur.rect.y + 30:
                #print("y", barrier.y, self.dinosaur.rect.y + 30)
                if barrier.x <= self.usr_x - 170:
                    #print(barrier.x, self.usr_x -170)
                    return True               
        return False"""
        #перевірка на jump
        for barrier in self.cactus_arr:
            if not self.make_jump:
                if barrier.x <= self.dinosaur.rect.x+40 <= barrier.x + barrier.width:
                    return True
            elif self.counter_jump == 10:
                if self.dinosaur.rect.y+self.usr_height-5 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x + self.usr_width -5 <= barrier.x + barrier.width:
                        return True
            elif self.counter_jump == 1:
                if self.dinosaur.rect.y + self.usr_height-5 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x + self.usr_width-35 <= barrier.x + 25:
                        return True
            else:
                if self.dinosaur.rect.y + self.usr_height-10 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x+5 <= barrier.x + barrier.width:
                        return True
        return False
    

    def game_over(self):
        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                keys = pygame.key.get_pressed()
                #self.print_text('Paused, press Enter to continue', 125, 300)
                if keys[pygame.K_RETURN]:
                    stopped = False
                    self.make_jump = False
                    self.cactus_arr = []
                    self.counter_jump = 30
                    self.usr_y = self.settings.screen_height-self.usr_height - 140
                    self.clouds = []
                    self.run_game()
                    return True
                if keys[pygame.K_ESCAPE]:
                    return False
                self.clouds = []
    
    
    def count_scores(self):
        if not self.above_cactus:
            for barrier in self.cactus_arr:
                if barrier.x <= self.dinosaur.rect.x + self.usr_width/2 <= barrier.x+barrier.width:
                    #print(barrier.x, self.usr_x, self.usr_width, barrier.x, barrier.width)
                    #print(self.dinosaur.rect.y, self.usr_height, barrier.y)
                    if self.dinosaur.rect.y + self.usr_height-5 <= barrier.y:
                        
                        self.above_cactus = True
                        break
        else:
            if self.counter_jump == -30:
                self.scores += 1
                self.above_cactus = False
                    
    




     
            

       
                

if __name__=='__main__':
    dino = DinoGame()
    dino.show_menu()
    