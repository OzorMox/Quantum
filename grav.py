import sys, pygame
pygame.init()

size = width, height = 1024, 768
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ship = pygame.image.load("ship.png")
shiprect = ship.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		
	key = pygame.key.get_pressed()
	
	if key[pygame.K_DOWN]:
		shiprect = shiprect.move(speed)
		speed = [0, 1]
	if key[pygame.K_RIGHT]:
		shiprect = shiprect.move(speed)
		speed = [1, 0]
	if key[pygame.K_UP]:
		shiprect = shiprect.move(speed)
		speed = [0, -1]
	if key[pygame.K_LEFT]:
		shiprect = shiprect.move(speed)
		speed = [-1, 0]
	
	screen.fill(black)
	screen.blit(ship, shiprect)
	pygame.display.flip()
