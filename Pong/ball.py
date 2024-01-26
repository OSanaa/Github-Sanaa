from turtle import Turtle
import random

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

    def ball_reset(self):
        '''
        Used to determine what angle and which player the ball will go towards at the start of
        each round
        '''
        self.goto(0,0)
        self.setheading(0)
        start_angle_range = random.choice([(0,35),(330,350),(145,215)])
        print(start_angle_range)
        rand_angle = random.randint(start_angle_range[0],start_angle_range[1])
        print(rand_angle)
        self.right(rand_angle)
        # self.right(rand_angle)
        self.tiltangle(90)

