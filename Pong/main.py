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

screen.listen()
screen.onkeypress(key='w',fun=paddle_1.player_move_up)
screen.onkeypress(key='s',fun=paddle_1.player_move_down)

screen.onkeypress(key='Up',fun=paddle_2.player_move_up)
screen.onkeypress(key='Down',fun=paddle_2.player_move_down)

game_on = True
game_ball.ball_start()
while game_on:
    time.sleep(.05)
    
    game_ball.ball_movement()

    # print(paddle_2.pos())
    # for i in range(-40,40):
    if (game_ball.distance(paddle_1) <15) or (game_ball.distance(paddle_2)<15) or (game_ball.distance(paddle_1.xcor(),paddle_1.ycor()+40) <15) or (game_ball.distance(paddle_1.xcor(),paddle_1.ycor()-40) <15) or (game_ball.distance(paddle_2.xcor(),paddle_2.ycor()+40) <15) or (game_ball.distance(paddle_2.xcor(),paddle_2.ycor()-40) <15):
        game_ball.ball_hit()

    screen.update()

screen.update()

screen.exitonclick()
