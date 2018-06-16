# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random


class World(object):
	def __init__(self,enemy_image,size):
		self.size=size
		self.entities={}
		self.bullets={}
		self.bullet_id=0
		self.entity_id=0
		self.background=pygame.surface.Surface(size).convert()
		self.background.fill((200,255,255))
		self.enemy_fraq=1
		self.enemy_image=enemy_image
		self.status=True #alive or dead
	def add_entity(self,entity):
		self.entities[self.entity_id]=entity
		entity.id=self.entity_id
		self.entity_id+=1
	def add_bullet(self,bullet):
		self.bullets[self.bullet_id]=bullet
		bullet.id=self.bullet_id
		self.bullet_id+=1
	def delete_entity(self,id):
		del self.entities[id]
	def delete_bullet(self,id):
		del self.bullets[id]
		
	def process(self,time):
		time_tick=time/1000.0
		self.enemy_fraq-=time_tick
		entities=self.entities.copy()
		bullets=self.bullets.copy()
		if self.status:
			for key in entities.keys():
				self.entities[key].process(time_tick)
			for key in bullets.keys():
				self.bullets[key].process(time_tick)
			self.enemy_attack()	

	def display(self,surface):
		surface.blit(self.background,(0,0))
		for entity in self.entities.values():
			entity.display(surface)
		for bullet in self.bullets.values():
			bullet.display(surface)
#enemy appears
	def enemy_attack(self):
		if self.enemy_fraq<=0:			
			a=enemy(self.enemy_image,self)
			self.add_entity(a)
			self.enemy_fraq=0.9**self.entities[0].level
			
			
class Plane(object):
	def __init__(self,image,world,startpoint,weapon_image):
		self.image=image
		self.weapon_image=weapon_image
		self.position=startpoint
		self.dead=False
		self.speed=200
		self.direction=Vector2(0,0)
		self.fire=True
		self.world=world
		self.id=0
		self.cd=0.2
		self.name='plane'
		self.hp=100
		self.score=0
		self.guns=1
		self.exp=0
		self.level=1
	def move(self,time):
		self.position+=self.direction*self.speed*time
	def check(self):
	#check boundary
		if (self.position[0]<=0 and self.direction==(-1,0)) or \
		  (self.position[0]>=self.world.size[0]-self.image.get_width() and self.direction==(1,0)):
			self.direction=Vector2(0,0)
	#check hp
		if self.hp<=0:
			self.hp=0
			self.world.status=False
	#check exp
		if self.exp>=100*(self.level):
			self.exp=0
			self.Level_up()
	def Fire(self):
		if self.fire and self.cd<=0:
			self.shoot()
			self.cd=0.2*(0.9**self.level)
	def shoot(self):
		lenth=max(self.image.get_width()/self.guns,20)
		fire_range=lenth*self.guns
		first_gun=self.position-((fire_range-self.image.get_width())/2,0)
		for i in range(self.guns):			
			shift=(lenth-self.weapon_image.get_width())/2+lenth*i
			gun_position=first_gun+(shift,0)
			bullet=ammo(self.weapon_image,self.world,gun_position)
			self.world.add_bullet(bullet)
	def Level_up(self):
		self.guns+=1
		self.level+=1
	def process(self,time):
		self.check()
		self.Fire()
		self.move(time)
		self.cd-=time
	def display(self,surface):
		surface.blit(self.image,self.position)

		
class ammo(object):		
	def __init__(self,image,world,position):
		self.image=image
		self.speed=1000
		self.position=position
		self.world=world
		self.id=0
		self.name='biu'
		self.damage=1
	def move(self,time):
		self.position+=self.speed*Vector2(0,-1)*time
	def check(self):
		if self.position[1]<0:
			self.world.delete_bullet(self.id)
		else:
			self.hit()		
	def display(self,surface):
		surface.blit(self.image,self.position)	
	def process(self,time):
		self.check()
		self.move(time)
	def hit(self):
		for enemy in self.world.entities.copy().values():
			if enemy.name=='enemy':
				if self.position[0]>=enemy.position[0]-self.image.get_width()and \
				   self.position[0]<=enemy.position[0]+enemy.image.get_width() and \
				   self.position[1]<=enemy.position[1]+enemy.image.get_height():
					self.world.delete_bullet(self.id)
					self.world.entities[enemy.id].hp-=self.damage
					break
	
	
