import sys
from glob import glob
from os.path import join, dirname
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.stencilview import StencilView
from kivy.uix.effectwidget import *
from random import random as r
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.slider import Slider
from kivy.uix.effectwidget import *

class SvgWidget(BoxLayout):
    gauge_height = 85 
    mask_offset = -14.515
    gauge_width = 100    
    mask_rotations=[]
    value = NumericProperty(0)
        
    def __init__(self, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)

        size = self.height if self.height < self.width else self.width
        gauge_height = size / self.gauge_height
        x_center = self.pos[0] + self.width / 2 - self.gauge_width / 2

        with self.canvas:
            PushMatrix()
            self.t=Translate(x_center, self.pos[1], 0)
            self.sc=Scale(x=gauge_height, y=gauge_height)
            Svg('round_gauge_270.svg',  bezier_points=1, circle_points=1)
            self.mask_t = Translate(0, self.mask_offset)
            PushMatrix()
            self.mask_rotations.append(Rotate(angle=-135, axis=(0,0,1), origin=(self.center[0], self.center[1])))
            Svg('gauge_mask.svg')
            PopMatrix()
            PushMatrix()
            self.mask_rotations.append(Rotate(angle=-225, axis=(0,0,1), origin=(self.center[0], self.center[1])))
            Svg('gauge_mask.svg')
            PopMatrix()
            PushMatrix()
            self.mask_rotations.append(Rotate(angle=-315, axis=(0,0,1), origin=(self.center[0], self.center[1])))
            Svg('gauge_mask.svg')
            PopMatrix()
            PopMatrix()

        with self.canvas.after:
            PushMatrix()
            self.t_shadow=Translate(x_center, self.pos[1], 0)
            self.sc_shadow=Scale(x=gauge_height, y=gauge_height)
            Svg('round_gauge_270_shadow.svg', bezier_points=1, circle_points=1)
            PopMatrix()
            
        self.bind(pos=self.update_all, size=self.update_all)

    def update_all(self, *args):
        size = self.height if self.height < self.width else self.width
        gauge_height = size / self.gauge_height

        x_center = self.pos[0] + self.width / 2 - (self.gauge_width / 2) * gauge_height
	self.t.x = x_center 
        self.t.y = self.pos[1]
        self.t_shadow.x = x_center
        self.t_shadow.y = self.pos[1]

        self.sc.x=gauge_height
        self.sc.y=gauge_height
        self.sc_shadow.x = gauge_height
        self.sc_shadow.y = gauge_height

    def on_value(self, instance, value):
        angle = (value * 270) / 100
        self.mask_rotations[0].angle = -135 - angle
        self.mask_rotations[1].angle = -135 - angle  if angle > 90 else -225
        self.mask_rotations[2].angle = -135 - angle  if angle > 180 else -315

class SvgApp(App):

    value = 0

    def build(self):
        self.root = BoxLayout(pos_hint={'center_x':.5, 'center_y':.5}, orientation='vertical')

        self.svg = SvgWidget(size_hint_y=0.9)
        self.root.add_widget(self.svg)
        s = Slider(min=0, max=100, value=0, size_hint_y=0.1)
        self.root.add_widget(s)
        s.bind(value=self.on_value)
        s.value=50
  
    def on_value(self, instance, value):
        self.svg.value = value

        


if __name__ == '__main__':
    SvgApp().run()
