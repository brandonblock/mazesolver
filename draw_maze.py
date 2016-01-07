import random
import pygame


class DrawMaze:
    def __init__(self, maze_layer, height, width):

        self.height = height
        self.width = width
        self.cells_wide = int(self.width / 8)
        self.cells_tall = int(self.height / 8)
        self.mazeArray = []
        self.state = 'create'
        self.mLayer = maze_layer
        self.mLayer.fill((0, 0, 0, 0))
        self.totalCells = self.cells_wide * self.cells_tall
        self.currentCell = random.randint(0, self.totalCells - 1)
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # Populate the maze layer with a base grid
        for y in range(self.cells_tall):
            pygame.draw.line(self.mLayer, (0, 0, 0, 255), (0, y * 8), (self.width, y * 8))
            for x in range(self.cells_wide):
                self.mazeArray.append(0)
                if y == 0:
                    pygame.draw.line(self.mLayer, (0, 0, 0, 255), (x * 8, 0), (x * 8, self.height))

    def update(self):
        if self.state == 'create':

            # If any cells remain unvisited, keep finding cells
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0
                self.cellStack = []
                self.state = 'solve'
                return
            moved = False

            while moved is False:
                x = self.currentCell % 80
                y = int(self.currentCell / 80)
                neighbors = []

                # Find the neighbors of currentCell that have all walls intact
                for i in range(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    # Check the presence of borders
                    if (self.cells_wide > nx >= 0) and (self.cells_tall > ny >= 0):
                        # Has the cell been visited?
                        if (self.mazeArray[ny * 80 + nx] & 0x000F) == 0:
                            nidx = ny * 80 + nx
                            neighbors.append((nidx, 1 << i))

                # If one of more neighbors w/ cell walls are found
                if len(neighbors) > 0:
                    # Choose a random one to visit next
                    idx = random.randint(0, len(neighbors) - 1)
                    nidx, direction = neighbors[idx]
                    # Remove the wall between the random cell and currentCell
                    dx = x * 8
                    dy = y * 8
                    if direction & 1:
                        self.mazeArray[nidx] |= 4
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx, dy + 1), (dx, dy + 7))
                    elif direction & 2:
                        self.mazeArray[nidx] |= 8
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + 1, dy + 8), (dx + 7, dy + 8))
                    elif direction & 4:
                        self.mazeArray[nidx] |= 1
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + 8, dy + 1), (dx + 8, dy + 7))
                    elif direction & 8:
                        self.mazeArray[nidx] |= 2
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (dx + 1, dy), (dx + 7, dy))
                    # Push currentCell location to cellStack
                    self.cellStack.append(self.currentCell)
                    # Make the new cell currentCell
                    self.currentCell = nidx
                    # Increment visitedCells
                    self.visitedCells += 1
                    moved = True
                # No qualifying neighbors are found
                else:
                    # Pop the last cell from cellStack and make it currentCell
                    self.currentCell = self.cellStack.pop()

    def draw(self, screen):
        screen.blit(self.mLayer, (0, 0))