class enemy(object):
	def __init__(self,image,world):
		self.name='enemy'
		self.speed=random.randint(100,200)
		x=random.randint(0,world.size[0]-image.get_width())
		y=0-image.get_height()
		self.position=Vector2(x,y)
		self.id=-1
		self.world=world
		self.image=image
		self.hp=5
		self.target=world.entities[0]
		self.damage=15
		self.score=5
	def move(self,time):
		self.position[1]+=self.speed*time 
	def check(self):
		if self.position[1]>=self.world.size[1]:
			self.world.delete_entity(self.id)
		if self.position[1]+self.image.get_height()/2>self.target.position[1] and \
		   self.position[0]>self.target.position[0]-self.image.get_width()/3*2 and \
		   self.position[0]<self.target.position[0]+self.target.image.get_width()-self.image.get_width()/3:
			self.target.hp-=self.damage
			self.hp=0
		if self.hp<=0:
			self.world.delete_entity(self.id)
			self.target.score+=self.score
			self.target.exp+=10
	def display(self,surface):
		surface.blit(self.image,self.position)	
	def process(self,time):
		self.check()
		self.move(time)	

class pannel(object):
	def __init__(self,world,pannel_font,size):
		self.size=size
		self.background=pygame.surface.Surface(size).convert()
		self.background.fill((255,255,255))
		self.position=world.size-(world.size[0],0)
		self.world=world
		self.font=pannel_font
	def display(self,surface):
		surface.blit(self.background,self.position)
		pygame.draw.rect(surface,(0,0,0),(self.position,self.size),2)
		score=self.font.render('Score:'+str(self.world.entities[0].score),True,(0,0,0))
		Hp=self.font.render('HP:'+str(self.world.entities[0].hp),True,(0,0,0))
		Level=self.font.render('Level:'+str(self.world.entities[0].level),True,(0,0,0))
		surface.blit(Hp,self.position)
		surface.blit(score,self.position+(200,0))		
		surface.blit(Level,self.position+(0,50))
		exp_bar=self.position+(Level.get_width(),50)+(3,3)
		pygame.draw.rect(surface,(0,0,0),(exp_bar,(100,20)),2)
		pygame.draw.rect(surface,(0,0,0),(exp_bar,(self.world.entities[0].exp/self.world.entities[0].level,20)),0)
		
#initialization
'''
screen_size=Vector2(400,720)
pannel_size=Vector2(screen_size[0],100)
world_size=Vector2(screen_size[0],620)
#plane_image=pygame.image.load('plane.png').convert_alpha()	
#ammo_image=pygame.image.load('ammo.png').convert_alpha()	
#enemy_image=pygame.image.load('enemy.png').convert_alpha()	
#startpoint=Vector2((world_size[0]-plane_image.get_width())/2,world_size[1]-plane_image.get_height())


screen=pygame.display.set_mode(screen_size,0,32)
pygame.display.set_caption('biu~~')
clock=pygame.time.Clock()	
pygame.init()

font=pygame.font.SysFont("楷体",40)
pannel_font=pygame.font.SysFont("楷体",40)
gameover=font.render("GAME OVER",True,(0,0,0))

plane_image=pygame.image.load('plane.png').convert_alpha()	
ammo_image=pygame.image.load('ammo.png').convert_alpha()	
enemy_image=pygame.image.load('enemy.png').convert_alpha()	
startpoint=Vector2((world_size[0]-plane_image.get_width())/2,world_size[1]-plane_image.get_height())



world1=World()	
plane1=Plane(plane_image,world1)
world1.add_entity(plane1)
pannel1=pannel(world1)

def reset():
	global world1,plane1,pannel1
	world1=World()	
	plane1=Plane(plane_image,world1)
	world1.add_entity(plane1)
	pannel1=pannel(world1)


while True:
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
		pygame.draw.rect(screen,(255,255,255),((screen_size-gameover.get_size())/2-(0,2),gameover.get_size()),0)
		screen.blit(gameover,(screen_size-gameover.get_size())/2)	

	pygame.display.update()

'''