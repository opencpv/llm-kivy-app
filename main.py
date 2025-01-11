from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex, platform
from kivy.core.window import Window
from screens.profile_screen import ProfileScreen
from screens.chat_screen import ChatScreen
import json
import os
from ai_response import send_chat_message
from kivy.uix.label import Label
from screens.profile_screen import ProfileScreen
from kivy.clock import Clock
from kivy.uix.image import Image
from screens.chat_screen import ChatScreen

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout with gradient background
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.bind(size=self._update_background)
        
        # App logo/icon
        logo = Image(
            source='assets/healthcare_logo.png',  # Add your logo
            size_hint=(None, None),
            size=('100dp', '100dp'),
            pos_hint={'center_x': 0.5}
        )
        
        # Welcome label with shadow effect
        welcome = Label(
            text='Healthcare Assistant',
            font_size='32sp',
            size_hint_y=0.2,
            color=get_color_from_hex('#2196F3'),
            bold=True
        )
        
        # Buttons layout
        buttons_layout = BoxLayout(orientation='vertical', spacing=25, size_hint_y=0.5)
        
        # Enhanced buttons with icons
        profile_btn = Button(
            text='My Profile',
            size_hint_y=None,
            height='70dp',
            background_color=get_color_from_hex('#2196F3'),
            background_normal='',
            font_size='18sp',
            bold=True
        )
        profile_btn.bind(on_press=self._button_pressed)
        
        chat_btn = Button(
            text='AI Health Assistant',
            size_hint_y=None,
            height='70dp',
            background_color=get_color_from_hex('#4CAF50'),
            background_normal='',
            font_size='18sp',
            bold=True
        )
        chat_btn.bind(on_press=self._button_pressed)
        
        # Add widgets
        layout.add_widget(logo)
        layout.add_widget(welcome)
        layout.add_widget(buttons_layout)
        buttons_layout.add_widget(profile_btn)
        buttons_layout.add_widget(chat_btn)
        self.add_widget(layout)
    
    def _button_pressed(self, instance):
        # Add button press animation
        instance.opacity = 0.8
        def restore_opacity(dt):
            instance.opacity = 1
        Clock.schedule_once(restore_opacity, 0.1)
        if instance.text == 'My Profile':
            self.manager.current = 'profile'
        else:
            self.manager.current = 'chat'

    def _update_background(self, instance, value):
        """Updates the background of the layout"""
        # You can implement gradient or background color logic here
        pass  # For now, we'll leave it empty



class HealthcareApp(App):
    def build(self):
        # Adjust window size only on desktop
        if platform != 'android':
            Window.size = (400, 600)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(ChatScreen(name='chat'))
        
        return sm

if __name__ == '__main__':
    HealthcareApp().run()
