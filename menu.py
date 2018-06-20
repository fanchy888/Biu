# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
import commons

class Button(object):
	def __init__(self,position,data):
		self.position=position
		self.size=Vector2(100,40)
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
			#print(commons.current_statu)
			
class Menu(object):
	def __init__(self,button_data):
		self.button_list=button_data
		self.buttons={}
		self.nums=len(button_data)		
	def build_buttons(self):
		height=self.nums*60
		x=(commons.screen_size[0]-100)/2
		y=(commons.screen_size[1]-height)/2
		for i in range(self.nums):
			position=(x,y+60*i)
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

	
	
	
	
	
