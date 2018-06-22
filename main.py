# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random
from menu import Menu, Button, tip_window
from biu import World, enemy, Plane, ammo, pannel, Boss, Chapter
import commons
from FSM import *
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
guide1=font_guide.render("Press 'SPACE' to go back to main menu",True,(0,0,0))


#ending script
position1=Vector2((commons.screen_size[0]-info1.get_width())/2,commons.screen_size[1])
position2=Vector2((commons.screen_size[0]-info2.get_width())/2,commons.screen_size[1])
position3=Vector2((commons.screen_size[0]-info3.get_width())/2,commons.screen_size[1])


plane_image=pygame.image.load('data\\armstrong.png').convert_alpha()	
ammo_image=pygame.image.load('data\\sperm.png').convert_alpha()	
enemy_image=pygame.image.load('data\\shit.png').convert_alpha()	
boss_image=pygame.image.load('data\\ass.png').convert_alpha()	
brick_image=pygame.image.load('data\\brick.png').convert_alpha()	
boss_ammo_image=pygame.image.load('data\\ammo.png').convert_alpha()	
startpoint=Vector2((commons.world_size[0]-plane_image.get_width())/2,commons.world_size[1]-plane_image.get_height())


enemy_list=[(enemy_image,100,5,5,10,1),(enemy_image,200,5,5,10,1),(enemy_image,300,5,5,10,1),[brick_image,100,1,0,0,100,brick_font]]
plane_data=[plane_image,ammo_image,startpoint,200,100,0.2,1,1]

button1=[font,'Start',('start a new game',''),font_guide,(100,40)]
button2=[font,'Quit',('exit',''),font_guide,(100,40)]
button3=[font,'Story',('start a chapter',''),font_guide,(100,40)]
button4=[font,'Endless',('begin endless game','complete all chapters to unlock'),font_guide,(100,40)]
button5=[font,'Chapter 1',('Chapter 1','complete previous chapter to unlock'),font_guide,(150,40)]
button6=[font,'Chapter 2',('Chapter 2','complete previous chapter to unlock'),font_guide,(150,40)]
button7=[font,'Chapter 3',('Chapter 3','complete previous chapter to unlock'),font_guide,(150,40)]
button8=[font,'Chapter 4',('Chapter 4','this chapter has not been finished yet'),font_guide,(150,40)]
button_back=[font,'Back',('',''),font_guide,(60,40)]
button_yes=[font_guide,'Yes',('',''),font_guide,(60,30)]
button_no=[font_guide,'No',('',''),font_guide,(60,30)]
menu1=Menu([button1,button2])
menu2=Menu([button3,button4,button_back])
menu3=Menu([button5,button6,button7,button8,button_back])
menus=[menu1,menu2,menu3]
tip=tip_window([button_yes,button_no],font)

world1=World(commons.world_size,enemy_list,message_font)	
plane1=Plane(world1,plane_data)
world1.add_champ(plane1)
pannel1=pannel(world1,pannel_font,commons.pannel_size)

boss1=[boss_image,boss_ammo_image,50,100,100,1]

chapter1=Chapter('Chapter 1',boss1,2,[(0,1)])
chapter2=Chapter('Chapter 2',boss1,2,[(0,2),(1,1)])
chapter3=Chapter('Chapter 3',boss1,2,[(2,1)])
chapter_end=Chapter('Endless',None,-1,[(3,5)])

world1.add_chapter(chapter1)
world1.add_chapter(chapter2)
world1.add_chapter(chapter3)
world1.add_chapter(chapter_end)

def retry():
	global position1,position2,position3,game_FSM
	#game_FSM.change_state('menu')
	position1=Vector2((commons.screen_size[0]-info1.get_width())/2,commons.screen_size[1])
	position2=Vector2((commons.screen_size[0]-info2.get_width())/2,commons.screen_size[1])
	position3=Vector2((commons.screen_size[0]-info3.get_width())/2,commons.screen_size[1])
def reset(mode):
	global world1,plane1,pannel1,plane_data
	world1.reset()
	pannel1.reset()
	world1.FSM.change_state(mode)
		
def run_game():
	for event in pygame.event.get():	
		if event.type==QUIT:
			commons.isQuit=True
	press_key=pygame.key.get_pressed()	
	if press_key[K_ESCAPE]:
		commons.isQuit=True	
	if not press_key[K_LEFT] and not press_key[K_RIGHT]:		
		world1.champ.direction=Vector2(0,0)
	if press_key[K_LEFT]:
		world1.champ.direction=Vector2(-1,0)
	if press_key[K_RIGHT]:
		world1.champ.direction=Vector2(1,0)
	if press_key[K_RIGHT] and press_key[K_LEFT]:
		world1.champ.direction=Vector2(0,0)
	if press_key[K_r]:
		retry()
		game_FSM.change_state('menu')
	time=clock.tick()
	world1.process(time)	
	world1.display(screen)
	pannel1.display(screen)
	if world1.champ.dead:
		pygame.draw.rect(screen,(255,255,255),((commons.screen_size-gameover.get_size())/2-(0,2),gameover.get_size()),0)
		screen.blit(gameover,(commons.screen_size-gameover.get_size())/2)	
	if commons.isQuit:
		run_exit()

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
			if id==1:
				reset(commons.mode)
	if press_key[K_ESCAPE]:
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
			
	if press_key[K_SPACE]:
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

#the state of the entire program
class state_(object):
	def __init__(self,name,next):
		self.name=name
		self.next=next
	def start(self):
		commons.s_change=False
	def run(self):
		mega_run(self.name)
	def stop(self):
		commons.s_change=False
		if self.name=='end':
			commons.menu_id=0		
			retry()
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
	else:	
		game_FSM.think()
	pygame.display.flip()			
	
	
		
