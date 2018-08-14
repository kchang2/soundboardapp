import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera

class MainApp(App):
    def build(self):
        return Camera(play=True, index=1, resolution=(640,480))

if __name__== "__main__":
    MainApp().run()