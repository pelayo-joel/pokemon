import widgets
from const import *


class Pokemon:
    def __init__(self, id:int, language:str, lvl:int=1):
        self.__id = id
        self.__DATA = POKEDEX[max(min(self.__id, 386), 1) - 1]
        self.__LVL = min(lvl, 100)
        self.__gender, self.__shiny = "Male", False


        if self.__id in FEMALE_ID:
            self.__gender = random.choice(["Female", "Male"])

        if random.uniform(0.000, 1.000) < 0.012:
            self.__shiny = True

        front1, front2, back1, back2 = self.__SpritePath(self.__id)
        self.__sprites = {
            "Front":[pygame.image.load(front1).convert_alpha(), pygame.image.load(front2).convert_alpha()],
            "Back":[pygame.image.load(back1).convert_alpha(), pygame.image.load(back2).convert_alpha()]
        }


        self.__NATURE = random.choice(naturesList)
        self.__NatureStats = NATURES[self.__NATURE]
        self.__IVs = {  
            "HP":random.randint(0, 31),
            "Attack":random.randint(0, 31),
            "Defense":random.randint(0, 31),
            "Sp. Attack":random.randint(0, 31),
            "Sp. Defense":random.randint(0, 31),
            "Speed":random.randint(0, 31)
        }
        self.__ShinyIVs()

        self.__EVs = {
            "HP":0,
            "Attack":0,
            "Defense":0,
            "Sp. Attack":0,
            "Sp. Defense":0,
            "Speed":0
        }


        self.__name = self.__DATA["name"][language]
        self.__types = self.__DATA["type"]
        self.__baseStats = self.__DATA["base"]
        self.__stats = self.__baseStats
        self.__ScalingStatsByLVL()

        self.__spentEVs = 0


        self.__currentHP = self.__stats["HP"]
        self.__currentXP = 0
        self.__xpRequirements = self.__XpRequirements()

        self.__currentStatStages = {
            "HP":0,
            "Atk":0,
            "SpeAtk":0,
            "Def":0,
            "SpeDef":0,
            "Spd":0
        }

        self.__state = ""


        self.__description = POKE_DESC[str(self.__id)]



    def __str__(self):
        return f"\n    ID: {self.__id}, Name: {self.__name}, \n    Types: {self.__types}, Lvl: {self.__LVL}, \n    Gender: {self.__gender}, Nature: {self.__NATURE}, \n    Shiny: {self.__shiny}\n\n \
        Stats:\n \
            HP: {self.__stats['HP']}\n \
            Atk: {self.__stats['Attack']}, SpeAtk: {self.__stats['Sp. Attack']}\n \
            Def: {self.__stats['Defense']}, SpeDef: {self.__stats['Sp. Defense']}\n \
            Spd: {self.__stats['Speed']}\n"
    



    """Public methods"""


    def Action(self, pokeActionSelection:int):
        return None
    


    def Incur(self, opp):
        self.__Damage()
        self.__Affliction()
        return None
    


    #Getters/Setters methods

    def GetID(self):
        return self.__id
    
    def GetName(self):
        return self.__name
    
    def GetPokeSprites(self):
        return self.__sprites

    def GetPokemonBaseStats(self):
        return self.__baseStats
    
    def GetPokemonCurrentStats(self):
        return self.__stats
    



    """Private methods"""


    def __ShinyIVs(self):
        if self.__shiny:
            for iv in self.__IVs:
                self.__IVs[iv] += 12
                self.__IVs[iv] = min(31, self.__IVs[iv])



    def __Damage(self, opponent:'Pokemon', movePower:int, moveType:str, moveCategory:str, crit:bool):
        if moveCategory == "Physical":
            opponentAtk = opponent["Attack"]
            selfDef = self.__stats["Defense"]

        elif moveCategory == "Special":
            opponentAtk = opponent["Sp. Attack"]
            selfDef = self.__stats["Sp. Defense"]


        burnValue, critMultiplier, multiplierSTAB, typeEffectiveness = 1, 1, 1, 1

        if self.__state == "Burn" and moveCategory == "Physical":
            burnValue = 0.5

        if crit:
            critMultiplier = 2

        if moveType in any(opponent.__types):
            multiplierSTAB = 1.5

        if all(self.__types) in TYPE_CHART[moveType]["EFFECTIVENESS"]:
            typeEffectiveness = 4
        elif any(self.__types) in TYPE_CHART[moveType]["EFFECTIVENESS"]:
            typeEffectiveness = 2
        elif all(self.__types) in TYPE_CHART[moveType]["RESISTANT"]:
            typeEffectiveness = 0.25
        elif any(self.__types) in TYPE_CHART[moveType]["RESISTANT"]:
            typeEffectiveness = 0.5


        DAMAGE = int(math.floor(math.floor((math.floor(((2 * opponent.__LVL) / 5) + 2) * movePower * (opponentAtk / selfDef)) / 50) * burnValue) * critMultiplier * multiplierSTAB * typeEffectiveness)
        if any(self.__types) in TYPE_CHART[moveType]["NULL"]:
            DAMAGE = 1

        self.__currentHP = max((self.__currentHP - DAMAGE), 0)



    def __Affliction(self):
        return None
    


    def __ScalingStatsByLVL(self):
        for stat in self.__stats:
            if stat == "HP":
                self.__stats[stat] = int(math.floor((2 * self.__baseStats[stat] + self.__IVs[stat] + (self.__EVs[stat] * 0.25)) * self.__LVL / 100) + self.__LVL + 10)
            
            else:
                self.__stats[stat] = int(math.floor(math.floor(((2 * self.__baseStats[stat] + self.__IVs[stat] + (self.__EVs[stat] * 0.25)) * self.__LVL / 100) + 5) * self.__NatureStats[stat]))



    def __XpRequirements(self):
        growthType = "Medium Slow"
        xpToNextLVL = 0

        for group in XP_GROUPS:

            if self.__id in XP_GROUPS[group]:
                growthType = group

        
        if growthType == "Erratic":
            if self.__LVL < 50:
                xpToNextLVL = int((self.__LVL ** 3 * (100 - self.__LVL)) / 50)
            elif 50 <= self.__LVL < 68:
                xpToNextLVL = int((self.__LVL ** 3 * (150 - self.__LVL)) / 50)
            elif 68 <= self.__LVL < 98:
                xpToNextLVL = int((self.__LVL ** 3 * math.floor((1911 - 10 * self.__LVL) / 3)) / 500)
            elif 98 <= self.__LVL < 100:
                xpToNextLVL = int((self.__LVL ** 3 * (160 - self.__LVL)) / 100)

        elif growthType == "Fast":
            xpToNextLVL = int((4 * self.__LVL ** 3) / 5)

        elif growthType == "Slow":
            xpToNextLVL = int((5 * self.__LVL ** 3) / 4)

        elif growthType == "Fluctuating":
            if self.__LVL < 15:
                xpToNextLVL = int((self.__LVL ** 3 * (math.floor((self.__LVL + 1) / 3) + 24)) / 50)
            elif 15 <= self.__LVL < 36:
                xpToNextLVL = int((self.__LVL ** 3 * (self.__LVL + 14)) / 50)
            elif 36 <= self.__LVL < 100:
                xpToNextLVL = int((self.__LVL ** 3 * (math.floor(self.__LVL / 2) + 32)) / 50)

        elif growthType == "Medium Slow":
            xpToNextLVL = int((6 / 5 * self.__LVL ** 3) + (15 * self.__LVL ** 2) + 100 * self.__LVL - 40)


        return xpToNextLVL



    def __SpritePath(self, id:int):
        FrontPath1, FrontPath2, BackPath1, BackPath2 = '', '', '', ''

        if self.__gender == "Female" and self.__shiny:
            FrontPath1 = POKEMON_SPRITE_PATH / f"shiny/{id}.png"
            FrontPath2 = POKEMON_SPRITE_PATH / f"shiny/frame2/{id}.png"
            BackPath1 = POKEMON_SPRITE_PATH / f"back/shiny/female/{id}.png"
            BackPath2 = POKEMON_SPRITE_PATH / f"back/shiny/female/frame2/{id}.png"

        elif self.__gender == "Female":
            FrontPath1 = POKEMON_SPRITE_PATH / f"{id}.png"
            FrontPath2 = POKEMON_SPRITE_PATH / f"frame2/{id}.png"
            BackPath1 = POKEMON_SPRITE_PATH / f"back/female/{id}.png"
            BackPath2 = POKEMON_SPRITE_PATH / f"back/female/frame2/{id}.png"

        elif self.__shiny:
            FrontPath1 = POKEMON_SPRITE_PATH / f"shiny/{id}.png"
            FrontPath2 = POKEMON_SPRITE_PATH / f"shiny/frame2/{id}.png"
            BackPath1 = POKEMON_SPRITE_PATH / f"back/shiny/{id}.png"
            BackPath2 = POKEMON_SPRITE_PATH / f"back/shiny/frame2/{id}.png"

        else:
            FrontPath1 = POKEMON_SPRITE_PATH / f"{id}.png"
            FrontPath2 = POKEMON_SPRITE_PATH / f"frame2/{id}.png"
            BackPath1 = POKEMON_SPRITE_PATH / f"back/{id}.png"
            BackPath2 = POKEMON_SPRITE_PATH / f"back/frame2/{id}.png"

        return FrontPath1, FrontPath2, BackPath1, BackPath2
    









class Player:
    def __init__(self) -> None:
        pass










class Map:
    def __init__(self) -> None:
        pass



        """Translate coordinates to 1D list (needed for tilemaps data in 'map.json' that are stored in 1D lists)"""


        #Coordinates to 1D list index
        '''
        mapWidth = 50
        index = y * mapWidth + x'''

        #Reverse (1D -> coordinates)
        '''x = i % mapWidth'''
        '''y = i / mapWidth'''










