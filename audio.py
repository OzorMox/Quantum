import sys, pygame

def play():
	#Play test file for now (anaconda!)
	pygame.mixer.music.load("anaconda.mp3")
	pygame.mixer.music.play()
	

def stop():
	pygame.mixer.music.stop()
