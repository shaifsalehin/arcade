# source https://www.101computing.net/pong-tutorial-using-pg-getting-started/
# modified by I'muniqe Hill and Shaif Salehin

import pygame as pg  # required pygame 2.0+
from pygame.locals import *
from Pong.paddle import Paddle
from Pong.ball import Ball
from time import sleep
import random


player1, player2 = 0, 0
    # define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (146, 0, 0)
YELLOW = (255, 194, 10)
GREY = (128, 128, 128)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

# initialize modules
pg.init()
pg.joystick.init()
clock = pg.time.Clock()

size = (1920, 1080)
screen = pg.display.set_mode(size, pg.FULLSCREEN)

running = True


def display_winner():
    global player1, player2, running
    width = 1920
    height = 1080
    
    # Open new window
    size = (1920, 1080)
    
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
    p1_winner_rect = ((width // 2) - 300, (height // 2) + 70)
    p2_winner_rect = ((width // 2) - 300, (height // 2) + 70)
    draw_winner_rect = ((width // 2) - 300, (height // 2) + 70)
    
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
    screen.fill(BLACK)
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
                pg.draw.circle(screen, RED, star, 1)
            elif player2 > player1:
                pg.draw.circle(screen, YELLOW, star, 1)


        for star in star_field_medium:
            star[1] += 4
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(screen, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(screen, DARKGREY, star, 3)
                
        screen.blit(gameover_text, gameover_rect)

    
        if player1 > player2:
            screen.blit(p1_winner_text, p1_winner_rect)
        elif player2 > player1:
            screen.blit(p2_winner_text, p2_winner_rect)
        else:
            screen.blit(draw_winner_text, draw_winner_rect)
    
        if seconds > 3.0:
            #running = False
            break

def play_pong():
    global player1, player2, running
    
    start_ticks = pg.time.get_ticks()

    # create left paddle
    paddleleft = Paddle(RED, 50, 120) # color, width, length
    paddleleft.rect.x = 0
    paddleleft.rect.y = 490

    # create right paddle
    paddleright = Paddle(YELLOW, 50, 120) # color, width, length
    paddleright.rect.x = 1870
    paddleright.rect.y = 490

    # create ball
    ball = Ball(WHITE, 960, 490, 50, 100) # color, x pos, y pos, radius, speed
    ball.rect.x = 960
    ball.rect.y = 490

    # initialize ball position
    ballmove = False

    all_sprites_list = pg.sprite.Group()

    # add objects to group
    all_sprites_list.add(paddleleft)
    all_sprites_list.add(paddleright)
    all_sprites_list.add(ball)

    # loop continues running until user exits the game
    running = True

    # create joysticks
    joysticks = [pg.joystick.Joystick(i)
                 for i in range(pg.joystick.get_count())]

 
    # clock will be used to control how fast the screen updates
    clock = pg.time.Clock()

    # array to store joystick axis and value
    left_motion = [0, 0]  # joystick 1 -> left paddle
    right_motion = [0, 0]  # joystick 2 -> right paddle
    
    font = pg.font.Font("Assets//fonts//Agave.ttf", 50)
    
    instruction_text = font.render("Instructions: Best of 3. Game is over when a player wins twice.", True, GREY)
    instruction_rect = instruction_text.get_rect()
    instruction_rect = (280, 1020)
            
    score1_text = font.render(f"Player 1 score: {player1}", True, GREY)
    score1_rect = score1_text.get_rect()
    score1_rect = (280, 10)
            
    score2_text = font.render(f"Player 2 score: {player2}", True, GREY)
    score2_rect = score2_text.get_rect()
    score2_rect = (1250, 10)

    while running:
        pg.display.update()
        pg.event.pump()
        for event in pg.event.get():
            if event.type == JOYAXISMOTION:
                # event axis [-1, 1]
                if event.axis == 1 :
                    if (event.instance_id == 0):  # joystick 1
                        left_motion[0] = event.value
                        
                    if (event.instance_id == 1):  # joystick 2
                        right_motion[0] = event.value

            if event.type == JOYDEVICEREMOVED:
                print("Joystick device removed. Please check your joystick connection.")

        # move left paddle with joystick 1
        if abs(left_motion[0]) < 0.1:
            left_motion[0] = 0
        paddleleft.move(left_motion[0])
      
        # move right paddle with joystick 2
        if abs(right_motion[0]) < 0.1:
            right_motion[0] = 0
        paddleright.move(right_motion[0])

        # logic
        all_sprites_list.update()

        if ball.rect.x > 2000:
            player1 += 1
            play_pong()
            
        if ball.rect.x < -100:
            player2 += 1
            play_pong()
            
        if ball.rect.y >= 900:
            ball.velocity[1] = -ball.velocity[1]
            if ball.rect.y >= 1000:
                ball.rect.y = 600
            
        if ball.rect.y <= 100:
            ball.velocity[1] = -ball.velocity[1]
            if ball.rect.y <= 0:
                ball.rect.y = 400
                
        if ball.rect.x < (paddleright.rect.x-50) and pg.sprite.collide_mask(paddleright, ball):
            ball.bounce()
        
        if ball.rect.x > (paddleleft.rect.x-50) and pg.sprite.collide_mask(paddleleft, ball):
            ball.bounce()
        #draw background screen
        screen.fill(BLACK)
        screen.blit(instruction_text, instruction_rect)
        screen.blit(score1_text, score1_rect)
        screen.blit(score2_text, score2_rect)
        # draw sprites all at once
        all_sprites_list.draw(screen)
        # draw score design
        font = pg.font.Font(None, 74)
        
        # make 60 fps
        clock.tick(60)

        if player1 >= 2 or player2 >= 2:
            display_winner()
            player1, player2 = 0, 0
            screen.fill(BLACK)
            break
    running = False

    
