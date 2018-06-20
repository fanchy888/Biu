# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random
from menu import Menu, Button
from biu import World, enemy, Plane, ammo, pannel, Boss, Chapter
import commons

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
guide1=font_guide.render("Press 'r' to go back to main menu",True,(0,0,0))



position1=Vector2((commons.screen_size[0]-info1.get_width())/2,commons.screen_size[1])
position2=Vector2((commons.screen_size[0]-info2.get_width())/2,commons.screen_size[1])
position3=Vector2((commons.screen_size[0]-info3.get_width())/2,commons.screen_size[1])


plane_image=pygame.image.load('plane.png').convert_alpha()	
ammo_image=pygame.image.load('ammo.png').convert_alpha()	
enemy_image=pygame.image.load('enemy.png').convert_alpha()	
brick_image=pygame.image.load('brick.png').convert_alpha()	
startpoint=Vector2((commons.world_size[0]-plane_image.get_width())/2,commons.world_size[1]-plane_image.get_height())


enemy_list=[(enemy_image,100,5,5,10,1),(enemy_image,200,5,5,10,1),(enemy_image,300,5,5,10,1),[brick_image,100,1,0,0,100,brick_font]]
plane_data=[plane_image,ammo_image,startpoint,200,100,0.2,1,1]

button1=[font,'Start',('start a new game',''),font_guide]
button2=[font,'Quit',('exit',''),font_guide]
button3=[font,'Story',('start a chapter',''),font_guide]
button4=[font,'Endless',('begin endless game','complete all chapters to unlock'),font_guide]
menu1=Menu([button1,button2])
menu2=Menu([button3,button4])
menus={}
menus['main_menu']=menu1
menus['game_mode']=menu2

world1=World(commons.world_size,enemy_list,message_font)	
plane1=Plane(world1,plane_data)
world1.add_champ(plane1)
pannel1=pannel(world1,pannel_font,commons.pannel_size)

boss1=[plane_image,ammo_image,50,100,100,1]

chapter1=Chapter(1,boss1,2,[(0,1)])
chapter2=Chapter(2,boss1,2,[(0,2),(1,1)])
chapter3=Chapter(3,boss1,2,[(2,1)])
chapter_end=Chapter('endless',None,-1,[(3,5)])

world1.add_chapter(chapter1)
world1.add_chapter(chapter2)
world1.add_chapter(chapter3)
world1.add_chapter(chapter_end)
commons.current_statu='Menu'
def retry():
	global position1,position2,position3
	commons.current_statu='Menu'
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
			exit()					
	press_key=pygame.key.get_pressed()	
	if press_key[K_ESCAPE]:
		exit()
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
	time=clock.tick()
	world1.process(time)	
	world1.display(screen)
	pannel1.display(screen)
	if world1.champ.dead:
		pygame.draw.rect(screen,(255,255,255),((commons.screen_size-gameover.get_size())/2-(0,2),gameover.get_size()),0)
		screen.blit(gameover,(commons.screen_size-gameover.get_size())/2)	

	pygame.display.flip()

def run_menu(id):
	global menus
	buttons=pygame.mouse.get_pressed()
	screen.fill((200,255,255))
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()			
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:
				exit()		
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			menus[id].process()	
			if id=='game_mode':
				reset(commons.mode)
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	menus[id].display(screen,mouse_position)
	pygame.display.flip()	

def run_end():
	global world1,pannel1,position1,position2,position3
	screen.fill((200,255,255))
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()					
	press_key=pygame.key.get_pressed()	
	if press_key[K_ESCAPE]:
		exit()	
	if press_key[K_r]:
		retry()
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
	pygame.display.flip()
	
	
while True:

	if commons.current_statu=='Menu':
		run_menu('main_menu')
	if commons.current_statu=='Start':
		run_menu('game_mode')
	if commons.current_statu=='quit':
		exit()
	if commons.current_statu=='Story':
		run_game()
	if commons.current_statu=='Endless':
		run_game()
	if commons.current_statu=='End':
		run_end()
	
	
	
	
		
