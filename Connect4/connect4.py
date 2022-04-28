# source https://github.com/jakeoeding/connect-4
# modified by Shaif Salehin

import sys
import tkinter
import random
import pygame as pg

import Connect4.board
clock = pg.time.Clock()


# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (12, 123, 220)
RED = (146, 0, 0)
YELLOW = (255, 194, 10)
GREEN = (26, 255, 26)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

width = 1920
height = 1080


class Pane:
    
    def __init__(self, row_count, column_count, square_size):
        self.board = Connect4.board.Board(row_count, column_count)
        self.square_size = square_size
        self.radius = square_size // 2 - 5
        self.width = column_count * square_size
        # Additional row for next piece at top
        self.height = (row_count + 1) * square_size
        self.row_offset = square_size  # Used to account for additional row at top
        # Used to center circle inside each grid square
        self.circle_offset = square_size // 2
        self.screen = pg.display.set_mode(
            (self.width, self.height), pg.FULLSCREEN)
        
        self.p1motion=[0,0]
        self.p2motion=[0,0]
        self.x_position = 0
    def draw_background(self):
        # Draws a grid of blue rectangles with black circles superimposed at the center of each rectangle
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.row_offset

                pg.draw.rect(self.screen, DARKGREY, (left, top,
                                                 self.square_size, self.square_size))

                pg.draw.circle(
                    self.screen, BLACK, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pg.display.update()

    def fill_in_pieces(self):
        # Fills each spot on the board with the color of the piece at said spot
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                if self.board.grid[r, c] == 1:
                    current_color = RED
                elif self.board.grid[r, c] == 2:
                    current_color = YELLOW
                else:
                    current_color = BLACK
                x_position = c * self.square_size + self.circle_offset
                # Invert because pieces need to come from bottom up
                y_position = self.height - \
                    (r * self.square_size + self.circle_offset)
                pg.draw.circle(self.screen, current_color,
                               (x_position, y_position), self.radius)
        pg.display.update()

    def track_joy_motion(self, motion, current_color):
        # Moves next piece x position along the top of the pane as user moves mouse
        # Resets top of pane to black
        
        if abs(motion) < 0.1:
            motion = 0

        self.x_position += motion * 3
  
        if self.x_position < 50:
            self.x_position = 50
        if self.x_position > 1870:
            self.x_position = 1870
            
        pg.draw.rect(self.screen, BLACK,
                     (0, 0, self.width, self.square_size))
        pg.draw.circle(self.screen, current_color,
                       (self.x_position, self.circle_offset), self.radius)
        
        pg.display.update()
        
    def try_drop_piece(self, turn):
        # Converts user's mouse position into a column selection
        # Fills said column if column isn't full
        # Returns whether or not operation was completed
        column_selection = int(self.x_position) // self.square_size
        if self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False

    def reset(self):
        # Prepares the Pane for another game
        self.screen = pg.display.set_mode(
            (self.width, self.height), pg.FULLSCREEN)  # Gives pg focus again
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def display_winner(p1, p2, draw):

    #screen = pg.display.set_mode(
            #(width, height), pg.FULLSCREEN)
    pane = Pane(6, 15, 128)
    seconds = 0
    start_ticks = pg.time.get_ticks()
    font = pg.font.Font("Assets//fonts//Agave.ttf", 100)
    font2 = pg.font.Font("Assets//fonts//Agave.ttf", 200)
    gameover_text = font2.render("Game over", True, WHITE)
    p1_winner_text = font.render("Player 1 wins!", True, RED)
    p2_winner_text = font.render("Player 2 wins!", True, YELLOW)
    draw_winner_text = font.render("It's a draw!", True, WHITE)

    gameover_rect = gameover_text.get_rect()
    p1_winner_rect = p1_winner_text.get_rect()
    p2_winner_rect = p2_winner_text.get_rect()
    draw_winner_rect = draw_winner_text.get_rect()

    gameover_rect = ((width // 2) - 400, (height // 2) - 250)
    p1_winner_rect = ((width // 2) - 330, (height // 2) - 50)
    p2_winner_rect = ((width // 2) - 330, (height // 2) - 50)
    draw_winner_rect = ((width // 2) - 330, (height // 2) - 50)
    
    star_field_slow = []
    star_field_medium = []
    star_field_fast = []

    for slow_stars in range(50): 
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_slow.append([star_loc_x, star_loc_y])

    for medium_stars in range(35):
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_medium.append([star_loc_x, star_loc_y])

    for fast_stars in range(15):
        star_loc_x = random.randrange(0, width)
        star_loc_y = random.randrange(0, height)
        star_field_fast.append([star_loc_x, star_loc_y])

    while True:
        pg.display.update()

        #set frames per second
        clock.tick(60)
        seconds = (pg.time.get_ticks()-start_ticks) / 1000
        
        for star in star_field_slow:
            star[1] += 1
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
                            
            if player1 > player2:
                pg.draw.circle(pane.screen, RED, star, 1)
            elif player2 > player1:
                pg.draw.circle(pane.screen, YELLOW, star, 1)


        for star in star_field_medium:
            star[1] += 4
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(pane.screen, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(pane.screen, DARKGREY, star, 3)
        
        pane.screen.blit(gameover_text, gameover_rect)

        if p1 > p2:
            pane.screen.blit(p1_winner_text, p1_winner_rect)
        elif p2 > p1:
            pane.screen.blit(p2_winner_text, p2_winner_rect)
        else:
            pane.screen.blit(draw_winner_text, draw_winner_rect)

        if seconds > 5.0:
            break
    #running = False

def play_connect4():
    # Setup game
    # Hide tkinter main application window, only using messagebox
    tkinter.Tk().wm_withdraw()
    pg.init()
    pg.display.init()
    pg.joystick.init()
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    for joystick in joysticks:
        print(joystick.get_name())
    font1 = pg.font.Font("Assets//fonts//Agave.ttf", 35)

    pane = Pane(6, 15, 128)
    pane.draw_background()
    running = True
    turn = 1
    current_color = RED
    
    # Begin gameplay
    while running:
        pg.display.update()
        instruction_text = font1.render("Instructions: Move left and right with joystick. Game alternates turns between player 1 and player 2.", True, WHITE)
        instruction_rect = instruction_text.get_rect()
        instruction_rect = (50, height - (height- 920))
        pane.screen.blit(instruction_text, instruction_rect)
        
        help_text_text = font1.render("Player 1 turn          Press    to drop                Player 2 turn", True, WHITE)
        help_text_rect = instruction_text.get_rect()
        help_text_rect = (350, height - (height- 985))
        pane.screen.blit(help_text_text, help_text_rect)
        
        pg.draw.circle(pane.screen, RED, (300,
                                              height - (height-1000)), 30, width=0)
        pg.draw.circle(pane.screen, YELLOW, ((width // 2) + 330,
                                                 height - (height-1000)), 30, width=0)
        pg.draw.circle(pane.screen, BLUE, ((width // 2) - 70,
                                               height - (height-1000)), 30, width=0)
        for event in pg.event.get(pump=True):
            
            if event.type == pg.JOYAXISMOTION: 
                if event.axis == 0:

                    if (event.instance_id == 0):
                        pane.p1motion[0] = event.value

                    elif (event.instance_id == 1):
                        pane.p2motion[0] = event.value
                
                if current_color == RED:
                    pane.track_joy_motion(pane.p1motion[0], current_color)
                elif current_color == YELLOW:
                    pane.track_joy_motion(pane.p2motion[0], current_color)


            elif event.type == pg.JOYBUTTONDOWN:
                if current_color == RED:
                    if (event.instance_id == 0 and event.button == 1):      
                        if pane.try_drop_piece(turn):
                            pane.fill_in_pieces()
                            # Check if the current player won
                            if pane.board.has_four_in_a_row(turn):
                                pane.screen.fill(BLACK)
                                display_winner(1, 0, 0)
                                running = False

                            elif pane.board.is_full():  # Check if there is a draw
                                pane.screen.fill(BLACK)
                                display_winner(0, 0, 1)
                                running = False

                            else:  # Prepare next turn
                                # Alternate turn between 1 and 2 after each valid selection
                                turn = 1 if turn == 2 else 2
                                # Player 1 color is red, player 2 is yellow
                                current_color = RED if turn == 1 else YELLOW
                                # Switch the next piece color
                                if event.type == pg.JOYAXISMOTION:
                                    if event.axis == 0:

                                        if (event.instance_id == 0):
                                            pane.p1motion[0] = event.value

                                        elif (event.instance_id == 1):
                                            pane.p2motion[0] = event.value
                                    if current_color == RED:
                                        pane.track_joy_motion(pane.p1motion[0], current_color)
                                    elif current_color == YELLOW:
                                        pane.track_joy_motion(pane.p2motion[0], current_color)
                                        
                elif current_color == YELLOW:
                    if (event.instance_id == 1 and event.button == 1):      
                        if pane.try_drop_piece(turn):
                            pane.fill_in_pieces()

                            # Check if the current player won
                            if pane.board.has_four_in_a_row(turn):
                                pane.screen.fill(BLACK)
                                display_winner(0, 1, 0)
                                running = False

                            elif pane.board.is_full():  # Check if there is a draw
                                pane.screen.fill(BLACK)
                                display_winner(0, 0, 1)
                                running = False

                            else:  # Prepare next turn
                                # Alternate turn between 1 and 2 after each valid selection
                                turn = 1 if turn == 2 else 2
                                # Player 1 color is red, player 2 is yellow
                                current_color = RED if turn == 1 else YELLOW
                                # Switch the next piece color
                                if event.type == pg.JOYAXISMOTION:
                                    if event.axis == 0:

                                        if (event.instance_id == 0):
                                            pane.p1motion[0] = event.value
                                        elif (event.instance_id == 1):
                                            pane.p2motion[0] = event.value
                                            
                                    if current_color == RED:
                                        pane.track_joy_motion(pane.p1motion[0], current_color)
                                    elif current_color == YELLOW:
                                        pane.track_joy_motion(pane.p2motion[0], current_color)
        
                                     
        
        pg.time.Clock().tick(60)
