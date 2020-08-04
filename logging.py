import time, _thread
from pybricks.parameters import Color, Button
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

#TODO Logging into Log file
class Logger:
    '''Logging method for CharlieOSX'''
    def __init__ (self, config, fileLocation, brick):
        self.__config = config
        self.__fileLocation = fileLocation
        self.__brick = brick
        self.__refreshScreenNeeded = 0
        self.__sound_lock = _thread.allocate_lock()
    
    def __sound(self, file):
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.__brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))

    def debug(self, method, msg):
        print('TODO: Debug')

    def info(self, method, msg):
        ''' Makes a log output, without showing anything on the EV3 screen'''
        if True:
            ts = time.localtime(time.time())
            print('[%d.%d.%d %d:%d:%d] [Info]' % (ts[2], ts[1], ts[0], ts[3], ts[4], ts[5]), msg)

    def warn(self, method, msg):
        if True:
            ts = time.localtime(time.time())
            print('[%d.%d.%d %d:%d:%d] [Warning]' % (ts[2], ts[1], ts[0], ts[3], ts[4], ts[5]), msg)
        
        if True:
            self.__sound(SoundFile.GENERAL_ALERT)
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/warn.png', transparent = Color.RED)
            self.__brick.screen.draw_text(31, 34, msg, text_color = Color.BLACK)

            if Font.text_width(Font(family = 'arial', size = 7), exception) <= 90:
                self.__brick.screen.draw_text(32, 47, msg, text_color = Color.BLACK)
            elif len(exception) <= 30 * 2:
                msg1, msg2 = msg[:27], msg[27:]
                self.__brick.screen.draw_text(32, 47, msg1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, msg2, text_color = Color.BLACK)
            else:
                msg1, msg2, msg3 = exception[:27], exception[27:53], exception[53:]
                self.__brick.screen.draw_text(32, 47, msg1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, msg2, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 67, msg3, text_color = Color.BLACK)
            
            #wait for user to press middle button
            while not Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/warnSel.png', transparent = Color.RED)
            #wait for user letting button go
            while Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__refreshScreenNeeded = 1

    def error(self, method, msg, exception):
        exception = str(exception)
        if True:
            ts = time.localtime(time.time())
            print('[%d.%d.%d %d:%d:%d] [Error]' % (ts[2], ts[1], ts[0], ts[3], ts[4], ts[5]), msg, exception)
        
        if True:
            self.__sound(SoundFile.GENERAL_ALERT)
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/error.png', transparent = Color.RED)
            self.__brick.screen.set_font(Font(family = 'arial', size = 7))
            if Font.text_width(Font(family = 'arial', size = 7), exception) <= 90:
                self.__brick.screen.draw_text(32, 47, exception, text_color = Color.BLACK)
            elif len(exception) <= 30 * 2:
                exception1, exception2 = exception[:27], exception[27:]
                self.__brick.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
            else:
                exception1, exception2, exception3 = exception[:27], exception[27:53], exception[53:]
                self.__brick.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 67, exception3, text_color = Color.BLACK)
            
            #wait for user to press middle button
            while not Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/errorSel.png', transparent = Color.RED)
            #wait for user letting button go
            while Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__refreshScreenNeeded = 1

    def getScreenRefreshNeeded(self):
        return self.__refreshScreenNeeded
    
    def setScreenRefreshNeeded(self, value):
        self.__refreshScreenNeeded = value