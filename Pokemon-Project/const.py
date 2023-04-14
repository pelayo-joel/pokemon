import pygame
import random
import math
import json
import os
from pathlib import Path



pygame.mixer.init()


'''Time/State globals'''

RUNNING = True
GAME_STATE = "Title"
GAME_MODE = ""



'''Path related globals'''

#Assets path
FONT_PATH = Path("./ASSETS/FONTS/pokemon_pixel_font.ttf")
YEARONE_FONT_PATH = Path("./ASSETS/FONTS/yearone.ttf")

SPRITE_PATH = Path("./ASSETS/Sprites")
POKEMON_SPRITE_PATH = Path("./ASSETS/Sprites/Pokedex/")
BATTLE_SPRITE_PATH = Path("./ASSETS/Sprites/BattleSprites/")
UI_PATH = Path("./ASSETS/Sprites/UI/")

MUSIC_PATH = Path("./ASSETS/Sound/Music/")
SFX_PATH = Path("./ASSETS/Sound/SFX/")


#Data path
POKEMON_DATA = Path("./DATA/PokemonData/")
BATTLE_DATA = Path("./DATA/BattleData/")
SAVE_DATA = Path("./DATA/PlayerData/")



'''Resolution/Size globals'''

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 600, 400


#Standard WindowBox

WINDOW_BOX = UI_PATH / "WindowFrames/Frame_4.png"



'''Data related globals'''

#Pokemon Data
with open(POKEMON_DATA / "pokedex-full.json", encoding='utf-8') as pokedex:
    POKEDEX = json.load(pokedex)

with open(POKEMON_DATA / "pokemon_descriptions.json") as descriptions:
    POKE_DESC = json.load(descriptions)

with open(POKEMON_DATA / "Nature.json") as natures:
    NATURES = json.load(natures)

naturesList = list(NATURES.keys())


#XPGroups

XP_GROUPS = {
    "Erratic":[334, 346, 348, 366, 346, 349, 368, 367, 345, 350, 290, 291, 292, 333, 313, 335],
    "Fast":[190, 168, 184, 298, 354, 242, 113, 358, 36, 35, 173, 222, 301, 225, 356, 355, 210, 326, \
            174, 39, 166, 165, 337, 370, 183, 303, 200, 353, 300, 235, 209, 338, 167, 327, 325, 175, 176, \
            40],
    "Slow":[386, 385, 384, 383, 382, 381, 380, 379, 377, 149, 309, 244, 245, 243, 129, 143, 250, 249, 248, \
            144, 145, 146, 148, 59],
    "Fluctuating":[286, 341, 342, 316, 297, 314, 296, 336, 285, 317, 320, 321]
}


#Females id
FEMALE_ID = [3, 12, 19, 20, 25, 41, 42, 44, 45, 64, 65, 84, 85, 97, 111, 112, 118, 119, 123, 129, 130, 154, \
             165, 166, 185, 186, 190, 194, 195, 198, 202, 203, 207, 208, 214, 215, 217, 221, 224, 229, 232, \
                255, 256, 257, 267, 269, 272, 274, 275, 307, 308, 315, 316, 317, 322, 323, 350, 358, 369]


#Battle data
with open(BATTLE_DATA / "Moves.json") as moves:
    MOVES = json.load(moves)

'''with open(BATTLE_DATA / "Items.json") as items:
    ITEMS = json.load(items)'''

with open(BATTLE_DATA / "TypeChart.json") as typeChart:
    TYPE_CHART = json.load(typeChart)

#CRIT_RATES = 


#Save Data
with open(SAVE_DATA / "Saves.json") as saves:
    SAVES = json.load(saves)

with open(SAVE_DATA / "PlayerCurrentData.json") as currentData:
    CURRENT_SAVE = json.load(currentData)



'''Loading sounds in dictionnaries'''

#SFXs
UI_SFX = {}

for sound in os.listdir(SFX_PATH / "UI"):
    UI_SFX.update({sound[:-4].upper():pygame.mixer.Sound(SFX_PATH / f"UI/{sound}")})

'''MOVES_SFX = {}

for sound in os.listdir(SFX_PATH / "Moves"):
    MOVES_SFX.update({sound[:-4].upper():pygame.mixer.Sound(SFX_PATH / f"Moves/{sound}")})'''

'''Loading all pokemons cries in a dictionnary would be a waste considering the sheer number of sounds that there would be to load,
    on top of that, the files name (being IDs) makes it even more convenient to just use a function'''
def PokemonCries(id:int):
    return pygame.mixer.Sound(SFX_PATH / f"Pokedex/{id}.ogg")


#Musics
MAIN_MUSICS = {}

for music in os.listdir(MUSIC_PATH):
    if not os.path.isdir(MUSIC_PATH / music):
        MAIN_MUSICS.update({music[:-4].upper():MUSIC_PATH / music})

LOCATIONS_MUSICS = {}

for music in os.listdir(MUSIC_PATH / "LocationsTheme"):
    LOCATIONS_MUSICS.update({music[:-4].upper():MUSIC_PATH / f"LocationsTheme/{music}"})



'''Stats related globals'''

MAX_EV = 510
MAX_STAT_EV = 255

STAGES_VALUE = {
    "-6":0.25,
    "-5":0.29,
    "-4":0.33,
    "-3":0.4,
    "-2":0.5,
    "-1":0.67,
    "0":1,
    "1":1.5,
    "2":2,
    "3":2.5,
    "4":3,
    "5":3.5,
    "6":4,
}