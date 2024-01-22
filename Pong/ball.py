from turtle import Turtle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=.9, stretch_wid=.9)
        self.speed("slowest") # If we need to adjust the ball speed
        self.penup()

    def ball_movement(self):
        self.forward(20)

    def ball_hit(self):
        if self.heading() == 0:
            self.setheading(180)
        elif self.heading() == 180:
            self.setheading(0)