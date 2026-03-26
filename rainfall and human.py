import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

person_x = WIDTH // 2
ground_y = HEIGHT - 150

walk_offset = 0
direction = 1

rain = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(220)]

# splash memory (visible for few frames)
splashes = []

# -------- SKY --------
def draw_sky():
    for i in range(HEIGHT):
        color = (35, 55 + i//14, 85 + i//12)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

# -------- GRASS --------
def draw_grass():
    pygame.draw.rect(screen, (30, 120, 30), (0, ground_y, WIDTH, HEIGHT-ground_y))

# -------- DDA --------
def dda(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0: return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        screen.set_at((int(x), int(y)), color)
        x += x_inc
        y += y_inc

# -------- PERSON --------
def draw_person():
    global walk_offset
    facing = direction

    head_y = ground_y - 55
    neck_y = ground_y - 48

    pygame.draw.circle(screen, (255,255,255), (person_x, head_y), 8)

    pygame.draw.line(screen, (255,255,255),
                     (person_x, head_y + 8),
                     (person_x, neck_y), 3)

    pygame.draw.line(screen, (255,255,255),
                     (person_x, neck_y),
                     (person_x, ground_y), 3)

    leg_offset = math.sin(walk_offset) * 8

    pygame.draw.line(screen, (255,255,255),
                     (person_x, ground_y),
                     (person_x - 8*facing + leg_offset*facing, ground_y + 18), 3)

    pygame.draw.line(screen, (255,255,255),
                     (person_x, ground_y),
                     (person_x + 8*facing - leg_offset*facing, ground_y + 18), 3)

    hand_y = neck_y + 4
    hand_x = person_x + 12 * facing

    pygame.draw.line(screen, (255,255,255),
                     (person_x, hand_y),
                     (hand_x, hand_y - 8), 3)

    pygame.draw.line(screen, (255,255,255),
                     (person_x, hand_y),
                     (hand_x, hand_y + 4), 3)

# -------- UMBRELLA --------
def draw_umbrella():
    facing = direction
    cx = person_x + 12 * facing
    cy = ground_y - 75
    r = 45

    for y in range(r):
        width = int(math.sqrt(r*r - y*y))
        pygame.draw.line(screen, (220, 0, 0),
                         (cx - width, cy - y),
                         (cx + width, cy - y))

    pygame.draw.line(screen, (255,255,255),
                     (cx, cy),
                     (cx, ground_y - 40), 3)

# -------- COLLISION --------
def hits_umbrella(x, y):
    facing = direction
    cx = person_x + 12 * facing
    cy = ground_y - 75
    r = 45
    return (x-cx)**2 + (y-cy)**2 < r*r and y < cy

# -------- SPLASH --------
def add_splash(x, y):
    splashes.append([x, y, 0])

def draw_splashes():
    for s in splashes[:]:
        x, y, life = s

        pygame.draw.line(screen, (220,220,255), (x, y), (x, y-6), 2)
        pygame.draw.line(screen, (220,220,255), (x, y), (x-4, y-3), 2)
        pygame.draw.line(screen, (220,220,255), (x, y), (x+4, y-3), 2)

        s[2] += 1
        if s[2] > 3:
            splashes.remove(s)

# -------- LOOP --------
running = True
while running:
    draw_sky()
    draw_grass()

    person_x += 2 * direction
    if person_x > WIDTH - 50: direction = -1
    if person_x < 50: direction = 1

    walk_offset += 0.2

    draw_person()
    draw_umbrella()

    for drop in rain:
        x, y = drop

        # THICK RAIN
        dda(x, y, x+3, y+10, (210,210,255))
        dda(x+1, y, x+4, y+10, (180,180,255))
        dda(x-1, y, x+2, y+10, (160,160,255))

        drop[0] += 1
        drop[1] += 7

        if hits_umbrella(x, y):
            add_splash(x, y)
            drop[1] = random.randint(-50, 0)
            drop[0] = random.randint(0, WIDTH)

        elif y > ground_y:
            add_splash(x, ground_y)
            drop[1] = random.randint(-50, 0)
            drop[0] = random.randint(0, WIDTH)

        if drop[1] > HEIGHT:
            drop[1] = random.randint(-50, 0)
            drop[0] = random.randint(0, WIDTH)

    draw_splashes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
