from PokeObj import *


class TitleScreen:
    def __init__(self, parent:widgets.Frame):
        self.__scene = parent
        self.__titleState = "Title"

        #Title Screen elements
        self.__titleBG = pygame.image.load(SPRITE_PATH / "TitleScreen.jpg")
        self.__gameLogo = pygame.transform.smoothscale(pygame.image.load(SPRITE_PATH / "PokemonDeltaEmerald.png"), (450, 200))
        self.__scene.parent.blit(self.__gameLogo, ((self.__scene.parent.get_width() / 2) - (self.__gameLogo.get_width() / 2), 0))

        pygame.mixer.music.load(MAIN_MUSICS["TITLETHEME"])
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

        self.__FadeTransition(1, "In")


        #Title menu elements
        self.__mainMenuGame = widgets.GfxButton(self.__scene, 420, 90, pourcentMode=True, centerX=True, posY=15, type="OnClick"\
                                                , buttonLabel="Saves  (actual  game,  in  development)", labelColor=(0, 0, 0), labelSize=25, imageButton=WINDOW_BOX, func=lambda:self.__DialogLoop(["Should  display  saves  and  let  you  load  then  play  with  your  save", "but  it's  still  in  early  development"]))
        self.__mainMenuBattle = widgets.GfxButton(self.__scene, 420, 60, pourcentMode=True, centerX=True, posY=35, type="OnClick"\
                                                  , buttonLabel="Battle  Demo", labelColor=(0, 0, 0), labelSize=25, imageButton=WINDOW_BOX, func=lambda:self.__ChangeGameState("Battle Demo"))
        self.__mainMenuPokedex = widgets.GfxButton(self.__scene, 420, 60, pourcentMode=True, centerX=True, posY=51, type="OnClick"
                                                   , buttonLabel="Pokedex", labelColor=(0, 0, 0), labelSize=25, imageButton=WINDOW_BOX, func=lambda:self.__ChangeGameState("Pokedex"))

        self.__menuButtons = [self.__mainMenuGame, self.__mainMenuBattle, self.__mainMenuPokedex]
        self.__menuSelector = 0




    

    """Public methods"""


    def TitleLoop(self):
        if self.__titleState == "Title":
            self.__TitleScreen()

        elif self.__titleState == "Menu":
            self.__TitleMenu()


        pygame.display.update()



    def GetStates(self):
        return RUNNING, GAME_STATE, GAME_MODE
    



    """Private methods"""


    def __TitleScreen(self):
        global RUNNING, GAME_STATE

        self.__scene.ActiveFrame(activeImage=self.__titleBG)
        self.__scene.parent.blit(self.__gameLogo, ((self.__scene.parent.get_width() / 2) - (self.__gameLogo.get_width() / 2), 0))
        widgets.TextLabel(self.__scene.parent, "@2023 LAPLATEFORME.io", 15, (YEARONE_FONT_PATH), pourcentMode=True, centerX=True, posY=95, color=(210, 210, 210))
        widgets.TextLabel(self.__scene.parent, "Press any key", 20, (YEARONE_FONT_PATH), pourcentMode=True, centerX=True, posY=70, color=(210, 210, 210))
        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                GAME_STATE = None

            if event.type == pygame.KEYDOWN:
                self.__ChangeTitleState("Menu")
    


    def __TitleMenu(self):
        self.__scene.ActiveFrame()

        for buttons in self.__menuButtons:
            buttons.ActiveButton()

        self.__menuButtons[self.__menuSelector].ActiveButton(focused=True)
        

        self.___MenuControls()



    def __ChangeGameState(self, gameMode:str):
        global GAME_STATE, GAME_MODE
        GAME_STATE = "Game"
        GAME_MODE = gameMode



    def __ChangeTitleState(self, newState:str):
        self.__titleState = newState
        self.__FadeTransition(2, "Out")
        
        if self.__titleState == "Title":
            pygame.mixer.music.load(MAIN_MUSICS["TITLETHEME"])
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            self.__FadeTransition(1, "In")

        else:
            pygame.mixer.music.fadeout(1000)   
            self.__scene.fill(self.__scene.get_SurfColor())
            self.__DialogLoop(["Still  in  early  development", "Battle  demo  and  Pokedex  prototype  should  be  available"])     

        pygame.display.update()



    def ___MenuControls(self):
        global RUNNING, GAME_STATE

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                GAME_STATE = None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.__ChangeTitleState("Title")

                if event.key == pygame.K_UP:
                    self.__menuSelector -= 1
                    pygame.mixer.Sound.play(UI_SFX["CURSOR"])

                if event.key == pygame.K_DOWN:
                    self.__menuSelector += 1
                    pygame.mixer.Sound.play(UI_SFX["CURSOR"])

                if event.key == pygame.K_RETURN:
                    self.__menuButtons[self.__menuSelector].Click(input=True)
                    pygame.mixer.Sound.play(UI_SFX["CURSOR"])

                self.__menuSelector = (self.__menuSelector % len(self.__menuButtons))


    def __FadeTransition(self, speed:int, mode:str, fadeColor:tuple=(255, 255, 255)):
        fadeSurf = pygame.Surface(DISPLAY_RES)
        fadeSurf.fill(fadeColor)


        if mode == "Out":
            for alpha in range(0, 300, speed):
                fadeSurf.set_alpha(alpha)

                if self.__titleState == "Title":
                    self.__scene.ActiveFrame()
                else:
                    self.__scene.ActiveFrame(activeImage=self.__titleBG)

                self.__scene.parent.blit(fadeSurf, (0, 0))
                pygame.display.update()

        elif mode == "In":
            for alpha in range(300, 0, -speed):
                fadeSurf.set_alpha(alpha)

                if self.__titleState == "Title":
                    self.__scene.ActiveFrame(activeImage=self.__titleBG)
                else:
                    self.__scene.ActiveFrame()

                self.__scene.parent.blit(fadeSurf, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)


    
    def __DialogLoop(self, texts:list):
        global RUNNING, GAME_STATE

        messageBox = widgets.WindowBox(self.__scene.parent, self.__scene.parent.get_width() - 20, 95, mode="Dialog", windowElements=texts, pourcentMode=True, centerX=True, posY=80, borderOffset=16, imageWindow=pygame.image.load(WINDOW_BOX))
        
        while True:
            if messageBox.EndOfDialog():
                return

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False
                    GAME_STATE = None
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(UI_SFX["CURSOR"])
                        messageBox.NextDialog()


            self.__scene.ActiveFrame()
            messageBox.ActiveWindow()
            pygame.display.update()













