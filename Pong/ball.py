from turtle import Turtle
import random

class Ball(Turtle):
    """
    Class used to create the game ball

    ...

    Attributes
    ----------

    shape : Turtle
        used to determine shape of the game ball
    color : Turtle
        determines the color of the game ball
    shapesize : Turtle
        determines the size of the game ball
    speed : Turtle
        determines speed of game ball
    penup : Turtle
        makes sure lines aren't being drawn when the ball Turtle object moves
    x : int
        x coordinate in which the ball will move (x speed)
    y : int
        y coordinate in which ball will move (y speed)
    direction : bool
        bool val used to determine what paddle the ball hits

    Methods
    -------
    ball_movement()
        Controls the balls movement by adding the x and y attribute to the Turtle
        xcor() and ycor() attribute

    ball_hit_paddle()
        Changes the direction of the ball from left to right by using the direction
        attribute by changing the x value to a positibe or negative number using 
        the abs() function

    ball_hit_y_border(value)
        Bounces the ball to the opposite direction if the y border is hit

    ball_reset(boundary_side)
        Used to determine what angle and which player the ball will go towards at the start of
        each round
    """

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=.9, stretch_wid=.9)
        self.speed("slowest") # If we need to adjust the ball speed
        self.penup()
        self.x = 20
        self.y = 20
        self.direction = True # True = Going Right, False = Going Left

    def ball_movement(self): 
        self.goto(self.xcor()+self.x,self.ycor()+self.y)

    def ball_hit_paddle(self):
        if self.direction == True:
            self.x = -abs(self.x)
            self.direction = False
        else:
            self.x = abs(self.x)
            self.direction = True

    def ball_hit_y_border(self,value):
        print("Border Hit Function")
        if value == False:
            self.y = abs(self.y)
        else:
            self.y = -abs(self.y)

    def ball_reset(self,boundary_side):
        '''
        Used to determine what angle and which player the ball will go towards at the start of
        each round
        '''

        self.goto(0,0)
        self.setheading(0)
        if boundary_side == 400:
            self.x = -abs(self.x)
        elif boundary_side == -400:
            self.x = abs(self.x)
