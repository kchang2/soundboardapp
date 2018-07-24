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
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

import cv2
import copy
import time

from face_recognition_kivy import FacialRecognitionMachine

data_path = 'songs.dat'
machine = FacialRecognitionMachine()

# Bill Bridge is genius
# https://stackoverflow.com/questions/40862009/kivy-camera-as-kv-language-widget

# import test as FR

# https://kivy.org/docs/api-kivy.uix.tabbedpanel.html
# https://groups.google.com/forum/#!topic/kivy-users/hM-goYwEvwc


# from kivy.uix.gridlayout import GridLayout

# from kivy.core.window import Window
# from kivy.properties import StringProperty
# from kivy.uix.label import Label
# from kivy.config import Config

class InstructionsNewFacePopup(Popup):
    def __init__(self, **kwargs):
        self.instruction_text = """These are ONE-TIME instructions prior to unlocking this feature. 
Please read over and click on Accept when finished.

NOTE: You must first have the identity of the person in the database.
You cannot add a new person through this method.


To add a new person:
    * Have them remove all items (ie. sunglasses, hat) blocking face.
    * Have them look directly in the camera.
    * Face should be as close to filling the green box as possible.
    * Facial expressions can be varied.

With all the above done, click on Add Face to take images.
When the computer finishes taking photos, click on the person's name.
The computer will then save the photos and re-train the model. """

        super(InstructionsNewFacePopup, self).__init__(**kwargs)

        self.response = None

    def on_answer(self, response):
        self.response = response
        self.dismiss()

class EmployeeListPopup(Popup):
    def __init__(self, **kwargs):
        super(EmployeeListPopup, self).__init__(**kwargs)

        self.df = pd.read_table(data_path, delimiter=', ')
        self.fill_layout()

    def fill_layout(self):
        self.layout = GridLayout(cols=5, padding=5)
        for i in xrange(self.df['name'].size):
            btn = Button(text=self.df['name'].iloc[i], font_size=12)
            btn.bind(on_press=self.select_person)
            self.layout.add_widget(btn)

        self.content = self.layout

    def select_person(self, instance):
        name = instance.text
        popup = Popup(title='Saving Data', content=Label(text='Saving Dataset...'), size_hint=(None, None), size=(200, 200), auto_dismiss=False)
        popup.open()
        Clock.schedule_once(lambda dt: self.machine_add_face(name, popup), 0.1)


    def machine_add_face(self, text, popup):
        machine.addFace(name=text, frame_list=self.face_list)
        popup.dismiss()
        self.dismiss()

