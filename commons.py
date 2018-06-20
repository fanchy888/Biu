from vector import Vector2
from sys import exit

screen_size=Vector2(400,720)
pannel_size=Vector2(screen_size[0],100)
world_size=Vector2(screen_size[0],620)
current_statu='Menu'
mode='gameover'
flags={}
flags['Start']=True
flags['Quit']=True
flags['Story']=True
flags['Endless']=False
def set_world(index):
	global current_statu,mode
	if index=='Start':
		current_statu='Start'
	if index=='Quit':
		current_statu='quit'
	if index=='Story':
		current_statu='Story'
		mode='pushing'
	if index=='Endless':
		current_statu='Endless'
		mode='endless'