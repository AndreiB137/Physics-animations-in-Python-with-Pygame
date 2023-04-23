import pygame
import sys
from pygame.locals import *
from math import sin, cos, pi
import numpy as np
from numpy.linalg import inv
from spring import spring

def F(y, t):
	x1, x2, x3, x4, x5 = y[5], y[6], y[7], y[8], y[9]
	dx1, dx2, dx3, dx4, dx5 = y[0], y[1], y[2], y[3], y[4]
	x = np.array([x1, x2, x3, x4, x5])
	ddx = A.dot(x)
	return np.array([ddx[0], ddx[1], ddx[2], ddx[3], ddx[4], dx1, dx2, dx3, dx4, dx5])

def Runge_Kutta(y, t, dt):
	k1 = F(y, t)
	k2 = F(y + 0.5 * k1 * dt, t + 0.5 * dt)
	k3 = F(y + 0.5 * k2 * dt, t + 0.5 * dt)
	k4 = F(y + k3 * dt, t + dt)

	return (k1 + 2 * k2 + 2 * k3 + k4) / 6

def update(a1, a2):
	scale = 100
	x1 = r * cos(a1) + offset[0]
	y1 = offset[1] - r * sin(a1)
	x2 = x1 + l * sin(a2)
	y2 = y1 + l * cos(a2)

	return (x1, x2, x3)

def render(point):
	scale = 10
	x1 = offset[0] - 400 + int(point[0])
	x2 = offset[0] - 200 + int(point[1])
	x3 = offset[0] + int(point[2])
	x4 = offset[0] + 200 + int(point[3])
	x5 = offset[0] + 400 + int(point[4])

	screen.fill(WHITE)

	# horizontal line
	pygame.draw.line(screen, BLACK, (offset[0] - 600, offset[1]), (offset[0] + 600, offset[1]), 5)
	# two vertical lines
	pygame.draw.line(screen, BLACK, (offset[0] - 600, offset[1]), (offset[0] - 600, offset[1] - 100), 5)
	pygame.draw.line(screen, BLACK, (offset[0] + 600, offset[1]), (offset[0] + 600, offset[1] - 100), 5)
	# create circles to lie on the horizontal line
	radius = 30
	s1.update((offset[0] - 600, offset[1] - radius), ((x1, offset[1] - radius)))
	s1.render()
	s2.update((x1, offset[1] - radius), ((x2, offset[1] - radius)))
	s2.render()
	s3.update((x2, offset[1] - radius), ((x3, offset[1] - radius)))
	s3.render()
	s4.update((x3, offset[1] - radius), ((x4, offset[1] - radius)))
	s4.render()
	s5.update((x4, offset[1] - radius), ((x5, offset[1] - radius)))
	s5.render()
	s6.update((x5, offset[1] - radius), ((offset[0] + 600, offset[1] - radius)))
	s6.render()
	pygame.draw.circle(screen, RED, (x1, offset[1] - radius), radius)
	pygame.draw.circle(screen, RED, (x2, offset[1] - radius), radius)
	pygame.draw.circle(screen, RED, (x3, offset[1] - radius), radius)
	pygame.draw.circle(screen, RED, (x4, offset[1] - radius), radius)
	pygame.draw.circle(screen, RED, (x5, offset[1] - radius), radius)

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

w, h = 1400, 1000
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
LT_BLUE = (230,230,255)
offset = (700, 500)

screen = pygame.display.set_mode((w,h))
screen.fill(WHITE)
trace = screen.copy()
pygame.display.update()
clock = pygame.time.Clock()

# parameters
m = 4
l = 150
g = 9.81
r = 100
k = 40
c = k / m
A = np.array([[-2 * c, c, 0.0, 0.0, 0.0], [c, -2 * c, c, 0.0, 0.0], [0.0, c, -2 * c, 0.0, 0.0], 
	[0.0, 0.0, c, -2 * c, c], [0.0, 0.0, 0.0, c, -2 * c]])

t = 0.0
fps = 144
delta_t = 1 / fps
y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 30.0, 50.0, 70.0, 90.0, 110.0])
agl = 0;
omega = 3

s1 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)
s2 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)
s3 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)
s4 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)
s5 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)
s6 = Spring(BLACK, (0, 0), (0, 0), 20, 50, 60, 60)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 38)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	point = (y[5], y[6], y[7], y[8], y[9])

	render(point)

	t += delta_t
	y = y + delta_t * Runge_Kutta(y, t, delta_t)

	clock.tick(fps)
	pygame.display.update()