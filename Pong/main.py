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

while game_on:
    screen.update()

# screen.listen()

screen.update()

screen.exitonclick()
