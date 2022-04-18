# source https://github.com/jakeoeding/connect-4
# modified by Shaif Salehin

import sys
import tkinter

import pygame as pg

import Connect4.board
clock = pg.time.Clock()

    
# Color constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


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

                pg.draw.rect(self.screen, BLUE, (left, top,
                                                 self.square_size, self.square_size))

                pg.draw.circle(
                    self.screen, BLACK, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pg.display.flip()

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
        pg.display.flip()

    def track_joy_motion(self, motion, current_color):
        # Moves next piece x position along the top of the pane as user moves mouse
        # Resets top of pane to black
        
        if abs(motion) < 0.1:
            motion = 0
   
        self.x_position += motion * 10
  
        if self.x_position < 50:
            self.x_position = 50
        if self.x_position > 1870:
            self.x_position = 1870
            
        pg.draw.rect(self.screen, BLACK,
                     (0, 0, self.width, self.square_size))
        pg.draw.circle(self.screen, current_color,
                       (self.x_position, self.circle_offset), self.radius)
        
        pg.display.flip()
        
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
    pane = Pane(6, 15, 128)
    pane.draw_background()
    continue_playing = True
    turn = 1
    current_color = RED
    
    
        
    # Begin gameplay
    while continue_playing:
       
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
                                continue_playing = False

                            elif pane.board.is_full():  # Check if there is a draw
                                continue_playing = False

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
                                continue_playing = False

                            elif pane.board.is_full():  # Check if there is a draw
                                continue_playing = False

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
        
                                     
        pg.display.flip()
        pg.time.Clock().tick(60)
