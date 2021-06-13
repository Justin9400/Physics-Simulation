import sys
import pygame
import pymunk
import time
import constants
import main
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

def Simulation_1(screen):
    main.clear_screen(constants.darkGrey)
    return_btn = main.UIElement(
        center_position = (constants.menu_button_location),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Menu",
        action = main.GameState.TITLE,
        )
    buttons = RenderUpdates(return_btn)
    return main.game_loop(screen, buttons)