from vector import Vector2
from sys import exit

screen_size=Vector2(400,720)
pannel_size=Vector2(screen_size[0],100)
world_size=Vector2(screen_size[0],620)

menu_id=0
s_change=False
isQuit=False

mode='gameover'
flags={}
flags['Start']=True
flags['Quit']=True
flags['Story']=True
flags['Endless']=True
flags['Chapter 1']=True
flags['Chapter 2']=False
flags['Chapter 3']=False
flags['Chapter 4']=False
flags['Back']=True
flags['Yes']=True
flags['No']=True
def set_world(index):
	global mode,menu_id,s_change,isQuit
	if index=='Start':
		menu_id+=1
	if index=='Quit':
		isQuit=True
	if index=='Story':
		menu_id+=1
		mode='pushing'
	if index=='Endless':
		s_change=True
		mode='endless'
	if index=='Chapter 1':
		s_change=True
	if index=='Chapter 2':
		s_change=True
	if index=='Chapter 3':
		s_change=True
	if index=='Back':
		menu_id-=1
	if index=='Yes':
		exit()
	if index=='No':
		isQuit=False
		'''
	if index=='Chapter 4':
		current_statu='game'
		mode='pushing'
		'''
		