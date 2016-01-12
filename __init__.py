import pygame
from pygame.locals import *
from draw_maze import DrawMaze
from maze_solver import Rodent

height = 480
width = 640


def main():
    pygame.init()

    # Create a new screen from the pygame.display, and set the mode to 640x480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("be aMAZEd!")
    pygame.mouse.set_visible(0)

    # Declares our background as a pygame surface
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    # Declares a second layer for drawing the maze
    maze_layer = pygame.Surface(screen.get_size())
    maze_layer = maze_layer.convert_alpha()
    maze_layer.fill((0, 0, 0, 0))

    # Instantiates the drawn maze object
    new_maze = DrawMaze(maze_layer, height, width)
    new_rodent = Rodent(new_maze)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()

    while True:

        clock.tick(480)

        # Grab events from the event list and quit if necessary
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        if new_maze.state == "create":
            new_maze.update()

        elif new_maze.state == "solve":
            new_rodent.update()

        screen.blit(background, (0, 0))
        new_maze.draw(screen)
        pygame.display.flip()


# Python calls for __main__ in the __name__ so we tell it to call main()
if __name__ == "__main__":
    main()
