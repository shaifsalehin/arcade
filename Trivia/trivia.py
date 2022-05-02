# created by Shaif Salehin
import Trivia.get_data
import pygame as pg
from pygame.locals import *
from Trivia.bar import Bar
import textwrap
import time
import random

pg.init()

pg.joystick.init()
joysticks = [pg.joystick.Joystick(i)
             for i in range(pg.joystick.get_count())]


number_of_questions = 10

WHITE = (255, 255, 255)
GREEN = (36, 255, 36)
BLUE = (12, 123, 220)
RED = (146, 0, 0)
YELLOW = (255, 194, 10)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

width = 1920
height = 1080
surface = pg.display.set_mode((width, height), pg.FULLSCREEN)
running = True
choices = []
category, difficulty, question, answer = "", "", "", ""
player1, player2 = 0, 0
p1_answer, p2_answer = 5, 5

lock1, lock2 = False, False

clock = pg.time.Clock()

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

def retrieve_data(question_num):
    global category, difficulty, question, answer, choices
    category, difficulty, question, answer = Trivia.get_data.get_trivia_data(
        question_num)
    choices = Trivia.get_data.get_choices()
    question = textwrap.wrap(question)


def event_checker():
    global p1_answer, p2_answer, lock1, lock2
    for event in pg.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.instance_id == 0 and not lock1:
                p1_answer = event.button
                lock1 = True
            if event.instance_id == 1 and not lock2:
                p2_answer = event.button
                lock2 = True


def are_ya_winning_son():
    global p1_answer, p2_answer, player1, player2
    if p1_answer != 5:
        if p1_answer < 4:
            if choices[p1_answer] == answer:
                player1 += 10
    if p2_answer != 5:
        if p2_answer < 4:
            if choices[p2_answer] == answer:
                player2 += 10


