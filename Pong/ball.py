from turtle import Turtle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=.9, stretch_wid=.9)
        # self.setheading(90)
        # self.speed("") # If we need to adjust the ball speed
        self.penup()