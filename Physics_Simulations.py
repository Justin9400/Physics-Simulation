import sys
import pygame
import pymunk 
import time 
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
grey = (133, 133, 133)
darkGrey = (62, 65, 65)

resolutionX = 1915
resolutionY = 1025
resolution = (resolutionX, resolutionY)
screen = pygame.display.set_mode((resolution), pygame.RESIZABLE)
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

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

def main():
    pygame.init()
    pygame.display.set_caption("Physics Simulation - Justin Kachornvanich") # Title of the window 
    clock = pygame.time.Clock()

    space = pymunk.Space() 
    space.gravity = (0.0, 900.0)

    space.step(1/50.0) 

    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = select_level(screen, player)

        if game_state == GameState.SIMULATION_1:
            game_state = select_level(screen, player)

        if game_state == GameState.SIMULATION_2:
            game_state = select_level(screen, player)

        if game_state == GameState.SIMULATION_3:
            game_state = select_level(screen, player)

        if game_state == GameState.SIMULATION_4:
            game_state = select_level(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return      

def title_screen(screen):
    start_btn = UIElement(
        center_position = (resolutionX/2, resolutionY/2),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Start",
        action = GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position = (resolutionX/2, resolutionY/1.5),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Quit",
        action = GameState.QUIT,
    )
    buttons = RenderUpdates(start_btn, quit_btn)
    return game_loop(screen, buttons)

def select_level(screen, player):
    return_btn = UIElement(
        center_position = (225, 950),
        font_size = 30,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Return to main menu",
        action = GameState.TITLE,
        )
    sim1_btn = UIElement(
        center_position = (600, 400),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Simulation 1",
        action = GameState.SIMULATION_1    
        )
    sim2_btn = UIElement(
        center_position = (600, 700),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Simulation 2",
        action = GameState.SIMULATION_1    
        )
    sim3_btn = UIElement(
        center_position = (1200, 400),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Simulation 3",
        action = GameState.SIMULATION_1    
        )
    sim4_btn = UIElement(
        center_position = (1200, 700),
        font_size = 50,
        bg_rgb = darkGrey,
        text_rgb = white,
        text = "Simulation 4",
        action = GameState.SIMULATION_1    
        )

    buttons = RenderUpdates(return_btn, sim1_btn, sim2_btn, sim3_btn, sim4_btn)

    return game_loop(screen, buttons)

def Simulation_1(screen, player):
    return_btn = UIElement(
        center_position=(225, 950),
        font_size=30,
        bg_rgb=darkGrey,
        text_rgb=white,
        text="Return to main menu",
        action=GameState.TITLE,
        )

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(darkGrey)
        Title_Screen_Header()
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    SIMULATION_1 = 2
    SIMULATION_2 = 3
    SIMULATION_3 = 4
    SIMULATION_4 = 5

def message_display(text):
    smallText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((resolutionX/2), (resolutionY/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(3)

def Title_Screen_Header():
    smallText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Physics Simulation", smallText)
    TextRect.center = ((resolutionX/2), (resolutionY/5))
    screen.blit(TextSurf, TextRect)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

if __name__ == "__main__":
    main()