class InGame:
    def __init__(self, parent:widgets.Frame, mode:str=GAME_MODE):
        self.__scene = parent
        self.__mode = mode
        self.__scene.parent.blit(self.__scene, (0, 0))

        if self.__mode == "Battle Demo":
            battleBackgrounds = os.listdir(BATTLE_SPRITE_PATH / "IndividualBackgrounds-Gen5")
            battleBG = pygame.image.load(BATTLE_SPRITE_PATH / f"IndividualBackgrounds-Gen5/{random.choice(battleBackgrounds)}").convert_alpha()
            battleMenuBG = pygame.image.load(BATTLE_SPRITE_PATH / "BattleUI/battleMessage.png").convert_alpha()

            pygame.mixer.music.load(MAIN_MUSICS["WILDBATTLE"])
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)

            self.__FadeTransition(2, "Out", fadeColor=(0, 0, 0))

            
            self.__playerPokeToBeOnField = 0
            self.__playersPokemon = []
            registeredIDs = []

            for i in range(6):
                newPokeID = random.randint(1, 386)

                while newPokeID in registeredIDs:
                    newPokeID = random.randint(1, 386)

                registeredIDs.append(newPokeID)
                self.__playersPokemon.append(Pokemon(newPokeID, "english", lvl=random.randint(20, 25)))

            self.__opponent = Pokemon(random.randint(1, 386), "english", lvl=random.randint(10, 35))


            self.__battleField = widgets.Frame(self.__scene, (DISPLAY_W, DISPLAY_H - 100), (0, 0), color=(1, 1, 1), surfImage=battleBG)
            self.__battleMenuFrame = widgets.Frame(self.__scene, (DISPLAY_W, 100), (0, DISPLAY_H - 100), color=(1, 1, 1), surfImage=battleMenuBG)

            self.__possibleActions = []
            self.__focusedButton = []

            self.__BattleIntro([f"A  wild  {self.__opponent.GetName()}  appears !", f"{self.__playersPokemon[self.__playerPokeToBeOnField].GetName()},  GO  !"])



        elif self.__mode == "Pokedex":
            pygame.mixer.music.load(MAIN_MUSICS["POKEDEXFROMTITLE"])
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)

            self.pokemonDisplayed = Pokemon(1, "english")
            print(self.pokemonDisplayed)
        



    """Public methods"""


    def GameLoop(self):

        if self.__mode == "Battle Demo":
            self.__Battle()
        
        elif self.__mode == "Pokedex":
            self.__Pokedex()
    


    def GetStates(self):
        return RUNNING, GAME_STATE
    



    """Private methods"""


    def __Battle(self):
        buttonSpriteSet = pygame.image.load(BATTLE_SPRITE_PATH / "BattleUI/battleCommandButtons.png")
        defaultButtonSprites = widgets.SpriteSheet(self.__battleMenuFrame, buttonSpriteSet, 4, sheetPartSize=(buttonSpriteSet.get_width() / 2), spriteCut=46, spriteSheetOrientation="y")
        focusedButtonSprites = widgets.SpriteSheet(self.__battleMenuFrame, buttonSpriteSet, 4, sheetPartSize=(buttonSpriteSet.get_width() / 2), spriteCut=46, spriteSheetOrientation="y", sheetPartStart=(buttonSpriteSet.get_width() / 2))
        defaultFrames = defaultButtonSprites.GetFrames()
        focusedFrames = focusedButtonSprites.GetFrames()

        pokeMoves = widgets.GfxButton(self.__battleMenuFrame, 130, 46, pourcentMode=True, posX=60, posY=25, type="OnClick", imageButton=buttonSpriteSet, parentImage=True)
        accessBag = widgets.GfxButton(self.__battleMenuFrame, 130, 46, pourcentMode=True, posX=85, posY=25, type="OnClick", imageButton=defaultFrames[1])
        callPokemon = widgets.GfxButton(self.__battleMenuFrame, 130, 46, pourcentMode=True, posX=60, posY=75, type="OnClick", imageButton=defaultFrames[2])
        tryFlee = widgets.GfxButton(self.__battleMenuFrame, 130, 46, pourcentMode=True, posX=85, posY=75, type="OnClick", imageButton=defaultFrames[3])
        

        self.__focusedButton = [[focusedFrames[0], focusedFrames[1]], [focusedFrames[2], focusedFrames[3]]]
        self.__possibleActions = [[pokeMoves, accessBag], [callPokemon, tryFlee]]
        self.__rowFocus, self.__columnFocus = 0, 0

        self.__battleMenuFrame.ChangeBGFrame(pygame.image.load(BATTLE_SPRITE_PATH / "BattleUI/battleCommand.png"))


        while True:
            self.__scene.ActiveFrame()
            self.__battleField.ActiveFrame()
            self.__battleMenuFrame.ActiveFrame()
            widgets.TextLabel(self.__battleMenuFrame, f"What  will  {self.__playersPokemon[self.__playerPokeToBeOnField].GetName()}  do  ?", size=25, font=FONT_PATH, color=(0, 0, 0), pourcentMode=True, posX=20, posY=25)
        
            for row in self.__possibleActions:
                for button in row:
                    button.ActiveButton(unfocusedIsDarker=False)

            self.__possibleActions[self.__rowFocus][self.__columnFocus].ActiveButton(focused=True, unfocusedIsDarker=False, focusedImage=self.__focusedButton[self.__rowFocus][self.__columnFocus])

            if not self.__BattleControls():
                break




            pygame.display.update()



    def __Pokedex(self):
        self.__PokedexControls()

        pygame.display.update()



    def __BattleControls(self):
        global RUNNING, GAME_STATE

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                GAME_STATE = None
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    GAME_STATE = "Title"



    def __PokedexControls(self):
        global RUNNING, GAME_STATE

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
                GAME_STATE = None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    GAME_STATE = "Title"



    def __FadeTransition(self, speed:int, mode:str, fadeColor:tuple=(255, 255, 255)):
        fadeSurf = pygame.Surface(DISPLAY_RES)
        fadeSurf.fill(fadeColor)


        if mode == "Out":
            for alpha in range(0, 300, speed):
                fadeSurf.set_alpha(alpha)

                self.__scene.ActiveFrame()
                '''self.__battleField.ActiveFrame()
                self.__battleMenuFrame.ActiveFrame()'''

                self.__scene.parent.blit(fadeSurf, (0, 0))
                pygame.display.update()

        elif mode == "In":
            for alpha in range(300, 0, -speed):
                fadeSurf.set_alpha(alpha)

                self.__scene.ActiveFrame()
                self.__battleField.ActiveFrame()
                self.__battleMenuFrame.ActiveFrame()

                self.__scene.parent.blit(fadeSurf, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)



    def __BattleIntro(self, texts:list):
        global RUNNING, GAME_STATE

        self.__FadeTransition(1, "In", fadeColor=(0, 0, 0))

        messageBox = widgets.WindowBox(self.__scene, self.__battleMenuFrame.get_width(), self.__battleMenuFrame.get_height(), mode="Dialog", windowElements=texts, textBG=(224, 224, 224), posX=0, posY=self.__battleMenuFrame.get_SurfPos()[1], borderOffset=25, imageWindow=self.__battleMenuFrame.surfImage)
        self.__opponentDisplay = widgets.ImageAnimation(self.__battleField, self.__opponent.GetPokeSprites()["Front"], scale=1.75)
        self.__playerPokeDisplay = widgets.ImageAnimation(self.__battleField, self.__playersPokemon[self.__playerPokeToBeOnField].GetPokeSprites()["Back"], scale=1.75)
        self.__battleFieldEraser = self.__battleField.surfImage

        playerSpriteSheet = widgets.SpriteSheet(self.__battleField, pygame.image.load(BATTLE_SPRITE_PATH / "PlayerInBattle-New.png"), 5, scale=2.5, spriteCut=62)
        
        playerPokePosX = 65
        playerPosX, playerPosY, opponentPosX = playerPokePosX, self.__battleField.get_height() - (playerSpriteSheet.GetSpriteSize()[1] * 2.5), int(self.__battleField.get_width() - playerPokePosX * 3.5)
        posX, opponentCurrentPosX = self.__battleField.get_width(), 0

        playerAnimPlayed, opponentPokeSoundPlayed, playerPokeSoundPlayed, playerPokeOnField = False, False, False, False


        while True:
            if messageBox.EndOfDialog():
                return
            

            if posX > playerPosX:
                posX -= 1
            
            if opponentCurrentPosX < opponentPosX:
                opponentCurrentPosX += 1
            elif not opponentPokeSoundPlayed:
                pygame.mixer.Sound.play(PokemonCries(self.__opponent.GetID()))
                opponentPokeSoundPlayed = True

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False
                    GAME_STATE = None
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(UI_SFX["CURSOR"])
                        
                        if not playerAnimPlayed:
                            posX = playerPosX 
                            playerSpriteSheet.SpriteAnimation((playerPosX, playerPosY), 150, spriteSceneBG=self.__battleFieldEraser, animLoop=False, sceneParent=self.__scene)
                            
                            if not playerPokeSoundPlayed:
                                pygame.mixer.Sound.play(PokemonCries(self.__playersPokemon[self.__playerPokeToBeOnField].GetID()))
                                playerPokeSoundPlayed = True
                            
                            playerPosX = -150
                            opponentCurrentPosX = opponentPosX
                            playerPokeOnField = True
                            playerAnimPlayed = True

                        messageBox.NextDialog()


            self.__scene.ActiveFrame()
            self.__battleField.ActiveFrame()
            self.__battleMenuFrame.ActiveFrame()
            self.__scene.blit(playerSpriteSheet.Get_Image(0, spriteCut=True), (posX, playerPosY))

            if playerPokeOnField:
                self.__playerPokeDisplay.ActiveAnimation((playerPokePosX, self.__battleField.get_height() - 100), 380, spriteSceneBG=self.__battleFieldEraser)
            else:
                self.__battleField.surfImage.blit(self.__battleFieldEraser, (0, 0))
            self.__opponentDisplay.ActiveAnimation((opponentCurrentPosX, 70), 380, spriteSceneBG=self.__battleFieldEraser, animOff=True)
       
            messageBox.ActiveWindow()

            pygame.display.update()



    def __PokeMoves(self):
        return None