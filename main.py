import pandas as pd

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader



# https://kivy.org/docs/api-kivy.uix.tabbedpanel.html
# https://groups.google.com/forum/#!topic/kivy-users/hM-goYwEvwc


# from kivy.uix.gridlayout import GridLayout

# from kivy.core.window import Window
# from kivy.properties import StringProperty
# from kivy.uix.label import Label
# from kivy.config import Config


class Panel(TabbedPanel):
    blist = []
    df = pd.read_table('songs.dat', delimiter=', ')
    sound = None

    def fill_IDs_rnd(self):  

        for i in xrange(self.df['name'].size):
            self.ids["b%i" %i].text = self.df['name'].iloc[i] 
        self.blist = []
        
    def fill_IDs_bbops(self):
        pass

    def play_song(self, id):
        name = id.text
        if self.sound is not None:
            self.sound.stop()
            self.sound = None
        else:
            self.sound = SoundLoader.load('./audio/%s.mp3' %name)
            self.sound.play()


class SoundBoardApp(App): 
    def build(self):
        return Panel()


if __name__ == '__main__':
    SoundBoardApp().run()