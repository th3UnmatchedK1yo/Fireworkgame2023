import pygame, sys, random, math
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
FPS = 60
SIZE = 4.5 
SPEED_CHANGE_SIZE = 0.05 
CHANGE_SPEED = 0.07 
RAD = math.pi/180 
A_FALL = 1.5 
NUM_BULLET = 50 
SPEED_MIN = 2 
SPEED_MAX = 4 
TIME_CREAT_FW = 40 
NUM_FIREWORKS_MAX = 3 
NUM_FIREWORKS_MIN = 1 
SPEED_FLY_UP_MAX = 12 
SPEED_FLY_UP_MIN = 8 

class Dot(): 
	def __init__(self, x, y, size, color):
		self.x = x 
		self.y = y
		self.size = size
		self.color = color
	def update(self):
		
		if self.size > 0:
			self.size -= SPEED_CHANGE_SIZE*5
		else:
			self.size = 0
	def draw(self): 
		if self.size > 0:
			pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))
		

class BulletFlyUp(): 
	def __init__(self, speed, x):
		self.speed = speed
		self.x = x
		self.y = WINDOWHEIGHT
		self.dots = [] 
		self.size = SIZE/2
		self.color = (255, 255, 100)

	def update(self):
		self.dots.append(Dot(self.x, self.y, self.size, self.color)) 
		self.y -= self.speed
		self.speed -= A_FALL*0.1
		
		for i in range(len(self.dots)):
			self.dots[i].update()
		
		i = 0
		while i < len(self.dots):
			if self.dots[i].size <= 0:
				self.dots.pop(i)
			else:
				i += 1

	def draw(self):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size)) 
		
		for i in range(len(self.dots)):
			self.dots[i].draw()
		
		

class Bullet(): 
	def __init__(self, x, y, speed, angle, color):
		self.x = x
		self.y = y
		self.speed = speed
		self.angle = angle 
		self.size = SIZE
		self.color = color

	def update(self):
		
		speedX = self.speed * math.cos(self.angle*RAD) 
		speedY = self.speed * -math.sin(self.angle*RAD)
		
		self.x += speedX
		self.y += speedY
		self.y += A_FALL
		
		if self.size > 0:
			self.size -= SPEED_CHANGE_SIZE
		else:
			self.size = 0
		
		if self.speed > 0:
			self.speed -= CHANGE_SPEED
		else:
			self.speed = 0

	def draw(self):
		if self.size > 0:
			pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))
		

class FireWork():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.dots = [] 

		def creatBullets(): 
			bullets = []
			color = Random.color()
			for i in range(NUM_BULLET):
				angle =  (360/NUM_BULLET)*i
				speed = random.uniform(SPEED_MIN, SPEED_MAX)
				bullets.append(Bullet(self.x, self.y, speed, angle, color))
			return bullets
		self.bullets = creatBullets()

	def update(self):
		for i in range(len(self.bullets)): 
			self.bullets[i].update()
			self.dots.append(Dot(self.bullets[i].x, self.bullets[i].y, self.bullets[i].size, self.bullets[i].color))
		for i in range(len(self.dots)): 
			self.dots[i].update()
		
		i = 0
		while i < len(self.dots):
			if self.dots[i].size <= 0:
				self.dots.pop(i)
			else:
				i += 1
	def draw(self):
		for i in range(len(self.bullets)): 
			self.bullets[i].draw()
		for i in range(len(self.dots)): 
			self.dots[i].draw()

class Random():
	def __init__(self):
		pass
		
	def color(): 
		
		color1 = random.randint(0, 255)
		color2 = random.randint(0, 255)
		if color1 + color2 >= 255:
			color3 = random.randint(0, 255)
		else:
			color3 = random.randint(255 - color1 - color2, 255)
		colorList = [color1, color2, color3]
		random.shuffle(colorList)
		return colorList
	def num_fireworks(): 
		return random.randint(NUM_FIREWORKS_MIN, NUM_FIREWORKS_MAX)
	def randomBulletFlyUp_speed(): 
		speed = random.uniform(SPEED_FLY_UP_MIN, SPEED_FLY_UP_MAX)
		return speed
	def randomBulletFlyUp_x(): 
		x = random.randint(int(WINDOWWIDTH*0.2), int(WINDOWHEIGHT*0.8))
		return x




def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	fireWorks = []
	time = TIME_CREAT_FW
	bulletFlyUps = []
	
	while True:
		DISPLAYSURF.fill((0, 0, 0)) 
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		if time == TIME_CREAT_FW: 
			for i in range(Random.num_fireworks()):
				bulletFlyUps.append(BulletFlyUp(Random.randomBulletFlyUp_speed(), Random.randomBulletFlyUp_x()))

		for i in range(len(bulletFlyUps)): 
			bulletFlyUps[i].draw()
			bulletFlyUps[i].update()

		for i in range(len(fireWorks)):
			fireWorks[i].draw()
			fireWorks[i].update()

		i = 0
		while i < len(bulletFlyUps):
			if bulletFlyUps[i].speed <= 0: 
				fireWorks.append(FireWork(bulletFlyUps[i].x, bulletFlyUps[i].y)) 
				bulletFlyUps.pop(i) 
			else:
				i += 1
		
		i = 0
		while i < len(fireWorks):
			if fireWorks[i].bullets[0].size <= 0:
				fireWorks.pop(i)
			else:
				i += 1

		
		if time <= TIME_CREAT_FW:
			time += 1
		else:
			time = 0
		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	main()
