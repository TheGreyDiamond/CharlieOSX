import _thread, time

from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI.UIObject import UIObject
from UI.tools import Menu, Box


class UIManager:
    """
        Basicly a Menu
    """

    def __init__(self, config, settings, brick, logger, settingsPath):
        # general variable setup
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.__settingsPath = settingsPath
        self.brick = brick
        self.logger = logger
        #self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()

        # Main Menu
        self.mainMenu = Menu('sidebar')
        mainPages = [
            "assets/graphics/menus/programming.png",
            "assets/graphics/menus/testing.png",
            "assets/graphics/menus/remote.png",
            "assets/graphics/menus/competition.png",
            "assets/graphics/menus/settings.png",
        ]
        for i in range(len(mainPages)):
            name = mainPages[i].split('/')[3].split('.')[0]
            self.mainMenu.addObject(UIObject(name, self.brick, Box(0, i, 30, 25), 'img', (0, 0, True), mainPages[i]))

        # Programming Menu
        self.programming = Menu('list')

        # Testing Menu
        self.testing = Menu('list')

        # Remote-Control Menu
        self.remote = Menu('canvas')

        # Competition-Mode Menu
        self.competition = Menu('canvas')

        # Settings Menu
        self.settingsMenu = Menu('dict')

        # menu Variables
        self.loop = True        
        self.currentMenu = self.mainMenu
        self.position = [0, 0]
        self.subMenus = [
            self.programming,
            self.testing,
            self.remote,
            self.competition,
            self.settingsMenu
        ]
        # testSubmenu = Menu('normal')
        # testSubmenu.addObject(UIObject('testObject1', self.brick, Box(0, 85, 20, 20), 'img', (0, 0), 'assets/graphics/menus/settingsMainMenu.png'))
        # testSubmenu.addObject(UIObject('testObject2', self.brick, Box(0, 5, 20, 20), 'img', (0, 0), 'assets/graphics/menus/programmingMainMenu.png'))
        # testSubmenu.addObject(UIObject('testObject3', self.brick, Box(40, 5, 20, 20), 'img', (0, 0), 'assets/graphics/menus/programmingMainMenu.png'))
        # print(testSubmenu.rasterize())

        #self.logger.info(self, 'UI initialized')

    def __sound(self, file):
        '''
        This private method is used for playing a sound in a separate thread so that other code can be executed simultaneously.

        Args:
            file (str / SoundFile): The path to the soundfile to play
        '''
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))

    def addObject(self, UIObject):
        self.UIObjects.append(UIObject)

    def draw(self):
        for UIObject in self.UIObjects:
            UIObject.draw()

    def mainLoop(self):
        while self.loop:
            self.update()

    def update(self):
        # for UIObject in self.UIObjects:
        #     UIObject.update()

        if self.brick.buttons.pressed():
            self.brick.screen.clear()
            self.checkButtons()
            self.draw()

    def checkButtons(self):
        # print("Current Icon: " + str(self.currentObject))

        if Button.DOWN in self.brick.buttons.pressed():
            if not self.currentObject == len(self.UIObjects) - 1:
                self.changeCurrentObj(1)
        elif Button.UP in self.brick.buttons.pressed():
            if not self.currentObject == 0:
                self.changeCurrentObj(-1)

    def changeCurrentObj(self, num):
        self.UIObjects[self.currentObject].selected = False
        self.currentObject += num
        self.UIObjects[self.currentObject].selected = True
