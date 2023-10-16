import pygame
import math
import sys

# For window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
FPS = 120

# For pendulum
PENDULUM_LENGTH = 200
GRAVITY = 9.81
AIR_RESISTANCE = 0.1

# Initializing window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pendul")

font = pygame.font.Font(None, 22)
mass = 0.4
max_angle = math.pi / 2
theta = math.pi / 4
theta_velocity = 0
pivot = (SCREEN_WIDTH // 2, 100)

clock = pygame.time.Clock()
dt = 0.02


class Slider:
    SLIDER_WIDTH, SLIDER_HEIGHT = 200, 10
    SLIDER_COLOR = (0, 0, 0)
    THUMB_WIDTH, THUMB_HEIGHT = 20, 20
    THUMB_COLOR = (120, 120, 120)
    slider_x = 0
    slider_y = 0
    thumb_x = 0
    thumb_y = 0
    thumb_position = 0

    def define_position(self, sx, sy):
        self.slider_x = sx
        self.slider_y = sy
        self.thumb_x = self.slider_x
        self.thumb_y = self.slider_y - (self.THUMB_HEIGHT - self.SLIDER_HEIGHT) // 2

    def define_length(self, length, h):
        self.SLIDER_WIDTH = length
        self.SLIDER_HEIGHT = h

    def draw_slider(self):
        pygame.draw.rect(screen, self.SLIDER_COLOR, (self.slider_x, self.slider_y, self.SLIDER_WIDTH, self.SLIDER_HEIGHT))
        pygame.draw.rect(screen, self.THUMB_COLOR, (self.thumb_x, self.thumb_y, self.THUMB_WIDTH, self.THUMB_HEIGHT))


# Mass Slider
slider1 = Slider()
slider1.define_length(200, 10)
slider1.define_position(20, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                x, y = event.pos
                slider1.thumb_x = min(max(x - slider1.THUMB_WIDTH // 2, slider1.slider_x),
                                      slider1.slider_x + slider1.SLIDER_WIDTH - slider1.THUMB_WIDTH)

    mass = slider1.thumb_x / 100

    inertia = mass * theta * theta
    theta_acceleration = -(GRAVITY / PENDULUM_LENGTH) * math.sin(theta)
    theta_velocity += (theta_acceleration - AIR_RESISTANCE * theta_velocity / mass) * dt
    theta += theta_velocity * dt * 100

    screen.fill(BACKGROUND_COLOR)

    pendulum_x = int(pivot[0] + PENDULUM_LENGTH * math.sin(theta))
    pendulum_y = int(pivot[1] + PENDULUM_LENGTH * math.cos(theta))
    pygame.draw.line(screen, (0, 0, 0), pivot, (pendulum_x, pendulum_y), 5)
    pygame.draw.circle(screen, (0, 0, 0), (pendulum_x, pendulum_y), 15)

    slider1.draw_slider()

    text = font.render(f"Masa: {mass:.2f}", True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (57, 20)

    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()