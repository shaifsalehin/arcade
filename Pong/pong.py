# source https://www.101computing.net/pong-tutorial-using-pg-getting-started/
# modified by I'muniqe Hill and Shaif Salehin

import pygame as pg  # required pygame 2.0+
from pygame.locals import *
from Pong.paddle import Paddle
from Pong.ball import Ball

player1, player2 = 0, 0
    # define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

    
def display_winner():
    global player1, player2, WHITE, BLACK
    width = 1920
    height = 1080
    
        # Open new window
    size = (1920, 1020)
    screen = pg.display.set_mode(size, pg.FULLSCREEN)
    
    seconds = 0
    start_ticks = pg.time.get_ticks()
    font = pg.font.Font('Agave.ttf', 100)
    font2 = pg.font.Font('Agave.ttf', 200)
    gameover_text = font2.render("Game over", True, WHITE)

    p1_winner_text = font.render("Player 1 wins!", True, WHITE)
    p2_winner_text = font.render("Player 2 wins!", True, WHITE)
    draw_winner_text = font.render("It's a draw!", True, WHITE)

    gameover_rect = gameover_text.get_rect()
    p1_winner_rect = p1_winner_text.get_rect()
    p2_winner_rect = p2_winner_text.get_rect()
    draw_winner_rect = draw_winner_text.get_rect()

    gameover_rect = ((width // 2) - 400, (height // 2) - 250)
    p1_winner_rect = ((width // 2) - 300, (height // 2) + 200)
    p2_winner_rect = ((width // 2) - 300, (height // 2) + 200)
    draw_winner_rect = ((width // 2) - 300, (height // 2) + 200)
    
    while True:
        pg.display.update()
        seconds = (pg.time.get_ticks()-start_ticks) / 1000
        screen.fill(BLACK)
        screen.blit(gameover_text, gameover_rect)

    
        if player1 > player2:
            screen.blit(p1_winner_text, p1_winner_rect)
        elif player2 > player1:
            screen.blit(p2_winner_text, p2_winner_rect)
        else:
            screen.blit(draw_winner_text, draw_winner_rect)
    
        if seconds > 10.0:
            break

def play_pong():
    global player1, player2, WHITE, BLACK
    
 
    # initialize modules
    pg.init()
    pg.joystick.init()

    # define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Open new window
    size = (1920, 1020)
    screen = pg.display.set_mode(size, pg.FULLSCREEN)


    # create left paddle
    paddleleft = Paddle(WHITE, 50, 200)
    paddleleft.rect.x = 5
    paddleleft.rect.y = 490

    # create right paddle
    paddleright = Paddle(WHITE, 50, 200)
    paddleright.rect.x = 1850
    paddleright.rect.y = 490

    # create ball
    ball = Ball(WHITE, 200, 300, 50, 70)
    ball.rect.x = 345
    ball.rect.y = 195

    # initialize ball position
    ballmove = False

    all_sprites_list = pg.sprite.Group()

    # add objects to group
    all_sprites_list.add(paddleleft)
    all_sprites_list.add(paddleright)
    all_sprites_list.add(ball)

    # create joysticks
    joysticks = [pg.joystick.Joystick(i)
                 for i in range(pg.joystick.get_count())]


    # loop continues running until user exits the game
    running = True

    # clock will be used to control how fast the screen updates
    clock = pg.time.Clock()


    # array to store joystick axis and value
    left_motion = [0, 0]  # joystick 1 -> left paddle
    right_motion = [0, 0]  # joystick 2 -> right paddle

    while running:
        pg.event.pump()
        for event in pg.event.get():
            if event.type == JOYAXISMOTION:
                # event axis [-1, 1]
                if event.axis < 2:
                    if (event.instance_id == 0):  # joystick 1
                        left_motion[event.axis] = event.value
                    if (event.instance_id == 1):  # joystick 2
                        right_motion[event.axis] = event.value

            if event.type == JOYDEVICEREMOVED:
                print("Joystick device removed. Please check your joystick connection.")

            if event.type == pg.JOYAXISMOTION and ballmove == False:
                ballmove = True

        # move left paddle with joystick 1
        paddleleft.move(left_motion[1])

        # move right paddle with joystick 2
        paddleright.move(right_motion[1])

        # logic
        all_sprites_list.update()

        if ball.rect.x >= 1920:
            ball.velocity[1] = -ball.velocity[1]
            player1 += 1
        if ball.rect.x <= 0:
            player2 += 1
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y > 1020:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        if pg.sprite.collide_mask(ball, paddleleft) or \
                pg.sprite.collide_mask(ball, paddleright):
            ball.bounce()
        #draw background screen
        screen.fill(BLACK)
        # draw net
        pg.draw.line(screen, BLACK, [960, 0], [960, 1020], 5)
        # draw sprites all at once
        all_sprites_list.draw(screen)
        # draw score design
        font = pg.font.Font(None, 74)
    ##    text = font.render(str(player1), 1, WHITE)
    ##    screen.blit(text, (250, 10))
    ##    text = font.render(str(player2), 1, WHITE)
    ##    screen.blit(text, (420, 10))
    ##    text = font.render("Player 1's Serve", 1, WHITE)
    ##    screen.blit(text, (50, 50))
        # update screen with current drawings
        pg.display.update()
        # make 60 fps
        clock.tick(60)
        
        if player1 < player2 or player2 < player1:
            display_winner()
            player1, player2 = 0, 0
            running = False
    
