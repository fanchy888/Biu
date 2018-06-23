from vector import Vector2
from sys import exit
import pickle
import os

screen_size=Vector2(400,720)
pannel_size=Vector2(screen_size[0],100)
world_size=Vector2(screen_size[0],620)


user=[0,200,100,0.2,1,1,0]
menu_id=0
s_change=False
isQuit=False
pause=False
restart=False
giveup=False
isDead=False
mode=['gameover',0]
flags={}
flags['Start']=True
flags['Quit']=True
flags['Reset']=True
flags['Story']=True
flags['Endless']=False
flags['Chapter 1']=True
flags['Chapter 2']=False
flags['Chapter 3']=False
flags['Chapter 4']=False
flags['Back']=True
flags['Yes']=True
flags['No']=True
flags['Restart']=True
flags['Resume']=True
flags['Give up']=True

def RST():
	global user,menu_id,s_change,isQuit,pause,restart,giveup,flags,mode
	user=[0,200,100,0.2,1,1,0]
	menu_id=0
	s_change=False
	isQuit=False
	pause=False
	restart=False
	giveup=False
	mode=['gameover',0]
	flags['Endless']=False
	flags['Chapter 2']=False
	flags['Chapter 3']=False
	flags['Chapter 4']=False
	save_game()
	return
	
def set_world(index):
	global mode,menu_id,s_change,isQuit,pause,restart,giveup,isDead
	if index=='Start':
		menu_id+=1
	if index=='Quit':
		isQuit=True
	if index=='Reset':
		RST()
	if index=='Story':
		menu_id+=1
		mode[0]='pushing'
	if index=='Endless':
		s_change=True
		mode[0]='endless'
		mode[1]=-1
	if index=='Chapter 1':
		s_change=True
		mode[1]=0
	if index=='Chapter 2':
		s_change=True
		mode[1]=1
	if index=='Chapter 3':
		s_change=True
		mode[1]=2
	if index=='Back':
		menu_id-=1
	if index=='Yes':
		save_game()
		exit()
	if index=='No':
		isQuit=False
	if index=='Resume':
		pause=False
	if index=='Restart':
		pause=False
		restart=True
	if index=='Give up':
		giveup=True
		pause=False
	if index=='OK':
		isDead=False
		giveup=True
		
		
		'''
	if index=='Chapter 4':
		current_statu='game'
		mode='pushing'
		'''
	return 
	
def load_game():
	global user,flags
	data={}
	with open('data\\userdata.txt','rb') as f1:
		data=pickle.load(f1)
	flags['Endless']=data['Endless']
	flags['Chapter 2']=data['Chapter 2']
	flags['Chapter 3']=data['Chapter 3']
	user[0]=data['exp']
	user[1]=data['speed']	
	user[2]=data['hp']
	user[3]=data['gun_cd']
	user[4]=data['gun_nums']
	user[5]=data['lv']
	user[6]=data['coins']
	return 

def save_game():
	global user,flags
	data={}
	data['Endless']=flags['Endless']
	data['Chapter 2']=flags['Chapter 2']
	data['Chapter 3']=flags['Chapter 3']
	data['exp']=user[0]
	data['speed']=user[1]
	data['hp']=user[2]
	data['gun_cd']=user[3]
	data['gun_nums']=user[4]
	data['lv']=user[5]
	data['coins']=user[6]
	with open('data\\userdata.txt','wb') as f2:
		data=pickle.dump(data,f2)	
		
	return
	