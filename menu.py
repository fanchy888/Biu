# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
import commons

class Button(object):
	def __init__(self,position,content,name):
		self.position=position
		self.size=Vector2(100,40)
		self.background=pygame.surface.Surface(self.size).convert()
		self.background.fill((200,200,200))
		self.content=content
		self.status=False
		self.name=name
	def display(self,surface):
		surface.blit(self.background,self.position)
		surface.blit(self.content,self.position+(self.size-self.content.get_size())/2)
		if self.status:
			pygame.draw.rect(surface,(0,0,0),(self.position,self.size),2)
	def check(self,position):
		if position[0]<=self.position[0]+self.size[0] and \
		   position[1]<=self.position[1]+self.size[1] and \
		   position[0]>=self.position[0] and position[1]>=self.position[1]:
			self.status=True
		else:
			self.status=False
	def process(self):
		if self.status:
			commons.set_world(self.name) #process the function it implies
			#print(commons.current_statu)
			
class Menu(object):
	def __init__(self,names,font):
		self.names=names
		self.buttons={}
		self.nums=len(names)
		self.font=font
		self.build_buttons()
	def build_buttons(self):
		height=self.nums*60
		x=(commons.screen_size[0]-100)/2
		y=(commons.screen_size[1]-height)/2
		for i in range(self.nums):
			content=self.font.render(self.names[i],True,(0,0,0))
			position=(x,y+60*i)
			self.buttons[self.names[i]]=Button(position,content,self.names[i])
	def display(self,surface,cursor):
		for button in self.buttons.values():
			button.check(cursor)
			button.display(surface)
	def process(self):
		for button in self.buttons.values():
			if button.status:
				button.process()

	
	
	
	
	
