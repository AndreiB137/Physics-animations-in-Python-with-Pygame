import pygame
import sys
import numpy as np
from numpy.linalg import inv
from pygame.locals import *
from math import sin, cos, pi
import math
from spring import spring

class Spring():
	def __init__(self, color, start, end, nodes, width, lead1, lead2):
		self.start = start
		self.end = end
		self.nodes = nodes
		self.width = width
		self.lead1 = lead1
		self.lead2 = lead2
		self.weight = 3
		self.color = color

	def update(self, start, end):
		self.start = start
		self.end = end

		self.x, self.y, self.p1, self.p2 = spring(self.start, self.end, self.nodes, self.width, self.lead1, self.lead2)
		self.p1 = (int(self.p1[0]), int(self.p1[1]))
		self.p2 = (int(self.p2[0]), int(self.p2[1]))

	def render(self):
		pygame.draw.line(screen, self.color, self.start, self.p1, self.weight)
		prev_point = self.p1
		for point in zip(self.x, self.y):
			pygame.draw.line(screen, self.color, prev_point, point, self.weight)
			prev_point = point
		pygame.draw.line(screen, self.color, self.p2, self.end, self.weight)


def G(y, t):
	a1d, a2d = y[0], y[1]
	a1, a2 = y[2], y[3]

	f1 = -g / l * sin(a1) - k  / (m1 * l) * cos(a1) * (sin(a1) - sin(a2))
	f2 = -g / l * sin(a2) + k / (m2 * l) * cos(a2) * (sin(a1) - sin(a2))
	f = np.array([f1, f2])

	return np.array([f1, f2, a1d, a2d])


def RK4(y, t, dt):
	k1 = G(y, t)
	k2 = G(y + 0.5 * k1 * dt, t + 0.5 * dt)
	k3 = G(y + 0.5 * k2 * dt, t + 0.5 * dt)
	k4 = G(y + k3 * dt, t + dt)

	return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

def update(a1, a2):
	scale = 100
	x1 = l * scale * sin(a1) + offset1[0]
	x2 = l * scale * sin(a2) + offset2[0]

	return (x1, 50 + scale * l), (x2, 50 + scale * l)



def render(point1, point2):
	scale = 10
	x1, y1 = int(point1[0]), int(point1[1])
	x2, y2 = int(point2[0]), int(point2[1])

	screen.fill(WHITE)

	pygame.draw.line(screen, BLACK, offset1, offset2, 5)
	pygame.draw.line(screen, BLACK, offset1, (x1, y1), 5)
	pygame.draw.line(screen, BLACK, offset2, (x2, y2), 5)
	s.update((x1, y1), (x2, y2))
	s.render()
	pygame.draw.circle(screen, BLACK, offset2, 8)
	pygame.draw.circle(screen, BLACK, offset1, 8)
	pygame.draw.circle(screen, RED, (x1, y1), int(m1 * scale))
	pygame.draw.circle(screen, BLUE, (x2, y2), int(m2 * scale))

w, h = 1400, 1400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
BLUE = (0, 255, 0)
offset1 = (400, 50)
offset2 = (900, 50)

screen = pygame.display.set_mode((w, h))
screen.fill(WHITE)
trace = screen.copy()
pygame.display.update()
clock = pygame.time.Clock()

m1, m2 = 4.0, 2.0
l = 2.0
k = 10
a1, a2 = pi / 2, 0.0
g = 9.81
t = 0
fps = 144

delta_t = 1 / fps
y = np.array([0.0, 0.0, pi / 6, 0.0])
A = 1
B = 1
s = Spring(PINK, (0, 0), (0, 0), 40, 30, 90, 90)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	point1, point2 = update(y[2], y[3])

	render(point1, point2)

	t += delta_t
	
	y = y + RK4(y, t, delta_t)

	clock.tick(fps)
	pygame.display.update()