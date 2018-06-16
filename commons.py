from vector import Vector2
from sys import exit

screen_size=Vector2(400,720)
pannel_size=Vector2(screen_size[0],100)
world_size=Vector2(screen_size[0],620)
current_statu='Menu'

def set_world(index):
	global current_statu
	if index=='Start':
		current_statu='game'
	if index=='Quit':
		current_statu='quit'