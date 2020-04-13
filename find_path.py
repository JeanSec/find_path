# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:01:58 2020

@author: Jean
"""
import sys
import pygame
from math import sqrt
import random
import collections

FPS = 240
pygame.init()
fpsClock=pygame.time.Clock()
clock = pygame.time.Clock()
background_color = pygame.Color(0, 0, 0, 255)
rocket_color = pygame.Color(255, 255, 255, 255)
point_color = pygame.Color(150, 150, 105, 255)

N = 3
max_gen = 6000
mutation_rate = 0.2
lifespan = 600
start_point = (100,100)
end_point = (900,700)

direction = {0:(1,0),
             1:(-1,0),
             2:(0,-1),
             3:(0,1)}

ordered_direction = collections.OrderedDict(sorted(direction.items()))


 #0 => right
        #1 => left
        #2 => top
        #3 => bottom



def distance(x1,y1, x2,y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)
    
class Rocket:
    def __init__(self, surface):
        self.genome = collections.OrderedDict(sorted({random.randint(0,lifespan):random.randint(0,3)} .items()))
        self.step = 0
        self.score = 0.0
        self.current_position = (0,0)
        self.state = True
        self.rect = pygame.Rect(start_point[0], start_point[1], 10, 10)
        pygame.draw.rect(surface, rocket_color, self.rect)
        self.current_direction = (0,0)

        
    def update_score(self):
        if distance(self.current_position[0], self.current_position[1],
                         end_point[0], end_point[1]) == 0:
            self.score = 1000
        else:
            self.score = (10.0/distance(self.current_position[0], self.current_position[1],
                         end_point[0], end_point[1]))

            
    def move(self, surface):
        if self.state == False:
            self.score = 0
            return False
        new_direction = self.current_direction
        for key in self.genome:
            #print('key=',key)
            if key == self.step:
                new_direction = ordered_direction[self.genome[key]]
                #print('new_direction=',new_direction)
                self.current_direction = new_direction
                #print('step=',self.step)
                break
                
        self.rect = self.rect.move(new_direction[0], new_direction[1])
        self.current_position = (self.rect.x,self.rect.y)
        self.update_score()
        self.step = self.step + 1
        
        if self.rect.x >= surface.get_width() or self.rect.x <= 0:
            self.state = False
        if self.rect.y >= surface.get_height() or self.rect.y <= 0:
            self.state = False
        
    def mutate(self, surface, genome):
        self.genome = genome
        if random.random() <= 0.1:
            random_key = random.randint(0,lifespan)
            random_value = random.randint(0,3)
            self.genome[random_key] = random_value
            self.genome = collections.OrderedDict(sorted(self.genome.items()))
             
        self.score = 0.0
        self.state = True
        self.step = 0
        self.rect = pygame.Rect(start_point[0], start_point[1], 10, 10)
        self.current_position = (0,0)
        self.current_direction = (0,0)
        pygame.draw.rect(surface, rocket_color, self.rect)
        print(self.genome)
        
        
class Map:
    def __init__(self, windowSizeX, windowSizeY):
        self.surface = pygame.display.set_mode((windowSizeX,windowSizeY))
        self.rect_start = pygame.Rect(start_point[0], start_point[1], 20, 20)
        self.rect_end = pygame.Rect(end_point[0], end_point[1], 20, 20)
        self.gen = []
        self.gen_nbr = 0
        self.gen_lifespan = lifespan
        self.creat_gen()
        pygame.draw.rect(self.surface, point_color, self.rect_start)
        pygame.draw.rect(self.surface, point_color, self.rect_end)
        pygame.display.flip()
        
    def creat_gen(self):
        for i in range(N):
            rocket = Rocket(self.surface)
            self.gen.append(rocket)
            
    def find_best_rocket(self):
        score = 0.0
        for rocket in self.gen:
            if rocket.score >= score:
                score = rocket.score
                best_rocket = rocket
        print(best_rocket.score)
        return best_rocket
            
    def step(self):
        if self.gen_lifespan == 0:
            best_rocket = self.find_best_rocket()
            self.gen_nbr = self.gen_nbr+1
            print("_______________")
            print("gen numero = " , self.gen_nbr)
            for rocket in self.gen:
                rocket.mutate(self.surface, best_rocket.genome)
            self.gen_lifespan = lifespan 
            pygame.display.flip()
            fpsClock.tick(FPS)
            return 1
            
        new_gen = []
        self.reset_screen()
        for rocket in self.gen:
            #print(rocket.genome)
            new_rocket = rocket
            new_rocket.move(self.surface)
            pygame.draw.rect(self.surface, rocket_color, new_rocket.rect)
            new_gen.append(new_rocket)
        self.gen = new_gen
        self.gen_lifespan = self.gen_lifespan - 1
        pygame.display.flip()
        fpsClock.tick(FPS)
        return 1
        
    def reset_screen(self):
        self.surface.fill(background_color)
        pygame.draw.rect(self.surface, point_color, self.rect_start)
        pygame.draw.rect(self.surface, point_color, self.rect_end)
        

if __name__ == '__main__':
    game = Map(1000, 800)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        game.step()
