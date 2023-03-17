import Pokemon
from const import *
from widgets import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pokemon Delta Emerald ver.0.0.-20")
        pygame.display.set_icon(pygame.image.load(SPRITE_PATH / "Pokeball-icon.png"))


        self.__DISPLAY = pygame.display.set_mode(DISPLAY_RES)

        self.__TITLE_SCENE = Frame(self.__DISPLAY, DISPLAY_RES, color=(105, 105, 250))
        self.__GAME_SCENE = Frame(self.__DISPLAY, DISPLAY_RES)




    def Run(self):
        global RUNNING, GAME_STATE

        while RUNNING:

            if GAME_STATE == "Title":
                Title = Pokemon.TitleScreen(self.__TITLE_SCENE)

                while GAME_STATE == "Title":
                    Title.TitleLoop()
                    RUNNING, GAME_STATE, GAME_MODE = Title.GetStates()


            elif GAME_STATE == "Game":
                Game = Pokemon.InGame(self.__GAME_SCENE, GAME_MODE)

                while GAME_STATE == "Game":
                    Game.GameLoop()
                    RUNNING, GAME_STATE = Game.GetStates()










if __name__ == "__main__":
    PokemonGame = Game()
    PokemonGame.Run()