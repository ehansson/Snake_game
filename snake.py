# -*- coding: utf-8 -*-
"""
Snake
"""
import tkinter as tk
import random
import time

#DEFAULT VARIABLES
SCREENWIDTH = 700
SCREENHIGHT = 500
BACKGROUND = 'black'
GRID = 20
STARTLENGTH = 2
STARTX = (SCREENWIDTH-GRID)/2
STARTY = (SCREENHIGHT-GRID)/2
SNAKECOLOR = "#FFFFFF"
FOODCOLOR = "#FF0000"
SPEED = 0.1
USERNAME = "Dangernoodle"


class Snake():
    def __init__(self):
        self.bodylength = STARTLENGTH
        self.coords = []
        self.squares = []
        self.score = 0
        
        for l in range(self.bodylength-1, -1, -1):
            self.coords.append([STARTX+GRID*l  , STARTY])
        
        for x,y in self.coords:
            square = canvas.create_rectangle(x, y, x+GRID, y+GRID, 
                                             fill=SNAKECOLOR, tag="snake")
            self.squares.insert(0, square)



        
class Food():
    def __init__(self):
        x =random.randint(0, SCREENWIDTH/GRID-1)*GRID
        y = random.randint(0, SCREENHIGHT/GRID-1)*GRID
        self.coords = [x,y]
        self.circle = canvas.create_oval(x,y,x+GRID,y+GRID, 
                                         fill=FOODCOLOR, tag="food")
    def eaten(self):
        canvas.delete(self.circle)
        x =random.randint(0, SCREENWIDTH/GRID-1)*GRID
        y = random.randint(0, SCREENHIGHT/GRID-1)*GRID
        self.coords = [x,y]
        self.circle = canvas.create_oval(x,y,x+GRID,y+GRID, 
                                         fill=FOODCOLOR, tag="food")


def keybinds(keypress):
    global direction
    if keypress.keycode == 37 and direction != "right":
        direction = "left"
    if keypress.keycode == 38 and direction != "down":
        direction = "up"
    if keypress.keycode == 39 and direction != "left":
        direction = "right"
    if keypress.keycode == 40 and direction != "up":
        direction = "down"   
    if keypress.keycode == 32:
        canvas.delete(instructions)
        while True:
            try: 
                next_move(snake, food)
            except:  
                break
         
def next_move(snake, food):
    x,y = snake.coords[0]
    
    newx = x + directions[direction][0]
    newy = y + directions[direction][1]
    
    snake.coords.insert(0, [newx, newy])
    x, y = snake.coords[0]
    square = canvas.create_rectangle(x, y, x+GRID, y+GRID, 
                                     fill=SNAKECOLOR, tag="snake")
    snake.squares.insert(0, square)
    
    
    # If snake head is not at food, snake does not grow
    if food.coords != snake.coords[0]:    
        snake.coords.pop(-1)
        canvas.delete(snake.squares[-1])
        snake.squares.pop(-1)
        
    else:
        food.eaten()
        snake.score += 1
    
    # If snake leaves screen you die
    if x < 0 or x > SCREENWIDTH-GRID or y < 0 or y > SCREENHIGHT-GRID:
        print('You crashed into the wall!')
        print("GAME OVER")
        set_score(USERNAME, snake.score)
        screen.destroy()
        
    # If head touches body you die
    if snake.coords[0] in snake.coords[1:]:
        print('You bit yourself!')
        print("GAME OVER")
        set_score(USERNAME, snake.score)
        screen.destroy()
    
    time.sleep(SPEED)
    canvas.update()

def set_score(username, score):
    scoreboard = open("snake_score.txt", "a")
    scoreboard.write(f'{USERNAME}: {score} \n')
    scoreboard.close()
    
def get_highscore():
    scoreboard = open("snake_score.txt", "r")
    lines = scoreboard.readlines()
    highscore = 0
    scoreholder = "Nobody"
    for line in lines:
        name, score = line.split(": ")
        score = int(score)
        if score > highscore:
            highscore = score
            scoreholder = name
    return scoreholder, highscore
    


# Dictionary of directions   
directions = {'up':[0,-GRID], 'down':[0,GRID], 'left':[-GRID,0], 'right':[GRID,0]}
direction = 'right' #Starting direction

# Create screen
screen = tk.Tk()
canvas = tk.Canvas(screen, bg=BACKGROUND, width=SCREENWIDTH, height=SCREENHIGHT)
canvas.pack()

snake = Snake()
food = Food()
screen.bind("<Key>", keybinds)
instructions = canvas.create_text(SCREENWIDTH/2, SCREENHIGHT/2+GRID, 
                   text = "Press <space> to start", fill = "#FFFFFF")
screen.mainloop()

winner, highscore = get_highscore()
print(f'The best player is {winner} with {highscore} points!')
