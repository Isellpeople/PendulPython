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
pygame.display.set_caption("Simulare pendul")

font = pygame.font.Font(None, 22)
mass = 0.4
max_angle = math.pi / 2
theta = math.pi / 4
theta_velocity = 0
pivot = (SCREEN_WIDTH // 2, 150)

# For text box
input_text = ""
text_surface = font.render(input_text, True, TEXT_COLOR)
textbox_rect = text_surface.get_rect()
textbox_rect.center = (720, 570)

clock = pygame.time.Clock()
dt = 0.02


class Slider:
    slider_collision = 30
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
        pygame.draw.rect(screen, self.SLIDER_COLOR, (self.slider_x, self.slider_y, self.SLIDER_WIDTH,
                                                     self.SLIDER_HEIGHT))
        pygame.draw.rect(screen, self.THUMB_COLOR, (self.thumb_x, self.thumb_y, self.THUMB_WIDTH, self.THUMB_HEIGHT))


# Mass Slider
slider1 = Slider()
slider1.define_length(200, 10)
slider1.define_position(20, 40)

# Length slider
slider2 = Slider()
slider2.define_length(200, 10)
slider2.define_position(20, 100)
slider2.thumb_x = 100

running = True
dragging1 = False
dragging2 = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:  # Input for slider
            if dragging1:
                x, y = event.pos
                slider1.thumb_x = min(max(x - slider1.THUMB_WIDTH // 2, slider1.slider_x),
                                      slider1.slider_x + slider1.SLIDER_WIDTH - slider1.THUMB_WIDTH)
            if dragging2:
                x, y = event.pos
                slider2.thumb_x = min(max(x - slider2.THUMB_WIDTH // 2, slider2.slider_x),
                                      slider2.slider_x + slider2.SLIDER_WIDTH - slider2.THUMB_WIDTH)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            thumb_rect1 = pygame.Rect(slider1.thumb_x, slider1.thumb_y, slider1.THUMB_WIDTH, slider1.THUMB_HEIGHT)
            thumb_rect2 = pygame.Rect(slider2.thumb_x, slider2.thumb_y, slider2.THUMB_WIDTH, slider2.THUMB_HEIGHT)
            if thumb_rect1.collidepoint(x, y):
                dragging1 = True
            if thumb_rect2.collidepoint(x, y):
                dragging2 = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging1 = False
            dragging2 = False
        elif event.type == pygame.KEYDOWN:      # Input for text box
            if event.key == pygame.K_r:
                theta = math.pi / 4
            elif event.key == pygame.K_o:
                theta = 0.0
                theta_velocity = 0.0
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                theta = float(input_text) * (math.pi / 180)
                input_text = ""
            else:
                input_text += event.unicode

    mass = slider1.thumb_x / 100
    PENDULUM_LENGTH = slider2.thumb_x * 2

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
    slider2.draw_slider()

    text = font.render(f"Masa: {mass * 10:.2f} kg", True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (65, 20)

    text_surface = font.render(input_text, True, TEXT_COLOR)
    t = font.render("Unghi teta (grade) : ", True, TEXT_COLOR)
    t_rect = t.get_rect()
    t_rect.center = (650, 570)
    length_text = font.render(f"Lungime curenta : {PENDULUM_LENGTH:.2f}", True, TEXT_COLOR)
    lt_rect = length_text.get_rect()
    lt_rect.center = (110, 80)
    angle_text = font.render(f"Unghi curent : {theta:.2f} rad", True, TEXT_COLOR)
    at_rect = angle_text.get_rect()
    at_rect.center = (661, 550)
    tutorial_text1 = font.render("'r'  -> reseteaza la unghi de 45°", True, TEXT_COLOR)
    tt_rect1 = tutorial_text1.get_rect()
    tt_rect1.center = (117, 550)
    tutorial_text2 = font.render("'o' -> opreste miscarea", True, TEXT_COLOR)
    tt_rect2 = tutorial_text2.get_rect()
    tt_rect2.center = (84, 570)

    screen.blit(text, text_rect)
    screen.blit(text_surface, textbox_rect)
    screen.blit(t, t_rect)
    screen.blit(length_text, lt_rect)
    screen.blit(angle_text, at_rect)
    screen.blit(tutorial_text1, tt_rect1)
    screen.blit(tutorial_text2, tt_rect2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
