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
    def __init__(self, canvas):
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
    def __init__(self, canvas):
        x =random.randint(0, SCREENWIDTH/GRID-1)*GRID
        y = random.randint(0, SCREENHIGHT/GRID-1)*GRID
        self.canvas = canvas
        self.coords = [x,y]
        self.circle = canvas.create_oval(x,y,x+GRID,y+GRID, 
                                         fill=FOODCOLOR, tag="food")
    def eaten(self):
        self.canvas.delete(self.circle)
        x =random.randint(0, SCREENWIDTH/GRID-1)*GRID
        y = random.randint(0, SCREENHIGHT/GRID-1)*GRID
        self.coords = [x,y]
        self.circle = self.canvas.create_oval(x,y,x+GRID,y+GRID, 
                                         fill=FOODCOLOR, tag="food") 
        
class Game(tk.Tk):
    def __init__(self, master = None):
        tk.Tk.__init__(self, master)
        self.direction = 'right' #Starting direction
        self.username = tk.StringVar()
        self.username.set(USERNAME)
        self.add_widgets()
        
        self.grid()
        

        
    def add_widgets(self):
        self.usernameEntry = tk.Entry(self, textvariable=self.username)
        self.usernameEntry.pack()

        
        self.startButton = tk.Button(
            self, text="Start", command=lambda: [
                self.destroy_startscreen(), self.create_game_screen()])
        self.startButton.pack()
        
        self.quitButton = tk.Button(
            self, text="Quit", command=self.destroy)
        self.quitButton.pack()
        
        self.highscoreLabel = tk.Label(self, text="")
        self.highscoreLabel.pack()
        
        self.highscoreButton = tk.Button(
            self, text="Highscore", command=self.show_highscore)
        self.highscoreButton.pack()
        
    def destroy_startscreen(self):
        self.usernameEntry.pack_forget()
        self.startButton.destroy()
        self.quitButton.destroy()
        self.highscoreButton.destroy()
        self.highscoreLabel.destroy()

    def create_game_screen(self):
        # Create screen
        self.canvas = tk.Canvas(self, bg=BACKGROUND, width=SCREENWIDTH, height=SCREENHIGHT)
        self.canvas.pack()
        
        self.instructions = self.canvas.create_text(
            SCREENWIDTH/2, SCREENHIGHT/2+GRID, text = "Press <space> to start", fill = "#FFFFFF")

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.bind_all("<Key>", self.keybinds) 
        

    def keybinds(self, keypress):
        
        if keypress.keycode == 37 and self.direction != "right":
            self.direction = "left"
        if keypress.keycode == 38 and self.direction != "down":
            self.direction = "up"
        if keypress.keycode == 39 and self.direction != "left":
            self.direction = "right"
        if keypress.keycode == 40 and self.direction != "up":
            self.direction = "down"   
        if keypress.keycode == 32:
            self.canvas.delete(self.instructions)
            while True:
                try: 
                    self.next_move(self.snake, self.food)
                except:  
                    break
             
    def next_move(self, snake, food):
        x,y = snake.coords[0]
        
        # Dictionary of directions   
        directions = {'up':[0,-GRID], 'down':[0,GRID], 'left':[-GRID,0], 'right':[GRID,0]}
        
        newx = x + directions[self.direction][0]
        newy = y + directions[self.direction][1]
        
        snake.coords.insert(0, [newx, newy])
        x, y = snake.coords[0]
        square = self.canvas.create_rectangle(x, y, x+GRID, y+GRID, 
                                         fill=SNAKECOLOR, tag="snake")
        snake.squares.insert(0, square)
        
        
        # If snake head is not at food, snake does not grow
        if food.coords != snake.coords[0]:    
            snake.coords.pop(-1)
            self.canvas.delete(snake.squares[-1])
            snake.squares.pop(-1)
            
        else:
            food.eaten()
            snake.score += 1
        
        # If snake leaves screen you die
        if x < 0 or x > SCREENWIDTH-GRID or y < 0 or y > SCREENHIGHT-GRID:
            print('You crashed into the wall!')
            
            print("GAME OVER")
            
            self.set_score(self.username.get(), snake.score)
            self.canvas.destroy()
            self.add_widgets()
            
        # If head touches body you die
        if snake.coords[0] in snake.coords[1:]:
            print('You bit yourself!')
            print("GAME OVER")
            self.set_score(self.username.get(), snake.score)
            self.canvas.destroy()
            self.add_widgets()
        
        time.sleep(SPEED)
        self.canvas.update()
    
    def set_score(self, username, score):
        scoreboard = open("snake_score.txt", "a")
        scoreboard.write(f'{username}: {score} \n')
        scoreboard.close()
        
    def get_highscore(self):
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
    
    def show_highscore(self):
        scoreholder, highscore = self.get_highscore()
        self.highscoreLabel.config(text = "The best player is " + scoreholder +
                                   " with " + str(highscore) + "points!")
        

game = Game()


game.mainloop()
