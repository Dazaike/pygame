import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game v31")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_strength = -10
on_ground = False
animation_counter = 0

# Load player images
try:
    idle_image = pygame.image.load('idle.png')
    run_images = [pygame.image.load('run1.png'), pygame.image.load('run2.png')]
    jump_image = pygame.image.load('jump.png')
    fall_image = pygame.image.load('fall.png')
except pygame.error as e:
    print(f"Error loading images: {e}")
    sys.exit()

# Scale images
idle_image = pygame.transform.scale(idle_image, (player_size, player_size))
run_images = [pygame.transform.scale(img, (player_size, player_size)) for img in run_images]
jump_image = pygame.transform.scale(jump_image, (player_size, player_size))
fall_image = pygame.transform.scale(fall_image, (player_size, player_size))

# Platform settings
platforms = [
    pygame.Rect(200, 500, 400, 20),
    pygame.Rect(100, 400, 200, 20),
    pygame.Rect(500, 300, 300, 20),
    pygame.Rect(50, 250, 150, 20),
    pygame.Rect(600, 150, 200, 20),
    pygame.Rect(300, 100, 200, 20),
]

# Load platform images
try:
    platform_image = pygame.image.load('platform.png')
except pygame.error as e:
    print(f"Error loading platform image: {e}")
    sys.exit()

# Scale platform images to fit platform dimensions
platform_images = [pygame.transform.scale(platform_image, (platform.width, platform.height)) for platform in platforms]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:  # Jump logic
        player_velocity_y = jump_strength
        on_ground = False

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Check for collisions with platforms
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y >= 0:
            player_y = platform.top - player_size
            player_velocity_y = 0
            on_ground = True

    # Check if player is on the ground (bottom of the screen)
    if player_y + player_size >= HEIGHT:
        player_y = HEIGHT - player_size
        player_velocity_y = 0
        on_ground = True

    # Fill the screen with white
    screen.fill(WHITE)

    # Determine player state and select the correct image
    if not on_ground:
        if player_velocity_y < 0:
            player_image = jump_image
        else:
            player_image = fall_image
    elif keys[pygame.K_a] or keys[pygame.K_d]:
        animation_counter += 1
        player_image = run_images[animation_counter // 10 % len(run_images)]
    else:
        player_image = idle_image

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Draw the platforms
    for platform, platform_img in zip(platforms, platform_images):
        screen.blit(platform_img, (platform.x, platform.y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
