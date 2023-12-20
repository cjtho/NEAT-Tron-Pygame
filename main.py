import pygame
import sys
from state_manager import StateManager
from main_menu import MenuScreen
from pregame import Pregame
from game_pvp import GamePlayerVsPlayer
from game_ai_train import GameAITraining
from game_ai import GamePlayerVsAI, GameAIVsAI

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

width = int(0.79 * screen_width)
height = int(0.823 * screen_height)

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tron")

clock = pygame.time.Clock()

sm = StateManager(screen, clock)
sm.add_state("menu", MenuScreen)
sm.add_state("pregame", Pregame)
sm.add_state("pvp", GamePlayerVsPlayer)
sm.add_state("ai_training", GameAITraining)
sm.add_state("pvai", GamePlayerVsAI)
sm.add_state("aivai", GameAIVsAI)
sm.set_state("menu")

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        sm.handle_event(event)

    sm.draw()
    sm.update()

    pygame.display.update()
    clock.tick(60)
