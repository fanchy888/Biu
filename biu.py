# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
from FSM import *
import random
import commons

#the state of the game
#story mode:each chapter includes a boss some enemies and a waiting period
class pushing(State):
	def __init__(self,world):
		super().__init__('pushing')
		self.world=world
	def check(self):
		if self.world.time<=self.world.current_chapter.time+3:
			return 'pushing'
		else:	
			return 'boss'
	def run(self):
		if self.world.time<=self.world.current_chapter.time:
			self.world.generate_enemy()
	def start(self):
		self.world.time=0
		self.world.status=False
		self.world.change_chapter()
		self.world.initial_enemy()
		self.world.champ.fire=True	
		bgm=self.world.current_chapter.bgm
		pygame.mixer.music.load(bgm)
		pygame.mixer.music.play(-1,0.0)
#boss appears		
class last_enemy(State):
	def __init__(self,world):
		super().__init__('boss')
		self.world=world
	def start(self):
		self.world.injert_boss()
	def check(self):
		if self.world.boss.hp<=0:
			return 'complete'
		else:
			return 'boss'
class complete(State):
	def __init__(self,world):
		super().__init__('complete')
		self.world=world
	def check(self):		
		if self.world.time>=3:
			if commons.mode[1]<len(self.world.chapters)-2:
				return 'pushing'
			else:
				return 'congrats'
		else:
			return 'complete'
	def start(self):
		self.world.time=0 
		self.world.bullets={}
		self.world.clear=True
		id=commons.mode[1]+1
		commons.flags[self.world.chapters[id].id]=True
		pygame.mixer.music.stop()
		pygame.mixer.music.load('sounds\\preview.ogg')
		pygame.mixer.music.play()
	def run(self):
		commons.user[0]=self.world.champ.exp
		commons.user[1]=self.world.champ.speed
		commons.user[2]=self.world.champ.hp
		commons.user[3]=self.world.champ.init_guncd
		commons.user[4]=self.world.champ.guns
		commons.user[5]=self.world.champ.level
		commons.user[6]=self.world.champ.score
	def stop(self):
		commons.mode[1]+=1
		self.world.clear=False
		pygame.mixer.music.stop()
#complete all chapters and the ending script
class congrats(State):
	def __init__(self,world):
		super().__init__('congrats')
		self.world=world
	def start(self):
		self.world.time=0
		self.world.champ.fire=False		
		self.world.champ.speed=200
		commons.flags['Endless']=True
		commons.user[2]=commons.user[5]*10+100		
	def check(self):
		if self.world.time>=3:
			return 'gameover'
		else:
			return 'congrats'
	def run(self):
		self.world.champ.direction=Vector2(0,-1)
		if self.world.champ.position[1]<-100:
			self.world.champ.speed=0
		else:
			self.world.champ.speed+=0.5
		if self.world.pannel.position[1]<=commons.screen_size[1]:
			self.world.pannel.speed=50
		else:
			self.world.pannel.speed=0
	def stop(self):
		self.world.status=True
		self.world.time=0	
		commons.s_change=True
#the credits			
class ending_script(State):
	def __init__(self,world):
		super().__init__('scripts')
		self.world=world
	def start(self):
		pass
	def check(self):
		if self.world.time>=50:
			commons.s_change=True
			return 'gameover'
		return 'scripts'
	
#endless mode:Never end
class endless(State):
	def __init__(self,world):
		super().__init__('endless')
		self.world=world
	def check(self):
		if self.world.champ.hp<=0:
			return 'gameover'
		else:
			return 'endless'
	def start(self):
		self.world.time=0
		self.world.change_chapter()
		self.world.initial_enemy()
		self.world.champ.reset()
	def run(self):
		self.world.generate_enemy()
		commons.user[6]=self.world.champ.score
#has nothing to do,keep idle
class gameover(State):
	def __init__(self,world):
		super().__init__('gameover')
		self.world=world	
	def start(self):
		self.world.time=0


