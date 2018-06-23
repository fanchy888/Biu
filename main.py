# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random
from menu import *
from biu import World, enemy, Plane, ammo, pannel, Boss, Chapter
import commons
from FSM import *





#initialize
screen=pygame.display.set_mode(commons.screen_size,0,32)
pygame.display.set_caption('biu~~')
clock=pygame.time.Clock()	
pygame.init()

font=pygame.font.SysFont("corbel",30)
logo_font=pygame.font.SysFont("corbel",60)
message_font=pygame.font.SysFont("corbel",40)
font_guide=pygame.font.SysFont("corbel",20)
pannel_font=pygame.font.SysFont("consolas",30)
brick_font=pygame.font.SysFont("consolas",40)
gameover=pannel_font.render("GAME OVER",True,(0,0,0))


info1=message_font.render("Congratulations!",True,(100,100,100))
info3=font_guide.render("source code: https://github.com/fanchy888/Biu",True,(100,100,100))
info2=logo_font.render("Work of Dr_Q",True,(100,100,100))
guide1=font_guide.render("Press 'ESC' to go back to main menu",True,(0,0,0))


#ending script
position1=Vector2((commons.screen_size[0]-info1.get_width())/2,commons.screen_size[1])
position2=Vector2((commons.screen_size[0]-info2.get_width())/2,commons.screen_size[1])
position3=Vector2((commons.screen_size[0]-info3.get_width())/2,commons.screen_size[1])


plane_image=pygame.image.load('data\\armstrong.png').convert_alpha()	
ammo_image=pygame.image.load('data\\ammo.png').convert_alpha()	
enemy1_image=pygame.image.load('data\\shit.png').convert_alpha()	

brick_image=pygame.image.load('data\\brick.png').convert_alpha()	
boss_ammo_image1=pygame.image.load('data\\sperm.png').convert_alpha()	
boss_ammo_image2=pygame.image.load('data\\shit_a.png').convert_alpha()	
boss_ammo_image3=pygame.image.load('data\\condom.png').convert_alpha()	
boss_image1=pygame.image.load('data\\ass.png').convert_alpha()
boss_image2=pygame.image.load('data\\ass1.png').convert_alpha()
boss_image3=pygame.image.load('data\\ass2.png').convert_alpha()		
commons.load_game()		

enemy_list=[(enemy1_image,100,5,10,10,100),(enemy1_image,150,10,10,10,100),(enemy1_image,200,5,10,10,100),[brick_image,100,1,0,1,100,brick_font]]
plane_data=[plane_image,ammo_image,commons.user]

button1=[font,'Start',('start a new game',''),font_guide,(100,40)]
button1_1=[font,'Reset',('Reset the Game, all progress will be deleted',''),font_guide,(100,40)]
button2=[font,'Quit',('exit',''),font_guide,(100,40)]
button3=[font,'Story',('start a chapter',''),font_guide,(100,40)]
button4=[font,'Endless',('try to live longer','complete all chapters to unlock'),font_guide,(100,40)]
button5=[font,'Chapter 1',('Chapter 1','complete previous chapter to unlock'),font_guide,(150,40)]
button6=[font,'Chapter 2',('Chapter 2','complete previous chapter to unlock'),font_guide,(150,40)]
button7=[font,'Chapter 3',('Chapter 3','complete previous chapter to unlock'),font_guide,(150,40)]
button8=[font,'Chapter 4',('Chapter 4','coming soon'),font_guide,(150,40)]
button_back=[font_guide,'Back',('',''),font_guide,(60,40)]
button_yes=[font_guide,'Yes',('',''),font_guide,(60,30)]
button_no=[font_guide,'No',('',''),font_guide,(60,30)]
button_resume=[font_guide,'Resume',('',''),font_guide,(80,30)]
button_restart=[font_guide,'Restart',('',''),font_guide,(80,30)]
button_goback=[font_guide,'Give up',('',''),font_guide,(80,30)]
button_quit=[font_guide,'Quit',('',''),font_guide,(80,30)]

menu1=Menu([button1,button1_1,button2])
menu2=Menu([button3,button4,button_back])
menu3=Menu([button5,button6,button7,button8,button_back])
menus=[menu1,menu2,menu3]
tip=tip_window([button_yes,button_no],font)
pause_tip=pause_menu([button_resume,button_restart,button_goback,button_quit],font)
retry_button=minibutton(pannel_font)

world1=World(commons.world_size,enemy_list,message_font)	
plane1=Plane(world1,plane_data)
world1.add_champ(plane1)
pannel1=pannel(world1,pannel_font,commons.pannel_size)

boss1=[boss_image1,boss_ammo_image1,50,100,50,1]
boss2=[boss_image2,boss_ammo_image2,100,100,60,0.8]
boss3=[boss_image3,boss_ammo_image3,150,100,70,0.7]

chapter1=Chapter('Chapter 1',boss1,15,[(0,1)])
chapter2=Chapter('Chapter 2',boss2,15,[(0,2),(1,1)])
chapter3=Chapter('Chapter 3',boss3,15,[(2,1),(1,0.5),(0,2)])
chapter_end=Chapter('Endless',None,-1,[(3,5)])

