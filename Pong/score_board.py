from turtle import Turtle

class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.borders = self.create_border()

    def create_border(self):
        border_list = []
        border_y = 290
        for i in range(15):
            borders = Turtle("square")
            borders.color("white")
            borders.shapesize(stretch_len=0.9, stretch_wid=0.9)
            borders.penup()

            borders.setposition(0,border_y)
            border_y-=40
            border_list.append(borders)

        return(border_list)