def display_winner():
    
    seconds = 0
    start_ticks = pg.time.get_ticks()
    font = pg.font.Font("Assets//fonts//Agave.ttf", 100)
    font2 = pg.font.Font("Assets//fonts//Agave.ttf", 200)
    gameover_text = font2.render("Game over", True, WHITE)
    player1_text = font.render("Player 1", True, WHITE)
    player2_text = font.render("Player 2", True, WHITE)
    score1_text = font.render("Score: " + str(player1), True, WHITE)
    score2_text = font.render("Score: " + str(player2), True, WHITE)
    p1_winner_text = font.render("Player 1 wins!", True, RED)
    p2_winner_text = font.render("Player 2 wins!", True, YELLOW)
    draw_winner_text = font.render("It's a draw!", True, WHITE)

    gameover_rect = gameover_text.get_rect()
    player1_rect = player1_text.get_rect()
    player2_rect = player2_text.get_rect()
    score1_rect = score1_text.get_rect()
    score2_rect = score2_text.get_rect()
    p1_winner_rect = p1_winner_text.get_rect()
    p2_winner_rect = p2_winner_text.get_rect()
    draw_winner_rect = draw_winner_text.get_rect()

    gameover_rect = ((width // 2) - 400, (height // 2) - 250)
    player1_rect = ((width // 2) - 600, (height // 2) - 75)
    player2_rect = ((width // 2) + 200, (height // 2) - 75)
    score1_rect = ((width // 2) - 600, (height // 2) + 50)
    score2_rect = ((width // 2) + 200, (height // 2) + 50)
    p1_winner_rect = ((width // 2) - 300, (height // 2) + 200)
    p2_winner_rect = ((width // 2) - 300, (height // 2) + 200)
    draw_winner_rect = ((width // 2) - 300, (height // 2) + 200)

    
    surface.fill(BLACK)
    
    while True:
        surface.fill(BLACK)
        seconds = (pg.time.get_ticks()-start_ticks) / 1000
        
        for star in star_field_slow:
            star[1] += 1
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
                            
            if player1 > player2:
                pg.draw.circle(surface, RED, star, 3)
            elif player2 > player1:
                pg.draw.circle(surface, YELLOW, star, 3)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(surface, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pg.draw.circle(surface, DARKGREY, star, 3)
    
     
        surface.blit(gameover_text, gameover_rect)
        surface.blit(player1_text, player1_rect)
        surface.blit(player2_text, player2_rect)
        surface.blit(score1_text, score1_rect)
        surface.blit(score2_text, score2_rect)

        if player1 > player2:
            surface.blit(p1_winner_text, p1_winner_rect)
        elif player2 > player1:
            surface.blit(p2_winner_text, p2_winner_rect)
        else:
            surface.blit(draw_winner_text, draw_winner_rect)
                    
        clock.tick(60)
        pg.display.update()
        
        if seconds > 5.0:
            break


def play_trivia():
    global player1, player2, p1_answer, p2_answer, lock1, lock2, running
    running = True
    question_count = 0 
      
    while running:
        for i in range(number_of_questions):
            bar = Bar(surface)
            lock1, lock2 = False, False
            p1_answer, p2_answer = 5, 5
            question_count += 1
            pg.event.clear()
            pg.event.set_allowed(JOYBUTTONDOWN)
            retrieve_data(i)
            font = pg.font.Font("Assets//fonts//Agave.ttf", 50)
            font1 = pg.font.Font("Assets//fonts//Agave.ttf", 30)
            category_text = font.render("Category: " + category, True, GREY)
            difficulty_text = font.render(
                "Difficulty: " + difficulty.title(), True, GREY)
            if len(question) == 1:
                question_text1 = font.render(question[0], True, WHITE)
            elif len(question) == 2:
                question_text1 = font.render(question[0], True, WHITE)
                question_text2 = font.render(question[1], True, WHITE)
            elif len(question) == 3:
                question_text1 = font.render(question[0], True, WHITE)
                question_text2 = font.render(question[1], True, WHITE)
                question_text3 = font.render(question[2], True, WHITE)
            elif len(question) == 4:
                question_text1 = font.render(question[0], True, WHITE)
                question_text2 = font.render(question[1], True, WHITE)
                question_text3 = font.render(question[2], True, WHITE)
                question_text4 = font.render(question[3], True, WHITE)
    
            answer0_text = font.render(choices[0], True, WHITE)
            answer1_text = font.render(choices[1], True, WHITE)
            answer2_text = font.render(choices[2], True, WHITE)
            answer3_text = font.render(choices[3], True, WHITE)
    
            category_rect = category_text.get_rect()
            difficulty_rect = difficulty_text.get_rect()
            if len(question) == 1:
                question_rect1 = question_text1.get_rect()
            elif len(question) == 2:
                question_rect1 = question_text1.get_rect()
                question_rect2 = question_text2.get_rect()
            elif len(question) == 3:
                question_rect1 = question_text1.get_rect()
                question_rect2 = question_text2.get_rect()
                question_rect3 = question_text3.get_rect()
            elif len(question) == 4:
                question_rect1 = question_text1.get_rect()
                question_rect2 = question_text2.get_rect()
                question_rect3 = question_text3.get_rect()
                question_rect4 = question_text4.get_rect()
    
            answer0_rect = answer1_text.get_rect()
            answer1_rect = answer1_text.get_rect()
            answer2_rect = answer1_text.get_rect()
            answer3_rect = answer1_text.get_rect()
    
            category_rect = ((width // 2) - 900, height - (height-100))
            difficulty_rect = ((width // 2) + 460, height - (height-100))
            question_rect1 = ((width // 2) - 900, height - (height-300))
            question_rect2 = ((width // 2) - 900, height - (height-350))
            question_rect3 = ((width // 2) - 900, height - (height-400))
            question_rect4 = ((width // 2) - 900, height - (height-450))
            answer0_rect = ((width // 2) - 860, height - (height-560))
            answer1_rect = ((width // 2) - 860, height - (height-660))
            answer2_rect = ((width // 2) - 860, height - (height-760))
            answer3_rect = ((width // 2) - 860, height - (height-860))
            
            question_number_text = font.render(f"Question: {question_count} of {number_of_questions}", True, GREY)
            question_number_rect = question_number_text.get_rect()
            question_number_rect = ((width // 2) - 220, height - (height-200))
            
            instruction1_text = font1.render("Instructions: This is a 2 player game. You each have 10 seconds to press the button color of your choice.", True, GREY)
            instruction1_rect = instruction1_text.get_rect()
            instruction1_rect = (30, height - (height- 950))
            
            instruction2_text = font1.render("Next question will appear after timer runs out and answer is revealed.", True, GREY)
            instruction2_rect = instruction2_text.get_rect()
            instruction2_rect = (280, height - (height- 990))
            
            score_text = font.render(f"Player 1 score:  {player1}                                 Player 2 score: {player2}", True, GREY)
            score_rect = question_number_text.get_rect()
            score_rect = ((width // 2) - 900, height - (height-200))
        
            start_ticks = pg.time.get_ticks()
            while True:
                counter = 0
                surface.fill(BLACK)
                surface.blit(score_text, score_rect)
                surface.blit(question_number_text, question_number_rect)
                surface.blit(answer0_text, answer0_rect)
                surface.blit(instruction1_text, instruction1_rect)
                surface.blit(instruction2_text, instruction2_rect)
                surface.blit(category_text, category_rect)
                surface.blit(difficulty_text, difficulty_rect)
                surface.blit(question_text1, question_rect1)
                if len(question) == 2:
                    surface.blit(question_text2, question_rect2)
                if len(question) == 3:
                    surface.blit(question_text2, question_rect2)
                    surface.blit(question_text3, question_rect3)
                if len(question) == 4:
                    surface.blit(question_text2, question_rect2)
                    surface.blit(question_text3, question_rect3)
                    surface.blit(question_text4, question_rect4)
    
                surface.blit(answer0_text, answer0_rect)
                surface.blit(answer1_text, answer1_rect)
                surface.blit(answer2_text, answer2_rect)
                surface.blit(answer3_text, answer3_rect)
    
                pg.draw.circle(surface, YELLOW, ((width // 2) - 900,
                                                 height - (height-580)), 30, width=0)
                pg.draw.circle(surface, BLUE, ((width // 2) - 900,
                                               height - (height-680)), 30, width=0)
                pg.draw.circle(surface, RED, ((width // 2) - 900,
                                              height - (height-780)), 30, width=0)
                pg.draw.circle(surface, GREEN, ((width // 2) - 900,
                                                height - (height-880)), 30, width=0)
    
                event_checker()
            
                seconds = (pg.time.get_ticks()-start_ticks) / \
                    1000  # calculate how many seconds
                
                # ~ timer_text = font.render(str(int(seconds)), True, WHITE)
                # ~ timer_rect = instruction1_text.get_rect()
                # ~ timer_rect = ((width // 2 + 500), height - (height- 930))
                seconds_in_total = seconds
                if 0 <= seconds <= 10:
                    piece_of_the_bar = ((2582 / (10) / bar.smoothness_of_bar))
                    bar.draw(add_value=piece_of_the_bar)
                if counter % bar.smoothness_of_bar == 0 and seconds_in_total > 0:
                    seconds_in_total -= 1

                # If the smoothnes of bar == 1, the program waits 1 second,
                # and the bar go second per second:
                time.sleep(1/bar.smoothness_of_bar)

                counter += 1
                #surface.blit(timer_text, timer_rect)
                
                if seconds > 10:  # if more than 10 seconds
                    pg.event.set_blocked(JOYBUTTONDOWN)
                    if choices[0] == answer:
                        answer1_text = font.render(choices[1], True, BLACK)
                        answer2_text = font.render(choices[2], True, BLACK)
                        answer3_text = font.render(choices[3], True, BLACK)
                        answer1_rect = answer1_text.get_rect()
                        answer2_rect = answer2_text.get_rect()
                        answer3_rect = answer3_text.get_rect()
                        answer1_rect = ((width // 2) - 900, height - (height-660))
                        answer2_rect = ((width // 2) - 900, height - (height-760))
                        answer3_rect = ((width // 2) - 900, height - (height-860))
                        surface.blit(answer1_text, answer1_rect)
                        surface.blit(answer2_text, answer2_rect)
                        surface.blit(answer3_text, answer3_rect)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-680)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-780)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-880)), 30, width=0)
    
                    elif choices[1] == answer:
                        answer0_text = font.render(choices[0], True, BLACK)
                        answer2_text = font.render(choices[2], True, BLACK)
                        answer3_text = font.render(choices[3], True, BLACK)
                        answer0_rect = answer0_text.get_rect()
                        answer2_rect = answer2_text.get_rect()
                        answer3_rect = answer3_text.get_rect()
                        answer0_rect = ((width // 2) - 860, height - (height-560))
                        answer2_rect = ((width // 2) - 860, height - (height-760))
                        answer3_rect = ((width // 2) - 860, height - (height-860))
                        surface.blit(answer0_text, answer0_rect)
                        surface.blit(answer2_text, answer2_rect)
                        surface.blit(answer3_text, answer3_rect)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-580)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-780)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-880)), 30, width=0)
    
                    elif choices[2] == answer:
                        answer0_text = font.render(choices[0], True, BLACK)
                        answer1_text = font.render(choices[1], True, BLACK)
                        answer3_text = font.render(choices[3], True, BLACK)
                        answer0_rect = answer0_text.get_rect()
                        answer1_rect = answer1_text.get_rect()
                        answer3_rect = answer3_text.get_rect()
                        answer0_rect = ((width // 2) - 860, height - (height-560))
                        answer1_rect = ((width // 2) - 860, height - (height-660))
                        answer3_rect = ((width // 2) - 860, height - (height-860))
                        surface.blit(answer0_text, answer0_rect)
                        surface.blit(answer1_text, answer1_rect)
                        surface.blit(answer3_text, answer3_rect)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-580)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-680)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-880)), 30, width=0)
    
                    elif choices[3] == answer:
                        answer0_text = font.render(choices[0], True, BLACK)
                        answer1_text = font.render(choices[1], True, BLACK)
                        answer2_text = font.render(choices[2], True, BLACK)
                        answer0_rect = answer0_text.get_rect()
                        answer1_rect = answer1_text.get_rect()
                        answer2_rect = answer2_text.get_rect()
                        answer0_rect = ((width // 2) - 860, height - (height-560))
                        answer1_rect = ((width // 2) - 860, height - (height-660))
                        answer2_rect = ((width // 2) - 860, height - (height-760))
                        surface.blit(answer0_text, answer0_rect)
                        surface.blit(answer1_text, answer1_rect)
                        surface.blit(answer2_text, answer2_rect)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-580)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-680)), 30, width=0)
                        pg.draw.circle(
                            surface, BLACK, ((width // 2) - 900, height - (height-780)), 30, width=0)
                
                if seconds > 12:
                    break
                
                # Draws the surface object to the screen.
                pg.display.flip()
            are_ya_winning_son()
        display_winner()
        player1, player2 = 0, 0
        p1_answer, p2_answer = 5, 5
        pg.event.set_allowed(JOYBUTTONDOWN)
        running = False
    
#def play_trivia():
    #setup()


#play_trivia()
