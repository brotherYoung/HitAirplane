import pygame


class MyBall(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.active = True

    def move(self):
        global score, score_surf, score_font
        self.rect = self.rect.move(self.speed)
        # bounce off the sides of the window
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed[0] = -self.speed[0]

            # bounce off the top of the window
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
            score = score + 1
            score_surf = score_font.render(str(score), 1, (0, 0, 0))


class MyPaddle(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([300, 20])
        image_surface.fill([0, 0, 0])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def add_balls(group, num):
    group.add(MyBall('wackyball.bmp', [10, 5], [150, 50]))
    group.add(MyBall('wackyball.bmp', [10, 7], [20, 50]))


pygame.init()
screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()
ball_group = pygame.sprite.Group()
lives = 4
add_balls(ball_group, lives)
paddle = MyPaddle([270, 400])

score = 0
score_font = pygame.font.Font(None, 50)
score_surf = score_font.render(str(score), 1, (0, 0, 0))
score_pos = [10, 10]
done = False

running = True
while running:
    clock.tick(30)
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            paddle.rect.centerx = event.pos[0]

    for ball in ball_group:
        ball.move()
        if not done:
            screen.blit(ball.image, ball.rect)
            screen.blit(paddle.image, paddle.rect)
            screen.blit(score_surf, score_pos)
            for i in range(lives - 1):
                width = screen.get_width()
                screen.blit(ball.image, [width - 40 * i, 20])
            pygame.display.flip()
        if ball.rect.top >= screen.get_rect().bottom:
            # lose a life if the ball hits the bottom
            lives = lives - 1
            print(lives)
            if lives == 0:
                final_text1 = "Game Over"
                final_text2 = "Your final score is:  " + str(score)
                ft1_font = pygame.font.Font(None, 70)
                ft1_surf = ft1_font.render(final_text1, 1, (0, 0, 0))
                ft2_font = pygame.font.Font(None, 50)
                ft2_surf = ft2_font.render(final_text2, 1, (0, 0, 0))
                screen.blit(ft1_surf, [screen.get_width() / 2 - \
                                       ft1_surf.get_width() / 2, 100])
                screen.blit(ft2_surf, [screen.get_width() / 2 - \
                                       ft2_surf.get_width() / 2, 200])
                pygame.display.flip()
                done = True
            else:  # wait 2 seconds, then start the next ball
                if lives > 1:
                    ball.rect.topleft = [50, 50]
                if lives == 1:
                    ball_group.remove(ball)
    balls_collide = pygame.sprite.spritecollide(paddle, ball_group, False)
    if balls_collide:
        for ball in balls_collide:
            ball.speed[1] = -ball.speed[1]

pygame.quit()
