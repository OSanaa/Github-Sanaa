from turtle import Turtle

class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        # self.scores = self.score_table()
        self.right_score = self.create_score()
        self.left_score = self.create_score()
        self.left_point = 0
        self.right_point = 0
        self.set_score()
        
    def create_score(self):
        point = Turtle()
        point.penup()
        point.hideturtle()
        point.color("white")
        return(point)

    def set_score(self):
        self.left_score.setposition(-200,170)
        self.left_score.write("{}".format(self.left_point),font=('Arial',50,'normal'))
        self.right_score.setposition(200,170)
        self.right_score.write("{}".format(self.right_point),font=('Arial',50,'normal'))
    
    def update_score(self,ball_side):
        if ball_side == 400:
            print("In Update Score")
            self.left_point+=1
            self.left_score.clear()
            self.set_score()
        elif ball_side == -400:
            print("In Update Score")
            self.right_point+=1
            self.right_score.clear()
            self.clear()
            self.set_score()

    def game_over(self):
        if self.left_point == 1:
            self.left_score.setposition(-300,0)
            self.left_score.write("Player 1 Wins",font=('Arial',20,"normal"))
        elif self.right_point == 1:
            self.left_score.setposition(300,0)
            self.left_score.write("Player 2 Wins",font=('Arial',20,"normal"))




    


