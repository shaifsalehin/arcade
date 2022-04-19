# source https://python-forum.io/thread-336.html
# modified by Shaif Salehin

import sys
import RPi.GPIO as GPIO
import pygame as pg
from time import sleep
from pygame.locals import *
from pynput.keyboard import Key, Controller
from Pong.pong import play_pong
from Connect4.connect4 import play_connect4
from Trivia.trivia import play_trivia
pg.init()
pg.display.init()

pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

keyboard = Controller()

counter_pin = 37 #pin 37 in BOARD mode = GPIO26 in BCM mode

GPIO.setmode( GPIO.BOARD ) #change pin to 26 if using BCM mode
GPIO.setup( counter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(counter_pin, GPIO.RISING, bouncetime=100)

class Main:
    def __init__(self):
        self.done = False
        self.fps = 60
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.flip()


class SceneManager:
    def __init__(self):
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255, 255, 0)
        self.deselected_color = (255, 255, 255)

    def draw_scene(self, screen):
        '''handle drawing of the menu options'''
        for i, opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx,
                             self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])

    def update_scene(self):

        self.change_selected_option()

    def get_event_menu(self, event):
   
        if event.type == pg.KEYDOWN:
            '''select new index'''
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)

            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
                
        if event.type == JOYBUTTONDOWN or event.type == JOYBUTTONUP:
            self.select_option(self.selected_index)
        self.mouse_menu_click(event)

    def mouse_menu_click(self, event):
        '''select menu option '''
      
        if (event.type == MOUSEBUTTONDOWN and event.button == 1):
            
            for i, opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break

    def pre_render_options(self):
        '''setup render menu options based on selected or deselected'''
        font_deselect = pg.font.Font("Assets//fonts//RetroGaming.ttf", 50)
        font_selected = pg.font.Font("Assets//fonts//RetroGaming.ttf", 75)

        rendered_msg = {"des": [], "sel": []}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, self.deselected_color)
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, self.selected_color)
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend, d_rect))
            rendered_msg["sel"].append((s_rend, s_rect))
        self.rendered = rendered_msg

    def select_option(self, i):
        '''select menu option via keys or mouse'''
        if i == len(self.next_list):
            self.quit = True
        else:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, op=0):
        '''change highlighted menu option'''
        for i, opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i
        if op:
            self.selected_index += op
            max_ind = len(self.rendered['des'])-1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0


class States(Main):
    def __init__(self):
        Main.__init__(self)
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None


class Insert_Coin(States, SceneManager):

    def __init__(self):
        States.__init__(self)
        SceneManager.__init__(self)
        self.next = 'game_select'
        self.options = ['']
        self.next_list = ['']
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75

    def cleanup(self):
        print('cleaning up Main Menu state stuff')

    def startup(self):
        pass

    def get_event(self, event):
#         coin_detected = GPIO.event_detected(counter_pin)
#         while (coin_detected == True):
#             self.done = True
#             self.get_event_menu(event)
# 
#             break
            
        self.done = True
        self.get_event_menu(event)
    def update(self, screen, dt):

        self.update_scene()
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_scene(screen)


class Game_Select(States, SceneManager):
    def __init__(self):
        States.__init__(self)
        SceneManager.__init__(self)
        self.next = 'game_select'
        self.options = ['PONG', 'CONNECT 4', 'TRIVIA']
        self.next_list = ['pong', 'connect4', 'trivia']
        self.pre_render_options()
        self.from_bottom = 500
        self.spacer = 100

    def cleanup(self):
        print('cleaning up Options state stuff')

    def startup(self):
        print('starting Options state stuff')

    def get_event(self, event):
        
        if event.type == JOYAXISMOTION:
            if (event.axis == 1 and 0.8 <= event.value <= 1.2):
                self.change_selected_option(-1)
            if (event.axis == 1 and -0.8 >= event.value >= -1.2):
                self.change_selected_option(1)
        
        self.get_event_menu(event)

    def update(self, screen, dt):
        self.update_scene()
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_scene(screen)


class Pong(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'insert_coin'

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')
        play_pong()

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.play(screen)

    def play(self, screen):
        self.done = True


class Connect4(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'insert_coin'

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')
        play_connect4()

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.play(screen)

    def play(self, screen):
        self.done = True


class Trivia(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'insert_coin'

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')
        play_trivia()
        

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.play(screen)

    def play(self, screen):
        self.done = True
        
app = Main()
state_dict = {
    'insert_coin': Insert_Coin(),
    'game_select': Game_Select(),
    'pong': Pong(),
    'connect4': Connect4(),
    'trivia': Trivia()


}
app.setup_states(state_dict, 'insert_coin')
app.main_game_loop()
pg.quit()
sys.exit()

