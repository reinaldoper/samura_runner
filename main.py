import asyncio
import pygame
from src.settings import FPS
from src.game import Game


async def main():
    pygame.init()
    pygame.display.set_caption("Samurai Runner")
    screen = pygame.display.set_mode((900, 500))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    while game.running:
        clock.tick(FPS)
        game._handle_events()
        game._update()
        game._draw()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
