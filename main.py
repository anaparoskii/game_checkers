import pygame
from checkers.variables import WIDTH, HEIGHT
from checkers.board import Board


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    FPS = 60

    main()
