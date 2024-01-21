import pygame, sys


# Initialize pygame and screen
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
favicon = pygame.image.load("favicon.png")
pygame.display.set_icon(favicon)
pygame.display.set_caption("Atari Pong")

# load game font and sounds
font = pygame.font.Font("font/Atari_Classic.ttf", 20)
ball_hit_sound = pygame.mixer.Sound("sounds/ball_hit.mp3")
score_sound = pygame.mixer.Sound("sounds/score.mp3")

# Game colors
navy_blue = (0, 30, 130)
yellow = (250, 255, 15)
green = (80, 170, 65)

# Initialize cpu, player, ball and score
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)
ball_speed_x = 6
ball_speed_y = 6

cpu = pygame.Rect(0, 0, 20, 100)
cpu.centery = screen_height / 2
cpu_speed = 6

player = pygame.Rect(0, 0, 20, 100)
player.midright = (screen_width, screen_height / 2)
player_speed = 0

cpu_score = 0
player_score = 0


# Move the ball
def move_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        ball_speed_x *= -1
        score("cpu")

    if ball.left <= 0:
        ball_speed_x *= -1
        score("player")

    # Check collision
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1
        ball_hit_sound.play()


# Move the player
def move_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height


# Move the cpu
def move_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -6

    if ball.centery >= cpu.centery:
        cpu_speed = 6

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height


# Add score
def score(winner):
    global cpu_score, player_score

    if winner == "cpu":
        cpu_score += 1
        score_sound.play()

    if winner == "player":
        player_score += 1
        score_sound.play()


# Main game loop
while True:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    # Change the game objects position
    move_ball()
    move_player()
    move_cpu()

    # Draw the game objects
    pygame.draw.ellipse(screen, green, ball)
    pygame.draw.rect(screen, yellow, cpu)
    pygame.draw.rect(screen, yellow, player)
    pygame.draw.aaline(
        screen, "white", (screen_width / 2, 0), (screen_width / 2, screen_height)
    )

    # Update the scores
    cpu_score_surface = font.render("CPU: " + str(cpu_score), False, yellow)
    player_score_surface = font.render("PLAYER: " + str(player_score), False, yellow)

    screen.blit(cpu_score_surface, (screen_width / 6, 20))
    screen.blit(player_score_surface, ((screen_width / 3) * 2, 20))

    # Update the display
    pygame.display.update()
    screen.fill(navy_blue)
    clock.tick(60)
