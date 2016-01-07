import pygame
import random


# This little guy should solve the maze.
class Rodent:
    def __init__(self, maze):
        self.maze = maze

    def update(self):
        if self.maze.state == "solve":
            print("Ready to solve!")
