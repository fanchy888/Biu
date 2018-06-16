# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random
from menu import Menu, Button
from biu import World, enemy, Plane, ammo, pannel
import commons

screen=pygame.display.set_mode(commons.screen_size,0,32)
pygame.display.set_caption('biu~~')
clock=pygame.time.Clock()	
pygame.init()

font=pygame.font.SysFont("楷体",40)
pannel_font=pygame.font.SysFont("楷体",40)
gameover=font.render("GAME OVER",True,(0,0,0))

plane_image=pygame.image.load('plane.png').convert_alpha()	
ammo_image=pygame.image.load('ammo.png').convert_alpha()	
enemy_image=pygame.image.load('enemy.png').convert_alpha()	
startpoint=Vector2((commons.world_size[0]-plane_image.get_width())/2,commons.world_size[1]-plane_image.get_height())

menu1=Menu(['Start','Quit'],font)
world1=World(enemy_image,commons.world_size)	
plane1=Plane(plane_image,world1,startpoint,ammo_image)
world1.add_entity(plane1)
pannel1=pannel(world1,pannel_font,commons.pannel_size)

commons.current_statu='Menu'
def reset():
	global world1,plane1,pannel1,menu1
	menu1=Menu(['Start','Quit'],font)
	world1=World(enemy_image,commons.world_size)	
	plane1=Plane(plane_image,world1,startpoint,ammo_image)
	world1.add_entity(plane1)
	pannel1=pannel(world1,pannel_font,commons.pannel_size)
	commons.current_statu='Menu'


		
def run_game():
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()					
	press_key=pygame.key.get_pressed()	
	if press_key[K_ESCAPE]:
		exit()
	if not press_key[K_LEFT] and not press_key[K_RIGHT]:		
		world1.entities[0].direction=Vector2(0,0)
	if press_key[K_LEFT]:
		world1.entities[0].direction=Vector2(-1,0)
	if press_key[K_RIGHT]:
		world1.entities[0].direction=Vector2(1,0)
	if press_key[K_RIGHT] and press_key[K_LEFT]:
		world1.entities[0].direction=Vector2(0,0)
	if press_key[K_r]:
		reset()
	time=clock.tick()
	world1.process(time)	
	world1.display(screen)
	pannel1.display(screen)
	if not world1.status:
		pygame.draw.rect(screen,(255,255,255),((commons.screen_size-gameover.get_size())/2-(0,2),gameover.get_size()),0)
		screen.blit(gameover,(commons.screen_size-gameover.get_size())/2)	

	pygame.display.flip()

def run_menu():
	buttons=pygame.mouse.get_pressed()
	screen.fill((200,255,255))
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()			
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:
				exit()		
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			menu1.process()	
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick()
	menu1.display(screen,mouse_position)
	pygame.display.flip()	


while True:

	if commons.current_statu=='Menu':
		run_menu()
	if commons.current_statu=='game':
		run_game()
	if commons.current_statu=='quit':
		exit()
