import sys, pygame
pygame.init()

size = width, height = 1024, 768
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ship.png")
ballrect = ball.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		
	key = pygame.key.get_pressed()
	
	if key[pygame.K_DOWN]:
		ballrect = ballrect.move(speed)
		speed = [0, 1]
	if key[pygame.K_RIGHT]:
		ballrect = ballrect.move(speed)
		speed = [1, 0]
	if key[pygame.K_UP]:
		ballrect = ballrect.move(speed)
		speed = [0, -1]
	if key[pygame.K_LEFT]:
		ballrect = ballrect.move(speed)
		speed = [-1, 0]
	
	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()
