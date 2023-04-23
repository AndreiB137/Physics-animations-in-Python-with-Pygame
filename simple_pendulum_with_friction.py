import pygame
import sys
import numpy as np
from numpy.linalg import inv
from pygame.locals import *
import math
from math import sin, cos, pi

def update(a):
	scale = 100
	x = l * scale * sin(a) + offset[0]
	y = l * scale * cos(a) + offset[1]

	return (x, y)



def render(point):
	scale = 10
	x, y = int(point[0]), int(point[1])

	if prev_point:
		xp, yp = prev_point[0], prev_point[1]
		pygame.draw.line(trace, PINK, (xp, yp), (x, y), 4)

	screen.fill(WHITE)
	screen.blit(trace, (0, 0))

	pygame.draw.line(screen, BLACK, offset, (x, y), 5)
	pygame.draw.circle(screen, BLACK, offset, 8)
	pygame.draw.circle(screen, RED, (x, y), int(m * scale))

	return x, y

w, h = 1400, 1400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (150, 200, 110)
BLUE = (0, 255, 0)
offset = (700, 50)

screen = pygame.display.set_mode((w, h))
screen.fill(WHITE)
trace = screen.copy()
pygame.display.update()
clock = pygame.time.Clock()

m = 2.0
l = 4.0
a = pi / 3 # amplitude
g = 9.81
t = 0
delta_t = 0.01
omega = 1 # frequency of oscilations
y = np.array([0.0, a])
prev_point = None
b = 0.3
friction_coef = -b / (2 * m)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	point = update(y[1])

	prev_point = render(point)

	t += delta_t
	y[1] = a * math.exp(friction_coef * t) * cos(omega * t)

	clock.tick(144)
	pygame.display.update()