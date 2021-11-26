import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 34)

LIMIT = pygame.Rect(WIDTH//2-5, 0, 5, HEIGHT)

Health_Font = pygame.font.SysFont('Rockwell', 20)
Winner_Font = pygame.font.SysFont('Rockwell', 80)
Spaceship_Width, Spaceship_Height = 45, 35
Fps = 60
Speed = 7
Bullet_Vel = 8
Max_Bullets = 5


Yellow_Hit = pygame.USEREVENT + 1
Red_Hit = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('image', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (Spaceship_Width, Spaceship_Height)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('image', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (Spaceship_Width, Spaceship_Height)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('image', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, LIMIT)

    red_health_text = Health_Font.render(
        "Health: " + str(red_health), 1, RED)
    yellow_health_text = Health_Font.render(
        "Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += Bullet_Vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Red_Hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= Bullet_Vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Yellow_Hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - Speed > 0:  # LEFT
        yellow.x -= Speed
    if keys_pressed[pygame.K_d] and yellow.x + Speed + yellow.width < LIMIT.x:  # RIGHT
        yellow.x += Speed
    if keys_pressed[pygame.K_w] and yellow.y - Speed > 0:  # UP
        yellow.y -= Speed
    if keys_pressed[pygame.K_s] and yellow.y + Speed + yellow.height < HEIGHT - 30:  # DOWN
        yellow.y += Speed


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - Speed > LIMIT.x + LIMIT.width:  # LEFT
        red.x -= Speed
    if keys_pressed[pygame.K_RIGHT] and red.x + Speed + red.width < WIDTH:  # RIGHT
        red.x += Speed
    if keys_pressed[pygame.K_UP] and red.y - Speed > 0:  # UP
        red.y -= Speed
    if keys_pressed[pygame.K_DOWN] and red.y + Speed + red.height < HEIGHT - 30:  # DOWN
        red.y += Speed


def draw_winner(winner_text,color):
    draw_text = Winner_Font.render(winner_text, 1, color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)


def main():
    red = pygame.Rect(700, 300, Spaceship_Width, Spaceship_Height)
    yellow = pygame.Rect(100, 300, Spaceship_Width, Spaceship_Height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(Fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < Max_Bullets:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < Max_Bullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == Red_Hit:
                red_health -= 1

            if event.type == Yellow_Hit:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            draw_winner(winner_text, YELLOW)
            break


        if yellow_health <= 0:
            winner_text = "Red Wins!"
            draw_winner(winner_text, RED)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
