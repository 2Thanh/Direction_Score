from pickle import TRUE
import pygame
import numpy
from numpy.linalg import inv
import math

pygame.init()
class button:
    def __init__(self,text,coordinate,width,height):
        self.coordinate = coordinate
        self.width = width
        self.height = height
        font = pygame.font.SysFont('sans', 40)
        self.font_text = font.render(str(text),True,WHITE)
        
    def draw_rect(self):
        pygame.draw.rect(screen,BLACK,(self.coordinate[0],self.coordinate[1],self.width,self.height))
        screen.blit(self.font_text,(self.coordinate[0]+5,self.coordinate[1]+5))

    def check_click(self):
        mouse = pygame.mouse.get_pos()
        if (self.coordinate[0] < mouse[0]< self.coordinate[0]+self.width and self.coordinate[1] < mouse[1] < self.coordinate[1] + self.height):
            return True
        else:
            return False

WIDTH = 1200
HEIGHT = 600
GRAY = (214,214,214)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)
BLUE = (0,0,200)

screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Direction Score")
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont('sans',20)

def distance(p1,p2):
    return math.sqrt(math.pow(p1[0]-p2[0],2) + math.pow(p1[1]-p2[1],2))
def coordinate_axis():
    #Draw OY (score band 10)
    score_txt = font.render("Score",True,RED)
    screen.blit(score_txt,(85,20))
    hours_per_week = font.render("Hour / Week",True,RED)
    screen.blit(hours_per_week,(850,545))
    pygame.draw.line(screen,GREEN,(100,50),(100,550),2)
    pygame.draw.polygon(screen , GREEN , points = [(95,50),(100,45),(105,50)])
    for i in range(int(450/45)):
        pygame.draw.line(screen,GREEN, (95,50 + 50*i),(105, 50 + 50*i),2)
        score_text = font.render(str(9-i),True,BLACK)
        screen.blit(score_text,(50,87 + 50*i))

    #Draw OX (time study)
    pygame.draw.line(screen,BLUE,(100,550),(820,550),2)
    pygame.draw.polygon(screen , BLUE , points = [(820,545),(825,550),(820,555)])
    for i in range(int(600/25)+1):
        pygame.draw.line(screen,BLUE, (100 + 30*i,545),(100 + 30*i ,555),2)
        time_study_text = font.render(str(i),True,BLACK)
        screen.blit(time_study_text,(94 + 30*i,555))


def greates_line(points):
    x = len(points)
    a = numpy.zeros([x,2], dtype = float)
    y = numpy.zeros([x,1], dtype = float)

    #add value to a matrix
    for j in range(x):
        for i in range (2):
            a[j][1] = 1
            a[j][0] = points[j][0]
    
    #add value to y
    for i in range(x):
        y[i] = points[i][1]
    C = inv(numpy.matmul((a.transpose()),a)) #inverse of (aT *a)^-1
    #print(numpy.matmul((a.transpose()),a))
    result = numpy.matmul(numpy.matmul(C,a.transpose()),y)
    return result
#a = numpy.matrix([[1, 2], [3, 4]])
#print(a.I)
start_btn = button("START",(840,400),140,50)
reset_btn = button("RESET",(1000,400),140,50)
btns = [start_btn,reset_btn]
points = []
points_2 = []
x = [0,0]
a= 0
run_draw = False
while running:
    screen.fill(GRAY)
    clock.tick(60) #60 Fps
    coordinate_axis()
    mouse = pygame.mouse.get_pos()
    
    font_board = pygame.font.SysFont('sans',30)
    if ( 95 < mouse[0] < 825 and 95 - 50 < mouse[1] < 555):
        hour_band =round((mouse[0] - 100)/30,1)
        score_band = round((- mouse[1] + 550)/50,1)
    else:
        hour_band = 0
        score_band = 0
    hour = font_board.render( "HOURS: " + str(hour_band) ,True,RED)
    score = font_board.render( "SCORE: " + str(score_band) ,True,RED)

    screen.blit(hour,(1000,150))
    screen.blit(score,(1000,250))

    
    #mouse coordinate
    if ( 95 < mouse[0] < 825 and 95 - 50 < mouse[1] < 555):
        font = pygame.font.SysFont('sans',15)
        #Draw coordinate
        mouse_text = font.render("("+ str(round((mouse[0] - 100)/30,1)) + "," + str(round((- mouse[1] + 550)/50,1)) + ")" ,True , YELLOW)
        pygame.draw.line(screen,BLACK,mouse,(mouse[0],mouse[1]+ distance((mouse[0],mouse[1]), (mouse[0],550))))
        pygame.draw.line(screen,BLACK,mouse,(mouse[0] - distance(mouse,(100,mouse[1])),mouse[1]))
        screen.blit(mouse_text,(mouse[0]+20,mouse[1]+20))
    for i in range(len(btns)):
        btns[i].draw_rect()
    for events in pygame.event.get():
        if(events.type == pygame.QUIT):
            running = False
        if(events.type == pygame.MOUSEBUTTONDOWN):
            if( start_btn.check_click()):
                print("start button")
            if ( reset_btn.check_click()):
                points = []
                points_2 = []
                run_draw = False
            if ( 95 < mouse[0] < 825 and 95 - 50 < mouse[1] < 555):
                point = round(round(mouse[0] - 100)/30,1),round((- mouse[1] + 550)/50,1)
                points.append(point)
                points_2.append(mouse)
                run_draw = False
                
            if (start_btn.check_click()):
                if(len(points_2) > 1): 
                    x = greates_line(points_2)
                    run_draw = True
                #print(type(x[0][0]))
    for i in range(len(points)):
        pygame.draw.circle(screen,ORANGE,(points[i][0]*30 + 100,-points[i][1]*50 + 550),6)

    if ((x[1] != 0 or x[0]!=0 )and len(points_2)!=0 and run_draw):
        pygame.draw.line(screen,RED,(10 , 10*x[0][0] + x[1][0]),(900,900*x[0][0]+x[1][0]),2)
    pygame.display.flip()
pygame.quit()


