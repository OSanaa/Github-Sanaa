from turtle import Turtle

class Paddle(Turtle):

    def __init__(self,player_num):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=5)
        self.setheading(90)
        self.speed("fastest")
        self.penup()
        # self.player_num = player_num # Not sure if we need this but including it just in case
        self.player_position(player_num)
    
    def player_position(self,player_num):
        if player_num == 1:
            self.goto(-350,0)
        elif player_num == 2:
            self.goto(350,0)

    def player_move_up(self):
        # self.setheading(90)
        if self.ycor() < 225:
            self.forward(40)

    def player_move_down(self):
        if self.ycor() > -225:
            self.backward(40)







