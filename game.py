import sys
import pygame
from random import randint
#setting the dimensions of screen,bricks,paddle,and the ball
Screen_size = 800, 600
Brick_width =65
Brick_height = 20
Paddle_width = 200
Paddle_height = 20
Ball_diameter = 25
Ball_radius = int(Ball_diameter / 2)

PADDLEX = Screen_size[0] - Paddle_width
BALLX = Screen_size[0] - Ball_diameter
BALLY = Screen_size[1] - Ball_diameter
PADDLEY = Screen_size[1] - Paddle_height - 10
#setting colors
Black = (0, 0, 0)
White = (255, 255, 255)
Blue=(11,7,116)
Grey = (102, 92, 94)
Red = (255,0,0)

#setting the states
start = 0
playing = 1
won = 2
game_over = 3


class Brick:

    def __init__(self):
        pygame.init()
        #initiallizing the size of the screen,the caption and its font
        self.screen = pygame.display.set_mode(Screen_size)
        pygame.display.set_caption("Breakout game")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.game()

    def game(self):
        self.lives = 3
        self.score = 0
        self.state = start
        #setting the position and dimensions of the paddle and the ball
        self.paddle = pygame.Rect(300, PADDLEY, Paddle_width, Paddle_height)
        self.ball = pygame.Rect(100, PADDLEY - Ball_diameter, Ball_diameter, Ball_diameter)
        #initiallizing the velocity of the ball
        self.ball_vel = [5, -5]

        self.bricks()

    def bricks(self): #creating the bricks(5 rows with 10 brick in each row)
        m = 60
        self.bricks = []
        for i in range(5):
            l = 35
            for j in range(10):
                self.bricks.append(pygame.Rect(l, m, Brick_width, Brick_height))
                l += Brick_width + 10
            m += Brick_height + 5

    def drawbricks(self): #setting the bricks on the screen with their color and shape
        for brick in self.bricks:
            pygame.draw.rect(self.screen, Blue, brick)

    def Event(self): #checking the event fired by the user depending on the pressed key(left key,right key,enter or space)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5
            if self.paddle.left > PADDLEX:
                self.paddle.left = PADDLEX

        if keys[pygame.K_SPACE] and self.state == start:
            self.ball_vel = [randint(5, 8),randint(5, 8)]
            self.state = playing
        elif keys[pygame.K_RETURN] and (self.state == game_over or self.state == won):
            self.init_game()

    def Ballmovement(self):   #controlling  the movement of the ball
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= BALLX:
            self.ball.left = BALLX
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= BALLY:
            self.ball.top = BALLY
            self.ball_vel[1] = -self.ball_vel[1]

    def Collision(self): #changing the score,lives and the state when the ball hits the brick
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 1 #if the ball hits the brick,increase the score by one and remove this brick
                self.ball_vel[1] = -self.ball_vel[1]
                
                pygame.draw.rect(self.screen, Red, brick)
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = won

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLEY - Ball_diameter
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:#if the ball hits the ground,decrease the lives by 1
            self.lives -= 1
            if self.lives > 0:
                self.state = start
            else:  #if lives=0 ,ends the game
                self.state = game_over

    def Stats(self):#showing the score and the lives on the screen
        pygame.draw.line(self.screen, White, [0, 30], [800, 30], 2)
        text = self.font.render("Score: " + str(self.score), 1, White)
        self.screen.blit(text, (20, 10))
        text = self.font.render("Lives: " + str(self.lives), 1, White)
        self.screen.blit(text, (700, 10))

    def message(self, message):#determine the position and the color of the showed message
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, White)
            x = (Screen_size[0] - size[0]) / 2
            y = (Screen_size[1] - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#if the user press quit,exit the game
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(Grey) #background of the screen
            self.Event()

            #determine which message to be appeared according to the state of the gaem
            if self.state == playing:
                self.Ballmovement()
                self.Collision()
            elif self.state == start:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.message("PRESS SPACE TO START THE GAME")
            elif self.state == game_over:
                self.message("GAME OVER!! PRESS ENTER TO PLAY AGAIN")
                text2 = self.font.render('your score is '+str(self.score),1, White )
                self.screen.blit(text2, (350, 250))

            elif self.state == won:
                self.message("YOU WON!! PRESS ENTER TO PLAY AGAIN")
                text2 = self.font.render('your score is ' + str(self.score), 1, White)
                self.screen.blit(text2, (350, 250))
            self.drawbricks()
            #display the paddle and the ball on the screen
            pygame.draw.rect(self.screen, Black, self.paddle)

            pygame.draw.circle(self.screen, White, (self.ball.left + Ball_radius, self.ball.top + Ball_radius), Ball_radius)

            self.Stats()

            pygame.display.flip()


if __name__ == "__main__":
    Brick().run()