#entity, contains all game entities and all the game factors like chapter infos	
class World(object):
	def __init__(self,size,enemy_list,font):
		self.size=size
		self.font=font
		self.entities={}
		self.bullets={}
		self.champ=None
		self.chapters=[]
		self.bullet_id=0
		self.entity_id=0
		self.background=pygame.surface.Surface(commons.screen_size).convert()
		self.background.fill((200,255,255))
		self.enemy_freq={}
		self.enemy_list=enemy_list
		self.boss=None
		self.status=False #pass or not
		self.FSM=FSM()
		self.time=0
		self.current_chapter=None
		self.clear=False
		self.FSM.add_state(pushing(self))
		self.FSM.add_state(last_enemy(self))
		self.FSM.add_state(complete(self))
		self.FSM.add_state(endless(self))
		self.FSM.add_state(gameover(self))
		self.FSM.add_state(congrats(self))
		self.check_point=0
		self.pannel=None
	#reset the world before a new game	
	def reset(self):
		self.status=False
		self.FSM.change_state(commons.mode[0])
		self.entities={}
		self.bullets={}
		if self.current_chapter.id=='Endless':
			self.champ.reset()
		else:
			self.champ.reload()
		self.bullet_id=0
		self.entity_id=0
		self.status=False
		self.pannel.reset()
	#add and delete the characters to the world
	def add_pannel(self,pannel):
		self.pannel=pannel
	def add_champ(self,champ):
		self.champ=champ
	def add_entity(self,entity):
		self.entities[self.entity_id]=entity
		entity.id=self.entity_id
		self.entity_id+=1
	def add_bullet(self,bullet):
		self.bullets[self.bullet_id]=bullet
		bullet.id=self.bullet_id
		self.bullet_id+=1
	def add_chapter(self,chapter):
		self.chapters.append(chapter)
	def change_chapter(self):
		self.current_chapter=self.chapters[commons.mode[1]]
	def injert_boss(self):
		boss_data=self.current_chapter.boss_data		
		self.boss=Boss(self,boss_data)
		self.add_entity(self.boss)
	def delete_entity(self,id):
		del self.entities[id]
	def delete_bullet(self,id):
		del self.bullets[id]
		
	#like it says	
	def process(self,time):
		time_tick=time/1000.0
		self.time+=time_tick
		for i in self.current_chapter.enemy:
			self.enemy_freq[i[0]]-=time_tick
		entities=self.entities.copy()
		bullets=self.bullets.copy()
		if not self.champ.dead and not self.status:
			self.champ.process(time_tick)
			for key in entities.keys():
				self.entities[key].process(time_tick)
			for key in bullets.keys():
				self.bullets[key].process(time_tick)			
			self.FSM.think()	
		self.pannel.process(time_tick)
	def display(self,surface):
		surface.blit(self.background,(0,0))
		for entity in self.entities.values():
			entity.display(surface)
		for bullet in self.bullets.values():
			bullet.display(surface)
		self.champ.display(surface)
		#display the clearance messages
		if self.clear:
			message=self.font.render(str(self.current_chapter.id)+" completed",True,(150,150,150))
			position=(self.size-message.get_size())/2
			if (self.time%3>0.5):
				surface.blit(message,position)
		self.pannel.display(surface)		
	def generate_enemy(self):
		for i in self.current_chapter.enemy:
			id=i[0]
			freq=i[1]
			if self.enemy_freq[id]<=0:
				y=0-self.enemy_list[id][0].get_height()
				#story mode
				if self.current_chapter.id is not 'Endless':
					x=random.randint(0,self.size[0]-self.enemy_list[id][0].get_width())
					position=Vector2(x,y)
					self.add_entity(enemy(self,position,self.enemy_list[id]))
				#endless mode
				else:
					num=int(self.size[0]/self.enemy_list[-1][0].get_width())
					temp=random.randint(0,4)
					for i in range(num):
						self.enemy_list[-1][2]=1+random.randint(int(self.time/2.5),int(self.time/2.5)+10)						
						if temp==i:
							self.enemy_list[-1][2]=1+int(self.time/8)
						self.enemy_list[-1][3]=self.enemy_list[-1][2]*3
						x=0+i*self.enemy_list[-1][0].get_width()
						position=Vector2(x,y)
						self.add_entity(Brick(self,position,self.enemy_list[-1]))	
						freq=self.current_chapter.enemy[0][1]-self.champ.level*0.3
				self.enemy_freq[id]=freq
	def initial_enemy(self):
		self.enemy_freq={}
		for i in self.current_chapter.enemy:
			self.enemy_freq[i[0]]=i[1]

