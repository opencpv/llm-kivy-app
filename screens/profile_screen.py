from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import json
import os

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = self.load_user_data()
        
        # Main layout with reduced padding
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Back button - full width
        back_btn = Button(
            text='Back to Main',
            size_hint=(1, None),
            height='45dp',
            background_color=get_color_from_hex('#2196F3'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)

        # Create scrollable content with reduced spacing
        scroll_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        fields = [
            ('Name', 'name', False),
            ('Age', 'age', False),
            ('Country', 'country', False),
            ('Medical History', 'medical_history', True),
            ('Current Medications', 'medications', True),
            ('Current Activities', 'activities', True)
        ]

        for label_text, key, is_multiline in fields:
            # Reduced height for field layouts
            field_layout = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height='80dp' if not is_multiline else '130dp',
                spacing=2  # Reduced spacing between label and input
            )
            
            # Centered white labels
            label = Label(
                text=label_text,
                size_hint_y=None,
                height='25dp',
                halign='center',
                valign='bottom',
                bold=True,
                color=(1, 1, 1, 1)  # White color
            )
            label.bind(size=label.setter('text_size'))
            
            input_widget = TextInput(
                multiline=is_multiline,
                text=self.user_data.get(key, ''),
                size_hint_y=None,
                height='40dp' if not is_multiline else '100dp',
                padding=('10dp', '10dp'),
                background_color=get_color_from_hex('#F5F5F5'),
                foreground_color=get_color_from_hex('#333333')
            )
            input_widget.bind(text=lambda instance, value, k=key: self.update_user_data(k, value))
            
            field_layout.add_widget(label)
            field_layout.add_widget(input_widget)
            scroll_layout.add_widget(field_layout)

        # Create ScrollView and add scroll_layout
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)

        # Save button - full width
        save_btn = Button(
            text='Save Profile',
            size_hint=(1, None),
            height='50dp',
            background_color=get_color_from_hex('#4CAF50'),
            background_normal='',
            bold=True
        )
        save_btn.bind(on_press=self.save_profile)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)

    def update_user_data(self, key, value):
        self.user_data[key] = value

    def save_profile(self, instance):
        if self.save_user_data(self.user_data):
            # Show success popup only if save was successful
            popup = Popup(
                title='Success',
                content=Label(text='Profile saved successfully!'),
                size_hint=(None, None),
                size=(300, 150)
            )
            popup.open()

    def load_user_data(self):
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        try:
            with open('data/user_profile.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default empty profile if file doesn't exist or is invalid
            return {
                'name': '',
                'age': '',
                'country': '',
                'medical_history': '',
                'medications': '',
                'activities': ''
            }

    def save_user_data(self, data):
        try:
            with open('data/user_profile.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            # Show error popup if save fails
            popup = Popup(
                title='Error',
                content=Label(text=f'Failed to save profile: {str(e)}'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
            return False 