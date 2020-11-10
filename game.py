import sys
import pygame

Screen_size = 640, 480
Brick_width = 60
Brick_height = 15
Paddle_width = 100
Paddle_height = 10
Ball_diameter = 16
Ball_radius = int(Ball_diameter / 2)

MAX_PADDLE_X = Screen_size[0] - Paddle_width
MAX_BALL_X = Screen_size[0] - Ball_diameter
MAX_BALL_Y = Screen_size[1] - Ball_diameter
PADDLE_Y = Screen_size[1] - Paddle_height - 10

Black = (0, 0, 0)
White = (255, 255, 255)
Grey = (102, 92, 94)
Brick_color = (155, 1, 39)

State_start = 0
State_playing = 1
State_won = 2
State_game_over = 3


class Brick:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(Screen_size)
        pygame.display.set_caption("Breakout game")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 20)
        else:
            self.font = None

        self.init_game()

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = State_start

        self.paddle = pygame.Rect(270, PADDLE_Y, Paddle_width, Paddle_height)
        self.ball = pygame.Rect(270, PADDLE_Y - Ball_diameter, Ball_diameter, Ball_diameter)

        self.ball_vel = [5, -5]

        self.create_bricks()

    def create_bricks(self):
        m = 35
        self.bricks = []
        for i in range(7):
            l = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(l, m, Brick_width, Brick_height))
                l += Brick_width + 10
            m += Brick_height + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, Brick_color, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == State_start:
            self.ball_vel = [5, -5]
            self.state = State_playing
        elif keys[pygame.K_RETURN] and (self.state == State_game_over or self.state == State_won):
            self.init_game()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 1
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = State_won

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - Ball_diameter
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = State_start
            else:
                self.state = State_game_over

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, White)
            self.screen.blit(font_surface, (205, 5))

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, White)
            x = (Screen_size[0] - size[0]) / 2
            y = (Screen_size[1] - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(Black)
            self.check_input()

            if self.state == State_playing:
                self.move_ball()
                self.handle_collisions()
            elif self.state == State_start:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO START THE GAME")
            elif self.state == State_game_over:
                self.show_message("GAME OVER!! PRESS ENTER TO PLAY AGAIN")
            elif self.state == State_won:
                self.show_message("YOU WON!! PRESS ENTER TO PLAY AGAIN")

            self.draw_bricks()

            pygame.draw.rect(self.screen, Grey, self.paddle)

            pygame.draw.circle(self.screen, White, (self.ball.left + Ball_radius, self.ball.top + Ball_radius), Ball_radius)

            self.show_stats()

            pygame.display.flip()


if __name__ == "__main__":
    Brick().run()
