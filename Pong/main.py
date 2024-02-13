"""
Gameplay: 
- First to 10
- The person who starts with the ball switches every round
- OPTIONAL:
    - Could have a play again option.
    - Could add a computer 
"""

from turtle import Screen
from paddle import Paddle
from ball import Ball
from border import Border
from score_board import ScoreBoard
import time


screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.tracer(0)

paddle_1 = Paddle(1)
paddle_2 = Paddle(2)
game_ball = Ball()
score_board = ScoreBoard()
border = Border()

screen.listen()
screen.onkeypress(key='w',fun=paddle_1.player_move_up)
screen.onkeypress(key='s',fun=paddle_1.player_move_down)

screen.onkeypress(key='Up',fun=paddle_2.player_move_up)
screen.onkeypress(key='Down',fun=paddle_2.player_move_down)

game_on = True

game_ball.ball_reset(game_ball.xcor())

'''
Game is on when game_on bool val is true
'''
while game_on:
    time.sleep(.09)
    game_ball.ball_movement()
    print(game_ball.ycor())

    ## Out of bounds
    if (game_ball.xcor() <= -400) or (game_ball.xcor() >= 400):
        score_board.update_score(game_ball.xcor())
        if (score_board.left_point == 1) or (score_board.right_point == 1):
            score_board.game_over()
            game_on = False
        else:
            game_ball.ball_reset(game_ball.xcor())
        
    ## If ball hits upper or lower bounderies
    if game_ball.ycor() >= 280:
        game_ball.ball_hit_y_border(True)

    ## If ball hits upper or lower bounderies
    if game_ball.ycor()<= -280:
        game_ball.ball_hit_y_border(False)

    if (game_ball.distance(paddle_1) < 35) or (game_ball.distance(paddle_2)<35) or (game_ball.distance(paddle_1.xcor(),paddle_1.ycor()+50) <35) or (game_ball.distance(paddle_2.xcor(),paddle_2.ycor()+50) <35) or (game_ball.distance(paddle_1.xcor(),paddle_1.ycor()-50) <35) or (game_ball.distance(paddle_2.xcor(),paddle_2.ycor()-50) <35):
        game_ball.ball_hit_paddle()

    screen.update()

screen.update()

screen.exitonclick()