#the main character			
class Plane(object):
	def __init__(self,world,data):
		self.image=data[0]
		self.weapon_image=data[1]
		self.startpoint=Vector2((commons.world_size[0]-data[0].get_width())/2,commons.world_size[1]-data[0].get_height())
		self.position=self.startpoint
		self.dead=False		
		self.direction=Vector2(0,0)
		self.fire=True
		self.world=world
		self.id=0
		self.name='plane'
		self.points=0
		self.load()
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
			self.dead=True
		#check exp
		if self.exp>=100*(self.level):
			self.exp=100*(self.level)
			if self.level<=9:
				self.Level_up()
	#auto fire	
	def Fire(self):
		if self.fire and self.gun_cd<=0:
			self.shoot()
			self.gun_cd=self.init_guncd
	#generate the bullets in the world
	def shoot(self):
		lenth=max(self.image.get_width()/self.guns,20)
		fire_range=lenth*self.guns
		first_gun=self.position-((fire_range-self.image.get_width())/2,0)
		for i in range(self.guns):			
			shift=(lenth-self.weapon_image.get_width())/2+lenth*i
			gun_position=first_gun+(shift,0)
			bullet=ammo(self.weapon_image,self.world,gun_position)
			self.world.add_bullet(bullet)
	#unfinished yet
	def Level_up(self):		
		self.level+=1
		self.exp=0
		self.speed=self.level*20+200
		self.hp+=10
		self.init_guncd=self.init_guncd*0.9
		self.guns=self.level//3+1		
	def process(self,time):
		self.check()
		self.Fire()
		self.move(time)
		self.gun_cd-=time
	def display(self,surface):
		surface.blit(self.image,self.position)
	#reload the user data after dead or exit
	def reload(self):
		self.direction=Vector2(0,0)
		self.dead=False
		self.fire=True
		self.position=self.startpoint
		self.load()
	def load(self):
		self.exp=commons.user[0]
		self.speed=commons.user[1]
		self.hp=commons.user[2]
		self.init_guncd=commons.user[3]
		self.guns=commons.user[4]
		self.level=commons.user[5]
		self.score=commons.user[6]
		self.gun_cd=self.init_guncd
	#reset to initial state for endless mode
	def reset(self):
		self.direction=Vector2(0,0)
		self.exp=0
		self.speed=200
		self.hp=100
		self.init_guncd=0.2
		self.guns=1
		self.level=1
		self.position=self.startpoint
		self.dead=False
		self.fire=True
		self.points=0
#the ammo from the champ		
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
					self.world.entities[enemy.id].hp=max(0,self.world.entities[enemy.id].hp-self.damage)
					self.world.champ.points+=self.damage
					break
	
# the enemy 	
class enemy(object):
	def __init__(self,world,position,data):
		self.name='enemy'
		self.id=-1
		self.world=world
		self.image=data[0]
		self.speed=data[1]#random.randint(data[1],data[1]+100)
		self.position=position	
		self.hp=data[2]
		self.target=self.world.champ
		self.exp=data[3]
		self.score=data[4]
		self.damage=data[5]
	def move(self,time):
		self.position[1]+=self.speed*time 
	def check(self):
		if self.position[1]>=self.world.size[1]:
			self.world.delete_entity(self.id)
		if self.position[1]+self.image.get_height()/2>self.target.position[1] and \
		   self.position[1]<self.target.position[1]+self.target.image.get_height()/3*2 and \
		   self.position[0]>self.target.position[0]-self.image.get_width()/3*2 and \
		   self.position[0]<self.target.position[0]+self.target.image.get_width()-self.image.get_width()/3:
			self.target.hp-=self.damage
			self.hp=0
		if self.hp<=0:
			self.hp=0
			self.world.delete_entity(self.id)
			self.target.score+=self.score
			self.target.exp+=self.exp
			
	def display(self,surface):
		surface.blit(self.image,self.position)	
	def process(self,time):
		self.check()
		self.move(time)	

