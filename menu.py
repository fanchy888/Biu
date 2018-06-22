# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
import commons

class Button(object):
	def __init__(self,position,data):
		self.position=position
		self.size=Vector2(data[4])
		self.background=pygame.surface.Surface(self.size).convert()
		self.background.fill((200,200,200))
		self.content=data[1]
		self.status=False
		self.font=data[0]
		self.message=data[2]
		self.message_font=data[3]
	def display(self,surface):
		surface.blit(self.background,self.position)
		color=(0,0,0)
		info=self.message_font.render(self.message[0],True,(0,0,0))
		if not commons.flags[self.content]:
			color=(255,255,255)
			info=self.message_font.render(self.message[1],True,(0,0,0))
		text=self.font.render(self.content,True,color)
		surface.blit(text,self.position+(self.size-text.get_size())/2)
		if self.status:
			pygame.draw.rect(surface,(0,0,0),(self.position,self.size),2)
			surface.blit(info,commons.screen_size-info.get_size())
	def check(self,position):
		if position[0]<=self.position[0]+self.size[0] and \
		   position[1]<=self.position[1]+self.size[1] and \
		   position[0]>=self.position[0] and position[1]>=self.position[1]:
			self.status=True
		else:
			self.status=False
	def process(self):
		if self.status and commons.flags[self.content]:
			commons.set_world(self.content) #process the function it implies
			#print(commons.current_state)
			
class Menu(object):
	def __init__(self,button_data):
		self.button_list=button_data
		self.buttons={}
		self.nums=len(button_data)		
	def build_buttons(self):
		height=self.nums*60		
		y=(commons.screen_size[1]-height)/2
		for i in range(self.nums):
			if self.button_list[i][1]!='Back':
				x=(commons.screen_size[0]-self.button_list[i][4][0])/2
				position=Vector2(x,y+60*i)
			else:
				position=commons.screen_size-(20,20)-self.button_list[i][4]
			self.buttons[self.button_list[i][1]]=Button(position,self.button_list[i])

	def display(self,surface,cursor):
		self.build_buttons()
		for button in self.buttons.values():
			button.check(cursor)
			button.display(surface)
	def process(self):	
		for button in self.buttons.values():
			if button.status:
				button.process()

class tip_window(Menu):
	def __init__(self,button_data,font):
		super().__init__(button_data)
		self.size=Vector2(220,150)
		self.background=pygame.surface.Surface(self.size).convert()
		self.background.fill((255,255,255))
		self.position=(commons.screen_size-self.size)/2
		self.build_buttons()
		self.font=font
	def build_buttons(self):
		for i in range(self.nums):			
			position=self.position+(110*i+25,100)		
			self.buttons[self.button_list[i][1]]=Button(position,self.button_list[i])
	def display(self,surface,cursor):
		surface.blit(self.background,self.position)
		content=self.font.render('Are you sure?',True,(0,0,0))
		pos=self.position+(self.size-content.get_size())/2-(0,20)
		pygame.draw.rect(surface,(0,0,0),(self.position,self.size),2)
		surface.blit(content,pos)
		for button in self.buttons.values():
			button.check(cursor)
			button.display(surface)
		
	
	
	

	
	
	
