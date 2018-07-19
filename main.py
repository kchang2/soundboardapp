import pandas as pd
import os
os.environ['KIVY_AUDIO'] = 'sdl2'

# import cv2

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2


# import test as FR


# https://kivy.org/docs/api-kivy.uix.tabbedpanel.html
# https://groups.google.com/forum/#!topic/kivy-users/hM-goYwEvwc


# from kivy.uix.gridlayout import GridLayout

# from kivy.core.window import Window
# from kivy.properties import StringProperty
# from kivy.uix.label import Label
# from kivy.config import Config




class KivyCamera(Image):
    def __init__(self, parent, capture, fps, **kwargs):
        self.parent = parent
        self.buf = 'http://lmsotfy.com/so.png'
        super(KivyCamera, self).__init__(**kwargs)
        
        self.capture = capture
        self.running = False
        self.rate = 1.0 / fps

    def onStart(self):
        if not self.running:
            self.running = True
            self.event = Clock.schedule_interval(self.update, self.rate)

    def onStop(self):
         if self.running:
            self.running = False
            self.event.cancel()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            # self.parent.ids.camimage = self
            self.load_memory(buf)
            self.parent.ids.camimage.reload()

class Panel(TabbedPanel):
    def __init__(self, **kwargs):
        self.camera = 'http://lmsotfy.com/so.png'

        super(Panel, self).__init__(**kwargs)
        self.blist = []
        self.df = pd.read_table('songs.dat', delimiter=', ')
        self.sound = None

        self.capture = None
        # self.machine = FR.FacialRecognitionMachine()
        self.fps = 20

    def fill_IDs_rnd(self):  
        for i in xrange(self.df['name'].size):
            self.ids["b%i" %i].text = self.df['name'].iloc[i] 
        self.blist = []
        
    def fill_IDs_bbops(self):
        pass

    def initial_setup(self):
        self.capture = cv2.VideoCapture(0)
        self.camera = KivyCamera(parent=self, capture=self.capture, fps=self.fps)
        self.camera.onStart()
        self.ids.camimage.source = self.camera.buf
        # self.ids.camimage.source = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png'
        # self.ids.camimage.reload()
        # print self.ids['camimage']

    def play_song(self, id):
        name = id.text
        if self.sound is not None:
            self.sound.stop()
            self.sound = None
        else:
            self.sound = SoundLoader.load('./audio/%s.mp3' %name)
            self.sound.play()

    def onExit(self):
        self.capture.release()


class SoundBoardApp(App): 
    def build(self):
        self.icon = './images/scully.ico'
        return Panel()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        self.root.capture.release()

if __name__ == '__main__':
    SoundBoardApp().run()