#the boss of a chapter
class Boss(object):
	def __init__(self,world,data):
		self.name='enemy'
		self.world=world
		self.image=data[0]
		self.weapon_image=data[1]
		self.speed=100
		y=0-self.image.get_height()
		x=(world.size[0]-self.image.get_width())/2
		self.position=Vector2(x,y)
		self.destination=Vector2(x,200)
		self.id=-1
		self.hp=data[2]
		self.score=data[3]
		self.exp=data[4]
		self.state=False
		self.gun_cd=data[5]

	def move(self,time):
		dir=self.destination-self.position
		dir.unit()
		self.position+=self.speed*time*dir
	def check(self):
		if self.position[1]>=100 and not self.state:
			self.state=True	
			self.destination=Vector2(self.world.size[0],self.position[1])	
		if self.position[0]<=10:
			self.destination=Vector2(self.world.size[0],self.position[1])	
		if self.position[0]>=self.world.size[0]-self.image.get_width()-10:
			self.destination=Vector2(0,self.position[1])
		if self.hp<=0:
			self.world.delete_entity(self.id)
			self.world.champ.exp+=self.exp
			self.world.champ.score+=self.score
			
	def Fire(self):
		if self.state and self.gun_cd<=0:
			self.shoot()
			self.gun_cd=1
	def shoot(self):
		x=self.position[0]+self.image.get_width()/2
		y=self.position[1]+self.image.get_height()
		bullet=Enemy_ammo(self.weapon_image,self.world,Vector2(x,y))
		self.world.add_bullet(bullet)
	def process(self,time):
		self.check()
		self.Fire()
		self.move(time)
		self.gun_cd-=time
	def display(self,surface):
		surface.blit(self.image,self.position)	

#ammo from boss		
class Enemy_ammo(ammo):
	def __init__(self,image,world,position):
		self.image=image
		self.position=position
		self.world=world
		self.id=0
		self.name='biu'
		self.damage=10
		self.speed=100
	def move(self,time):
		self.position+=self.speed*Vector2(0,1)*time
	def check(self):
		if self.position[1]>=self.world.size[1]:
			self.world.delete_bullet(self.id)
		else:
			self.hit()		
	def display(self,surface):
		surface.blit(self.image,self.position)	
	def process(self,time):
		self.check()
		self.move(time)
	def hit(self):
		if self.position[0]>=self.world.champ.position[0] and \
		   self.position[0]<=self.world.champ.position[0]+self.world.champ.image.get_width()-self.image.get_width() and \
		   self.position[1]>=self.world.champ.position[1] and \
		   self.position[1]<=self.world.size[1]-self.image.get_height():
			self.world.delete_bullet(self.id)
			self.world.champ.hp-=self.damage

#endless mode enemy			
class Brick(enemy):
	def __init__(self,world,position,data):
		super().__init__(world,position,data)
		self.font=data[6]
	def display(self,surface):
		super().display(surface)
		hp=self.font.render(str(self.hp),True,(0,0,0))
		x=(self.image.get_width()-hp.get_width())/2
		y=(self.image.get_height()-hp.get_height())/2		
		surface.blit(hp,self.position+(x,y))
			
# a chapter class			
class Chapter(object):
	def __init__(self,id,bgm,boss_data,time,enemy_data):
		self.id=id
		self.bgm=bgm
		self.time=time
		self.enemy=enemy_data
		self.boss_data=boss_data


#the panel show the infos of champs		
class pannel(object):
	def __init__(self,world,pannel_font,size):
		self.size=size
		self.background=pygame.surface.Surface(size).convert()
		self.background.fill((255,255,255))
		self.position=world.size-(world.size[0],0)
		self.world=world
		self.font=pannel_font
		self.speed=0
	def process(self,time):
		self.position+=self.speed*time*Vector2(0,1)
	def display(self,surface):
		surface.blit(self.background,self.position)
		pygame.draw.rect(surface,(0,0,0),(self.position,self.size),2)
		score=self.font.render('Coins:'+str(self.world.champ.score),True,(0,0,0))
		Hp=self.font.render('HP:'+str(self.world.champ.hp),True,(0,0,0))
		Level=self.font.render('Level:'+str(self.world.champ.level),True,(0,0,0))		
		surface.blit(Hp,self.position)
		surface.blit(score,self.position+(220,0))		
		surface.blit(Level,self.position+(0,50))
		if self.world.current_chapter.id !='Endless':
			Stage=self.font.render(str(self.world.current_chapter.id),True,(0,0,0))
			surface.blit(Stage,self.position+(220,50))
		else:
			Points=self.font.render('Score:'+str(self.world.champ.points),True,(0,0,0))	
			surface.blit(Points,self.position+(220,50))
		exp_bar=self.position+(Level.get_width(),50)+(3,3)
		pygame.draw.rect(surface,(0,0,0),(exp_bar,(80,20)),2)
		pygame.draw.rect(surface,(0,0,0),(exp_bar,(self.world.champ.exp/self.world.champ.level*80/100,20)),0)
	def reset(self):
		self.position=self.world.size-(self.world.size[0],0)
		self.speed=0