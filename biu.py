# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random

startpoint=Vector2(300,400)
class World(object):
	def __init__(self):
		self.entities={}
		self.entity_id=0
		self.background=pygame.surface.Surface(screen_size).convert()
		self.background.fill((255,255,255))
	def add_entity(self,entity):
		self.entities[self.entity_id]=entity
		entity.id=self.entity_id
		self.entity_id+=1
	def delete_entity(self,entity):
		del self.entities[entity.id]
	def process(self,time):
		time_tick=time/1000.0
		entities=self.entities.copy()
		for key in entities.keys():
			self.entities[key].process(time_tick)
			
	def display(self,surface):
		surface.fill((255,255,255))
		for entity in self.entities.values():
			entity.display(surface)
			
			
class Plane(object):
	def __init__(self,image,world):
		self.image=image
		self.position=startpoint
		self.dead=False
		self.speed=200
		self.direction=Vector2(0,0)
		self.fire=True
		self.world=world
		self.id=0
		self.cd=0.5
	def move(self,time):
		self.position+=self.direction*self.speed*time
	def check(self,mouse):
		if (self.position[0]<=1 and self.direction==(-1,0)) or (self.position[0]>=571 and self.direction==(1,0)):
			self.direction=Vector2(0,0)
		self.position[0]=mouse[0]
	def Fire(self):
		if self.fire and self.cd<0:
			shoot()
			self.cd=0.2
	def process(self,time):
		self.Fire()
		self.move(time)
		self.cd-=time
	def display(self,surface):
		surface.blit(self.image,self.position)
		
class ammo(object):		
	def __init__(self,image,world):
		self.image=image
		self.speed=1000
		self.position=world.entities[0].position+(22,-23)
		self.world=world
		self.id=-1
	def move(self,time):
		self.position+=self.speed*Vector2(0,-1)*time
	def check(self):
		if self.position[1]<0:
			self.world.delete_entity(self.world.entities[self.id])
	def display(self,surface):
		surface.blit(self.image,self.position)	
	def process(self,time):
		self.check()
		self.move(time)
		
clock=pygame.time.Clock()		
screen_size=Vector2(640,480)
pygame.init()
screen=pygame.display.set_mode(screen_size,0,32)
pygame.display.set_caption('biu~~')

world1=World()	

planepic=pygame.image.load('planepic.png').convert()	
plane1=Plane(planepic,world1)
ammopic=pygame.image.load('ammo.png').convert()	
world1.add_entity(plane1)	
def shoot():
	global world1
	bullet=ammo(ammopic,world1)
	world1.add_entity(bullet)



while True:
	
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()			
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:
				exit()
			if event.key==K_LEFT:
				world1.entities[0].direction=Vector2(-1,0)
			if event.key==K_RIGHT:
				world1.entities[0].direction=Vector2(1,0)

	mouse_position=pygame.mouse.get_pos()

	time=clock.tick()
	world1.entities[0].check(mouse_position)
	world1.process(time)
	world1.display(screen)
	

	pygame.display.update()
