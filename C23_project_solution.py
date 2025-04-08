import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
cannonball_visible = False  # Initially hidden

# Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Load Images
cannon_image = pygame.image.load('canon.png')
cannon_ball_image = pygame.image.load('cannon_ball.png')
background_image = pygame.image.load('bg4.jpg')
brick_image = pygame.image.load('bricks.png')
# Resize Images
background_image = pygame.transform.scale(background_image, (800, 600))
cannon_ball_image = pygame.transform.scale(cannon_ball_image, (50, 50))
cannon_image = pygame.transform.scale(cannon_image, (200, 200))
brick_image = pygame.transform.scale(brick_image, (60, 60))

ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 1
space.add(ground_body, ground_shape)

# Create Cannonball (Initially Hidden)
cannonball_body = None
cannonball_shape = None

# Create Cannon
def create_cannon(x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    space.add(body, shape)
    return body, shape

cannon_body, cannon_shape = create_cannon(10, 500)


# Function to create a new cannonball when clicked
def create_cannonball(x, y):
    global cannonball_body, cannonball_shape, cannonball_visible

    # Remove existing ball from space if any
    if cannonball_body:
        space.remove(cannonball_body, cannonball_shape)

    # Create a new ball
    cannonball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    cannonball_body.position = x, y
    cannonball_shape = pymunk.Circle(cannonball_body, 20)
    cannonball_shape.elasticity = 0.2
    cannonball_shape.friction = 0.2
    cannonball_shape.collision_type = 1  # Collision type for cannonball
    space.add(cannonball_body, cannonball_shape)

    cannonball_visible = True  # Make ball visible
# Create Block
def create_block(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (60, 60)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    shape.elasticity = 0.4
    shape.friction = 0.6
    shape.collision_type = 2
    space.add(body, shape)
    return body, shape

# Create stacked blocks (fixed positions)
blocks = [
    create_block(540, 520), create_block(600, 520), create_block(660, 520),create_block(720, 520),create_block(780, 520),
    create_block(600, 460), create_block(660, 460), create_block(720, 460),
    create_block(630, 400), create_block(690, 400),
    create_block(660, 340)
]
# Draw function
def draw_objects():
    global game_over, game_won
    screen.blit(background_image, (0, 0))

    # Draw Cannonball only if it's visible
    if cannonball_visible and cannonball_body:
        ball_pos = cannonball_body.position
        screen.blit(cannon_ball_image, (ball_pos.x - 25, ball_pos.y - 25))

    # Draw Cannon
    cannon_pos = cannon_body.position
    screen.blit(cannon_image, (cannon_pos.x - 20, cannon_pos.y - 20))

     # Blocks
    for body, shape in blocks:
        pos = body.position
        angle = body.angle * (180 / 3.14159)
        rotated = pygame.transform.rotate(brick_image, angle)
        rect = rotated.get_rect(center=(pos.x, pos.y))
        if pos.x > 800:
          blocks.remove((body, shape))
          space.remove(body, shape)
        else:
            screen.blit(rotated, rect.topleft)

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Allow launching only if game is not over and not won
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Create and launch cannonball
            create_cannonball(150, 500)
            cannonball_body.velocity = ((mouse_pos[0] - 150) * 4, (mouse_pos[1] - 500) * 4)
           

    
    space.step(1 / 60.0)
    draw_objects()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
