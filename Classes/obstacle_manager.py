import pygame
import random
import math


class ObstacleManager:
    def __init__(self, screen):
        self.screen = screen
        self.obstacle_imgs = []  # Lists to store obstacle info; image, rects, position, change in position, # of obstacles.
        self.obstacle_rects = []
        self.obstacle_x = []
        self.obstacle_y = []
        self.obstacle_x_change = []
        self.obstacle_y_change = []
        num_of_obstacles = 6

        for i in range(num_of_obstacles):  # loop to iterate through each obstacle
            obstacle_img = pygame.image.load('Assets/Obstacles/obstacle.png')
            self.obstacle_imgs.append(obstacle_img)
            self.obstacle_x.append(random.randint(0, 736))  #adds random x,y position to obstacle.
            self.obstacle_y.append(random.randint(50, 150))
            self.obstacle_x_change.append(4)
            self.obstacle_y_change.append(40)
            obstacle_rect = obstacle_img.get_rect()
            obstacle_rect.topleft = (self.obstacle_x[i], self.obstacle_y[i])
            self.obstacle_rects.append(obstacle_rect)

    def update(self):  #updates the position of the obstacles.
        for i in range(len(self.obstacle_rects)):
            self.obstacle_x[i] += self.obstacle_x_change[i]
            if self.obstacle_x[i] <= 0:
                self.obstacle_x_change[i] = 4
                self.obstacle_y[i] += self.obstacle_y_change[i]
            elif self.obstacle_x[i] >= 736:
                self.obstacle_x_change[i] = -4
                self.obstacle_y[i] += self.obstacle_y_change[i]
            self.obstacle_rects[i].topleft = (self.obstacle_x[i], self.obstacle_y[i])

    def draw(self):  #displays the obstacle to the screen
        for i in range(len(self.obstacle_imgs)):
            if i < len(self.obstacle_rects):
                self.screen.blit(self.obstacle_imgs[i], self.obstacle_rects[i].topleft)

    def all_destroyed(self):  #checks if all obstacles are destroyed
        return all(rect is None for rect in self.obstacle_rects)

    def reset(self):  # Reset obstacles not implemented yet
        pass
