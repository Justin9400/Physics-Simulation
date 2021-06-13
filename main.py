import sys
import pygame
import pymunk
import time
import sim1, sim2, sim3, sim4
import constants
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.RESIZABLE)

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)
class Player:
    def __init__(self, score=0, current_level=1):
        self.score = score
        self.current_level = current_level
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    SIMULATION_1 = 2
    SIMULATION_2 = 3
    SIMULATION_3 = 4
    SIMULATION_4 = 5

def main():
    pygame.display.set_caption("Physics Simulation - Justin Kachornvanich") # Title of the window
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0, 900.0)
    space.step(1/50.0)
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.SIMULATION_1:
            game_state = sim1.Simulation_1(screen)
            clear_title(game_state, constants.darkGrey)

        if game_state == GameState.SIMULATION_2:
            game_state = sim2.Simulation_2(screen)

        if game_state == GameState.SIMULATION_3:
            game_state = sim3.Simulation_3(screen)

        if game_state == GameState.SIMULATION_4:
            game_state = sim4.Simulation_4(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()
def title_screen(screen):
    sim1_btn = UIElement(
        center_position = (infoObject.current_w/3.9, infoObject.current_h/2.5),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Simulation 1",
        action = GameState.SIMULATION_1
    )
    sim2_btn = UIElement(
        center_position = (infoObject.current_w/1.35, infoObject.current_h/2.5),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Simulation 2",
        action = GameState.SIMULATION_2
    )
    sim3_btn = UIElement(
        center_position = (infoObject.current_w/3.9, infoObject.current_h/1.5),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Simulation 3",
        action = GameState.SIMULATION_3
    )
    sim4_btn = UIElement(
        center_position = (infoObject.current_w/1.35, infoObject.current_h/1.5),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Simulation 4",
        action = GameState.SIMULATION_4
    )
    quit_btn = UIElement(
        center_position = (infoObject.current_w/2, infoObject.current_h/1.1),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Quit",
        action = GameState.QUIT,
    )
    buttons = RenderUpdates(quit_btn, sim1_btn, sim2_btn, sim3_btn, sim4_btn)
    return game_loop(screen, buttons)
'''
def Simulation_1(screen):
    clear_screen(constants.darkGrey)
    return_btn = UIElement(
        center_position = (constants.menu_button_location),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Menu",
        action = GameState.TITLE,
        )
    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons)
def Simulation_2(screen):
    clear_screen(constants.darkGrey)
    return_btn = UIElement(
        center_position = (constants.menu_button_location),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Menu2",
        action = GameState.TITLE,
        )
    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons)
def Simulation_3(screen):
    clear_screen(constants.darkGrey)
    return_btn = UIElement(
        center_position = (constants.menu_button_location),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Menu3",
        action = GameState.TITLE,
        )
    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons)
def Simulation_4(screen):
    clear_screen(constants.darkGrey)
    return_btn = UIElement(
        center_position = (constants.menu_button_location),
        font_size = 50,
        bg_rgb = constants.darkGrey,
        text_rgb = constants.white,
        text = "Menu4",
        action = GameState.TITLE,
        )
    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons)
    '''
def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(constants.darkGrey)
        Title = Title_Screen_Header()
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()
def message_display(text):
    smallText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((constants.resolutionX/2), (constants.resolutionY/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(3)
def Title_Screen_Header():
    smallText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Physics Simulation", smallText)
    TextRect.center = ((constants.resolutionX/2), (constants.resolutionY/5))
    screen.blit(TextSurf, TextRect)
def text_objects(text, font):
    textSurface = font.render(text, True, constants.white)
    return textSurface, textSurface.get_rect()
def clear_screen(color):
    #while True:
        screen.fill(color)
        pygame.display.flip()
def clear_title(game_state, color):
    if game_state == GameState.SIMULATION_1:
        screen.fill(color)
        pygame.display.flip()

if __name__ == "__main__":
    main()
