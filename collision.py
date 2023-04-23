import pygame
import sys
from pygame.locals import *
from math import sin, cos, pi
import numpy as np
import random
import math

def render():

	screen.fill(WHITE)
	# horizontal lines
	pygame.draw.line(screen, BLACK, (offset[0] - 300, offset[1] + 300), (offset[0] + 300, offset[1] + 300), 5)
	pygame.draw.line(screen, BLACK, (offset[0] - 300, offset[1] - 300), (offset[0] + 300, offset[1] - 300), 5)
	# vertical lines
	pygame.draw.line(screen, BLACK, (offset[0] - 300, offset[1] + 300), (offset[0] - 300, offset[1] - 300), 5)
	pygame.draw.line(screen, BLACK, (offset[0] + 300, offset[1] + 300), (offset[0] + 300, offset[1] - 300), 5)
	for i in range(0, nr_objects):
		pygame.draw.circle(screen, objects[i].color, (int(objects[i].x), int(objects[i].y)), objects[i].radius)
	
def dist(x1, y1, x2, y2):
	return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

def random_color():
	r = random.randrange(0, 255)
	g = random.randrange(0, 255)
	b = random.randrange(0, 255)
	return (r, g, b)

def after_collision_wall(i, type):
	if type == 1:
		# vertical wall collision
		objects[i].dx = -objects[i].dx
	elif type == 2:
		# horizontal wall collision
		objects[i].dy = -objects[i].dy

def after_collision_balls(i, j):
	m1 = objects[i].mass
	m2 = objects[j].mass
	v1x = objects[i].dx
	v1y = objects[i].dy
	v2x = objects[j].dx
	v2y = objects[j].dy
	objects[i].dx = (m1 - m2) * v1x / (m1 + m2) + 2 * m2 * v2x / (m1 + m2)
	objects[j].dx = 2 * m1 * v1x / (m1 + m2) + (m2 - m1) * v2x / (m1 + m2)
	objects[i].dy = (m1 - m2) * v1y / (m1 + m2) + 2 * m2 * v2y / (m1 + m2)
	objects[j].dy = 2 * m1 * v1y / (m1 + m2) + (m2 - m1) * v2y / (m1 + m2)


def detect_collision():
	for i in range(0, nr_objects - 1):
		for j in range(i + 1, nr_objects):
			if dist(objects[i].x, objects[i].y, objects[j].x, objects[j].y) <= objects[i].radius + objects[j].radius:
				after_collision_balls(i, j)

	for i in range(0, nr_objects):
		# collision with a wall
		if objects[i].x + objects[i].radius <= offset[0] - 275 or objects[i].x + objects[i].radius >= offset[0] + 300:
			after_collision_wall(i, 1)
		elif objects[i].y + objects[i].radius <= offset[1] - 275 or objects[i].y + objects[i].radius >= offset[1] + 300:
			after_collision_wall(i, 2)



class ball:
	def __init__(self, x, y, dx, dy, radius, color, mass):
		dx = random.randrange(-200, 200)
		dy = random.randrange(-200, 200)
		color = random_color()
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.radius = radius
		self.color = color
		self.mass = mass


def update(dt):
	for i in range(0, nr_objects):
		objects[i].x += dt * objects[i].dx
		objects[i].y += dt * objects[i].dy


w, h = 1400, 1000
offset = (700, 500)

screen = pygame.display.set_mode((w,h))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen.fill(WHITE)
trace = screen.copy()
pygame.display.update()
clock = pygame.time.Clock()

t = 0.0
fps = 1000
delta_t = 1 / fps
objects = []
nr_objects = 200
cnt = 0

while cnt < nr_objects:
	x = random.randrange(offset[0] - 300 + 10 + 5, offset[0] + 300 - 10 - 5)
	y = random.randrange(offset[1] - 300 + 10 + 5, offset[1] + 300 - 10 - 5)
	found = False
	for i in range(0, len(objects)):
		if not(found) and dist(objects[i].x, objects[i].y, x, y) <= 20:
			found = True
	if not(found):
		objects.append(ball(x, y, 0, 0, 10, 0, 5))
		cnt += 1

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	#print(objects[0].dx, objects[0].dy)
	detect_collision()
	update(delta_t)
	render()

	t += delta_t

	clock.tick(fps)
	pygame.display.update()