class KivyCamera(Image):
    def __init__(self, **kwargs): #, parent, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

        self.running = False

    def onStart(self, capture, fps=20, mode=None):
        if not self.running:
            self.running = True
            self.capture = capture
            self.rate = 1.0 / fps

            if mode is None:
                self.event = Clock.schedule_interval(self.update, self.rate)

            elif mode is 'face':
                self.event = Clock.schedule_interval(self.update_face, self.rate)

            elif mode is 'predict':
                self.event = Clock.schedule_interval(self.update_predict, self.rate)

    def onStop(self):
        if self.running:
            self.running = False
            self.event.cancel()
            self.capture.release()
            self.capture = None

            # face information
            self.face_list = []
            self.face_trigger = False

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            # display image from the texture
            self.texture = image_texture
            self.canvas.ask_update()

    def update_face(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # save image
            if self.face_trigger is True and len(self.face_list) < 42:
                print 'bye'
                self.face_list.append(copy.deepcopy(frame))

            elif self.face_trigger is True:
                self.save_popup.face_list = copy.deepcopy(self.face_list)
                self.save_popup.open()

                # reset face info
                self.face_trigger = False
                self.face_list = []

            # include face triangle
            cv2.rectangle(frame, (100, 40), (540, 440), (0, 255, 0), 2)

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            self.canvas.ask_update()

    def update_predict(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame, p_name, p_conf = machine.predictFrame(frame)
            
            if p_conf < 70:
                self.label.text = '[b][size=24][color=#167ee2]Identification:[/color] %s[/size][/b]' %p_name
                self.play_song(name=p_name)

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            self.canvas.ask_update()

    # def start_face(self):
    #     self.running = False
    #     self.event.cancel()
    #     self.face_trigger = True
    #     self.face_list = []

    #     self.onStart(capture=self.capture, mode='face')

class Panel(TabbedPanel):
    def __init__(self, **kwargs):
        super(Panel, self).__init__(**kwargs)

        self.blist = []
        self.df = pd.read_table(data_path, delimiter=', ')
        self.sound = None

        # self.machine = FR.FacialRecognitionMachine()
        self.capture = None
        self.fps = 20

        # instruct new face popup
        self.instruct_new_face_popup = InstructionsNewFacePopup()

        # saving popup
        self.save_new_face_popup = EmployeeListPopup()
        self.ids.facecam.save_popup = self.save_new_face_popup

        # saving relation of name
        self.ids.facecam.label = self.ids.faceLabel

        # saving music queue <-- future maybe
        # self.music_queue = queue()
        # self.ids.facecam.queue = self.music_queue

        # save relation of save song function
        self.ids.facecam.play_song = self.play_song_auto

        # initial time
        self.last_played_time = time.time()

        # initial ID
        self.current_id = None

    def fill_IDs_rnd(self):
        # stop face cam if it exists
        self.ids.facecam.onStop()

        for i in xrange(self.df['name'].size):
            self.ids["b%i" %i].text = self.df['name'].iloc[i] 
        self.blist = []
        
    def fill_IDs_bbops(self):
        # stop face cam if it exists
        self.ids.facecam.onStop()
        pass

    def initial_camera_setup(self):
        self.capture = cv2.VideoCapture(0)
        self.ids.facecam.onStart(capture=self.capture, fps=self.fps)
        # insert here to reset all modes

    def add_face(self):
        # never even pressed this button before
        if self.instruct_new_face_popup.response is not True:
            self.instruct_new_face_popup.open()
        
        # if not in add face mode
        elif self.ids.predictButton.disabled is False:
            # disable recording
            self.ids.predictButton.disabled = True

            # set up cancel button
            self.ids.cancelButton.text = '[size=24]CANCEL[/size]'
            self.ids.cancelButton.disabled = False

            # change add button setup premise
            self.ids.addButton.text = '[size=24]Take Photo[/size]'

            # stop face cam & re-run with new mode
            self.ids.facecam.onStop()
            self.capture = cv2.VideoCapture(0)
            self.ids.facecam.onStart(capture=self.capture, fps=self.fps, mode='face')

        # in add face mode
        else:
            # self.ids.facecam.start_face() # <-- elegant solution
            self.ids.facecam.face_trigger = True

    def cancel_action(self):
        # currently on face recognition machine
        if self.ids.predictButton.disabled is False:
            # turn off machine + reset button
            self.ids.predictButton.text = '[size=24]RUN[/size]'

            # enable add face feature
            self.ids.addButton.disabled = False

            self.ids.cancelButton.disabled = True
            self.ids.cancelButton.text = ''

        # currently on adding new face controls
        else:
            # close add face features
            self.ids.addButton.text = '[size=24]ADD FACE[/size]'

            # enable run machine button
            self.ids.predictButton.disabled = False

            self.ids.cancelButton.disabled = True
            self.ids.cancelButton.text = ''
        
        # return to original camera view
        self.ids.facecam.onStop()
        self.initial_camera_setup()

    def execute_machine(self):
        # is currently running machine
        if self.ids.addButton.disabled is True:

            # ------ stops playing song, in case mess up ------ #
            if self.sound is not None:
                try:
                    self.sound.stop()
                except:
                    pass

            self.sound = None
            self.current_id = None

            self.ids.faceLabel.text = '[b][size=24][color=#167ee2]Identification:[/color] None[/size][/b]'

            # -------- same as cancel -------- #
            # turn off machine + reset button
            # self.ids.predictButton.text = '[size=24]RUN[/size]'

            # # enable add face feature
            # self.ids.addButton.disabled = False

            # self.ids.cancelButton.disabled = True
            # self.ids.cancelButton.text = ''

            # # return to original camera view
            # self.ids.facecam.onStop()
            # self.initial_camera_setup()
            
        # is not on predict mode
        else:
            # show training model popup
            popup = Popup(title='Training Machine', content=Label(text='Training Machine with dataset...'), size_hint=(None, None), size=(300, 250), auto_dismiss=False)
            popup.open()
            Clock.schedule_once(lambda dt: self.retrain_machine(popup), 0.1)

            # disable recording
            self.ids.addButton.disabled = True

            # set up cancel button
            self.ids.cancelButton.text = '[size=24]CANCEL[/size]'
            self.ids.cancelButton.disabled = False

            # change add button setup premise
            self.ids.predictButton.text = '[size=24]Stop[/size]'

            # stop face cam & re-run with new mode
            self.ids.facecam.onStop()
            self.capture = cv2.VideoCapture(0)
            self.ids.facecam.onStart(capture=self.capture, fps=self.fps, mode='predict')

    def retrain_machine(self, popup):
        # retrain model
        machine.trainModel()
        machine.saveModel()
        popup.dismiss()

    def play_song(self, id):
        name = id.text

        if self.sound is not None:
            try:
                self.sound.stop()
            except:
                pass

            self.sound = None

            if self.current_id != name:
                self.play_song(id)
        else:
            try:
                self.current_id = name
                self.sound = SoundLoader.load('./audio/%s.mp3' %name)
                self.sound.play()
                self.last_played_time = time.time()
            except:
                pass

    def play_song_auto(self, name):
        if self.name not in self.df['name']:
            pass

        elif self.current_id != name or time.time() - self.last_played_time > 15:
            if self.sound is not None:
                try:
                    self.sound.stop()
                except:
                    pass

            self.sound = None
            self.current_id = name
            self.sound = SoundLoader.load('./audio/%s.mp3' %name)
            self.sound.play()
            self.last_played_time = time.time()


    def onExit(self):
        self.capture.release()


class queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class SoundBoardApp(App): 
    def build(self):
        self.icon = './images/scully.ico'
        return Panel()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        try:
            self.root.capture.release()

        except AttributeError:
            pass

        # stop playing music if still exists
        try:
            self.root.sound.stop()
        except:
            pass

if __name__ == '__main__':
    SoundBoardApp().run()