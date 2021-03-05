import random
import time
import itertools

class guitar:
    def __init__(self):
        self.chords = []
        self.chords_basic = ['A', 'C', 'D', 'E', 'G', 'Cadd9']
    def add_chord(self,chord):
        if isinstance(chord, list):
            for ch in chord:
                if ch in self.chords_basic:
                    if ch in self.chords:
                        print("Chord already added.")
                    else:
                        self.chords.append(chord)
                else:
                    print("Add a valid chord.")
        elif isinstance(chord, str):
            if chord in self.chords_basic:
                if chord in self.chords:
                    print("Chord already added.")
                else:
                    self.chords.append(chord)
            else:
                print('Add a valid chord.')
        else:
            print("Add a valid chord.")
    def print_chords(self):
        print(self.chords)
    def training(self, length, pause):
        if isinstance(length, int) and isinstance(pause,float) or isinstance(pause,int):
            for i in range(length):
                print(random.choice(self.chords))
                print("_\n")
                time.sleep(pause)
        else:
            print("Incorrect length or pause.")

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.sel_chords = []
        self.time = 0

        self.cols = 1
        self.add_widget(Label(text="Please, select the chords you would like to practise."))

        self.intro = StackLayout()

        self.A = ToggleButton(text="A", size_hint=(.2, .2))
        self.intro.add_widget(self.A)

        self.E = ToggleButton(text="E", size_hint=(.2, .2))
        self.intro.add_widget(self.E)

        self.C = ToggleButton(text="C", size_hint=(.2, .2))
        self.intro.add_widget(self.C)

        self.D = ToggleButton(text="D", size_hint=(.2, .2))
        self.intro.add_widget(self.D)

        self.G = ToggleButton(text="G", size_hint=(.2, .2))
        self.intro.add_widget(self.G)

        self.Cadd9 = ToggleButton(text="Cadd9", size_hint=(.2, .2))
        self.intro.add_widget(self.Cadd9)
        self.add_widget(self.intro)

        self.outro = GridLayout(cols=3)
        self.outro.add_widget(Label(text="Seconds per chord:"))
        self.minutes = TextInput(multiline=False)
        self.outro.add_widget(self.minutes)
        self.submit = Button(text="Accept", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.outro.add_widget(self.submit)
        self.add_widget(self.outro)

    def pressed(self, instance):
        self.sel_chords =[]

        if self.A.state == "down":
            self.sel_chords.append("A")
        if self.C.state == "down":
            self.sel_chords.append("C")
        if self.D.state == "down":
            self.sel_chords.append("D")
        if self.E.state == "down":
            self.sel_chords.append("E")
        if self.G.state == "down":
            self.sel_chords.append("G")
        if self.Cadd9.state == "down":
            self.sel_chords.append("Cadd9")
        try:
            self.time = int(self.minutes.text)
        except:
            self.time = 1

        next_screen = App.get_running_app().root.get_screen("new_screen").children[0]
        next_screen.start(self.sel_chords, self.time)


class MyGrid2(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid2, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.temp = "A"
        self.lbl = Label(text="A")
        self.lbl.font_size = '60dp'
        self.add_widget(self.lbl)
        self.back = Button(text="Back", font_size=40)
        self.add_widget(self.back)

        self.selected_buttons = None

    def start(self, button_list, time):
        if len(button_list) == 0:
            return
        self.selected_buttons = button_list
        self.lbl.text = self.selected_buttons[0]
        Clock.schedule_interval(lambda x: self.update_lbl(random.choice(self.selected_buttons), time), time)

    def next_button(self):
        if self.selected_buttons.index(self.lbl.text) == len(self.selected_buttons) - 1:
            return 0
        else:
            return self.selected_buttons.index(self.lbl.text) + 1

    def update_lbl(self, button, time, *kwargs):
        #self.lbl.text = self.selected_buttons[button]
        self.lbl.text = button + " / " + str(time) + "s per chord" 

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

        self.main_screen = Screen(name="main_screen")
        self.new_screen = Screen(name="new_screen")

        self.add_widget(self.main_screen)
        self.add_widget(self.new_screen)

        main_grid = MyGrid()
        main_grid.submit.bind(on_press=self.next_screen)
        self.main_screen.add_widget(main_grid)

        next_grid = MyGrid2()
        next_grid.back.bind(on_press=self.back_screen)
        self.new_screen.add_widget(next_grid)

    def next_screen(self, *args):
        self.current = "new_screen"

    def back_screen(self, *args):
        self.current = "main_screen"



class MyApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    MyApp().run()
