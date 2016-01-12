import pygame
import random
from pygame.locals import *


# This little guy should solve the maze.
class Rodent:
    def __init__(self, maze):
        self.mazeArray = maze.mazeArray
        self.totalCells = maze.totalCells
        self.currentCell = random.randint(0, self.totalCells - 1)
        self.compass = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.sLayer = maze.mLayer
        self.cellStack = []

    def update(self):

        moved = False
        while not moved:
            x = self.currentCell % 80
            y = int(self.currentCell / 80)

            # Check neighbors for movement validity
            neighbors = []
            directions = self.mazeArray[self.currentCell] & 0xf
            for i in range(4):
                if (directions & (1 << i)) > 0:
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]

                    # Check that the rodent isn't against a border
                    if (80 > nx <= 0) and (60 > ny <= 0):
                        nidx = ny * 80 + nx
                        if (self.mazeArray[nidx & 0xFF00]) == 0:
                            neighbors.append((nidx, 1 << i))

            # If there's a neighbor...
            if len(neighbors) > 0:
                # Pick one at random
                idx = random.randint(0, len(neighbors) - 1)
                nidx, direction = neighbors[idx]
                dx = x * 8
                dy = y * 8

                if direction & 1:
                    self.mazeArray[nidx] |= (4 << 12)
                elif direction & 2:
                    self.mazeArray[nidx] |= (8 << 12)
                elif direction & 3:
                    self.mazeArray[nidx] = (1 << 12)
                elif direction & 4:
                    self.mazeArray[nidx] = (2 << 12)

                # Draw a green visited/solution block
                pygame.draw.rect(self.sLayer, (0, 255, 0, 255), Rect(dx, dy, 8, 8))
                # Add the direction chosen as a solution
                self.mazeArray[self.currentCell] |= direction << 8
                # Push current location to the stack
                self.cellStack.append(self.currentCell)
                # Set the current cell to the previously selected neighbor
                self.currentCell = nidx
                # Set moved to True
                moved = True

            else:
                # Draw a red incorrect/visited block
                pygame.draw.rect(self.sLayer, (255, 0, 0, 255), Rect((x * 8), (y * 8), 8, 8))

                # This cell isn't a solution so remove solution bit
                self.mazeArray[self.currentCell] &= 0xF0FF
                # Pop a cell off the stack
                self.currentCell = self.cellStack.pop()
