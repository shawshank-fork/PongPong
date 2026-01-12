import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle setup
paddle_width, paddle_height = 10, 100
left_paddle = pygame.Rect(20, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)

# Ball setup
ball = pygame.Rect(WIDTH//2 - 7, HEIGHT//2 - 7, 15, 15)
ball_speed_x = 50
ball_speed_y = 50

score_left = 0
score_right = 0
font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 8
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 8

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 8
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 8

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle Collision 
    if ball.colliderect(left_paddle):
        ball_speed_x = abs(ball_speed_x)  # ensure moves right
        ball_speed_y += (ball.centery - left_paddle.centery) * 0.3

    if ball.colliderect(right_paddle):
        ball_speed_x = -abs(ball_speed_x)  # ensure moves left
        ball_speed_y += (ball.centery - right_paddle.centery) * 0.3

    # Scoring 
    if ball.x < -20:
        score_right += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if ball.x > WIDTH + 20:
        score_left += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    screen.fill(BLACK)

    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, i, 4, 10))

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 50, 20))

    pygame.display.flip()
    clock.tick(60)

