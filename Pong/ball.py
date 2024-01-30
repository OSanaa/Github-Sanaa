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
        self.x = 20
        self.y = 20

    def ball_movement(self): 
        self.goto(self.xcor()+self.x,self.ycor()+self.y)

    def ball_hit_mid_paddle(self):
        print(self.heading())
        # if the ball angle is in between specified parameters, the ball will the opposite direction by 180 degrees from previous angle
        if (self.heading() <= 27.5) and (self.heading() >= 0) or (self.heading()>=315) and (self.heading<=360):
            # print("Angle: {}".format(self.angle))
            print("heading - 180 {}".format(abs(self.heading()-180)))
            self.setheading(abs(self.heading()-180))
        elif (self.heading() >= 152.5) and (self.heading() <= 207.5):
            print("In the going left if ")
            print("heading - 180: {}".format(abs(self.heading()-180)))
            self.setheading(abs(self.heading()-180))

    def ball_hit_top_paddle(self):
        self.setheading(abs((self.heading())-135))

    def ball_hit_border(self):
        # self.angle += 90
        print("Border Hit Function")
        # self.setheading(abs(self.heading()+90))
        # print(self.heading())
        # self.y = self.y - 10
        self.y = -abs(self.y)
        # self.goto(self.xcor(),self.ycor()-self.y)

    def ball_reset(self):
        '''
        Used to determine what angle and which player the ball will go towards at the start of
        each round
        '''
        self.goto(0,0)
        self.setheading(0)
        start_angle_range = random.choice([(0,35),(330,350),(145,215)])
        print(start_angle_range)
        self.angle = random.randint(start_angle_range[0],start_angle_range[1])
        # print(rand_angle)
        # self.right(self.angle) # remove comment once the paddle function is set
        self.right(0) # For testing 
        # print(self.right())
        self.tiltangle(90)