world1.add_chapter(chapter1)
world1.add_chapter(chapter2)
world1.add_chapter(chapter3)
world1.add_chapter(chapter_end)


#in game:
#give up current game
def retry():
	global game_FSM
	commons.giveup=False
	game_FSM.change_state('menu')
#restart from current chapter
def reset():
	global world1,plane1,pannel1,plane_data
	world1.reset()
	pannel1.reset()
	commons.restart=False
		
def run_game():	
	for event in pygame.event.get():	
		if event.type==QUIT:
			commons.isQuit=True		
	press_key=pygame.key.get_pressed()	
	if not press_key[K_LEFT] and not press_key[K_RIGHT]:		
		world1.champ.direction=Vector2(0,0)
	if press_key[K_LEFT]:
		world1.champ.direction=Vector2(-1,0)
	if press_key[K_RIGHT]:
		world1.champ.direction=Vector2(1,0)
	if press_key[K_RIGHT] and press_key[K_LEFT]:
		world1.champ.direction=Vector2(0,0)
	if press_key[K_ESCAPE]:
		commons.pause=True

	time=clock.tick()
	world1.process(time)	
	world1.display(screen)
	pannel1.display(screen)
	if world1.champ.dead:
		commons.isDead=True
	
def run_menu(id):
	global menus
	screen.fill((200,255,255))
	buttons=pygame.mouse.get_pressed()
	press_key=pygame.key.get_pressed()			
	for event in pygame.event.get():	
		if event.type==QUIT:
			commons.isQuit=True
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			menus[id].process()	
		if event.type==KEYDOWN and event.key==K_ESCAPE:
			if commons.menu_id>0:
				commons.menu_id-=1
			else:
				commons.isQuit=True
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	menus[id].display(screen,mouse_position)

def run_end():
	global world1,pannel1,position1,position2,position3
	screen.fill((200,255,255))				
	press_key=pygame.key.get_pressed()	
	for event in pygame.event.get():	
		if event.type==QUIT:
			commons.isQuit=True
			
	if press_key[K_ESCAPE]:
		commons.s_change=True
	time=clock.tick()
	world1.process(time)	
	world1.display(screen)
	if pannel1.position[1]<=commons.screen_size[1]:
		pannel1.position+=Vector2(0,1)*time/1000*50
		pannel1.display(screen)
	else:
		if position1[1]>=-info1.get_height():
			screen.blit(info1,position1)		
			position1+=Vector2(0,-1)*50*time/1000
		position2[1]=max((commons.screen_size[1]-info2.get_height())/2,position1[1]+360)
		screen.blit(info2,position2)	
		position3[1]=position2[1]+info2.get_height()+20	
		screen.blit(info3,position3)		
		if (world1.time%2<1.5):
			screen.blit(guide1,commons.screen_size-guide1.get_size())
			
def run_exit():
	buttons=pygame.mouse.get_pressed()
	press_key=pygame.key.get_pressed()			
	for event in pygame.event.get():	
		if event.type==QUIT:
			exit()
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			tip.process()	
	
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	tip.display(screen,mouse_position)

def run_pause():
	buttons=pygame.mouse.get_pressed()
	press_key=pygame.key.get_pressed()			
	for event in pygame.event.get():	
		if event.type==QUIT:
			exit()
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			pause_tip.process()	
	
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	pause_tip.display(screen,mouse_position)
	
def run_over():
	buttons=pygame.mouse.get_pressed()
	press_key=pygame.key.get_pressed()			
	for event in pygame.event.get():	
		if event.type==QUIT:
			exit()
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			retry_button.process()	
	
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	pygame.draw.rect(screen,(255,255,255),((commons.screen_size-gameover.get_size())/2-(0,2),gameover.get_size()),0)
	screen.blit(gameover,(commons.screen_size-gameover.get_size())/2)	
	retry_button.display(screen,mouse_position)
	
#the state of the entire program
class state_(object):
	def __init__(self,name,next):
		self.name=name
		self.next=next
	def start(self):
		commons.s_change=False
		if self.name=='game':
			reset()
	def run(self):
		mega_run(self.name)
	def stop(self):
		commons.s_change=False
		if self.name=='end':					
			commons.menu_id=0
			global position1,position1,position3
			position1=Vector2((commons.screen_size[0]-info1.get_width())/2,commons.screen_size[1])
			position1=Vector2((commons.screen_size[0]-info2.get_width())/2,commons.screen_size[1])
			position3=Vector2((commons.screen_size[0]-info3.get_width())/2,commons.screen_size[1])
	def check(self):
		if commons.s_change:
			return self.next
		else:
			return self.name
			
def mega_run(id):
	if id=='game':
		run_game()
	if id=='menu':
		run_menu(commons.menu_id)
	if id=='end':
		run_end()

game_FSM=FSM()		
game_FSM.add_state(state_('menu','game'))
game_FSM.add_state(state_('game','end'))
game_FSM.add_state(state_('end','menu'))
game_FSM.change_state('menu')






		

	
while True:

	if commons.isQuit:
		run_exit()
	elif commons.pause:
		run_pause()
	elif commons.isDead:
		run_over()
	else:	
		game_FSM.think()
	if commons.restart:
		reset()
	if commons.giveup:
		retry()
	
	pygame.display.flip()			
	
	
		
