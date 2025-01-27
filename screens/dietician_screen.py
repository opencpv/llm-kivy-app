from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
import json
import os
from ask_dietician import ask_dietician 
class DieticianScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = self.load_user_data()
        self.response = None
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Back button
        back_btn = Button(
            text='Back to Main',
            size_hint=(1, None),
            height='45dp',
            background_color=get_color_from_hex('#2196F3'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        
        # Scrollable content
        scroll_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Health Goal
        health_goal_label = Label(
            text='Select Health Goal',
            size_hint_y=None,
            height='25dp',
            halign='center',
            valign='bottom',
            bold=True,
            color=(1, 1, 1, 1)
        )
        health_goal_label.bind(size=health_goal_label.setter('text_size'))
        
        health_goal_spinner = Spinner(
            text=self.user_data.get('health_goal', 'Select Health Goal'),
            values=('Weight Loss', 'Muscle Gain', 'Maintain Weight', 'Improve Health'),
            size_hint_y=None,
            height='40dp'
        )
        health_goal_spinner.bind(text=lambda instance, value: self.update_user_data('health_goal', value))
        
        scroll_layout.add_widget(health_goal_label)
        scroll_layout.add_widget(health_goal_spinner)
        
        # Dietary Preference
        dietary_preference_label = Label(
            text='Select Dietary Preference',
            size_hint_y=None,
            height='25dp',
            halign='center',
            valign='bottom',
            bold=True,
            color=(1, 1, 1, 1)
        )
        dietary_preference_label.bind(size=dietary_preference_label.setter('text_size'))
        
        dietary_preference_spinner = Spinner(
            text=self.user_data.get('dietary_preference', 'Select Dietary Preference'),
            values=('Vegetarian', 'Vegan', 'Pescatarian', 'Omnivore'),
            size_hint_y=None,
            height='40dp'
        )
        dietary_preference_spinner.bind(text=lambda instance, value: self.update_user_data('dietary_preference', value))
        
        scroll_layout.add_widget(dietary_preference_label)
        scroll_layout.add_widget(dietary_preference_spinner)
        
        # Allergies
        allergies_label = Label(
            text='Add Allergies',
            size_hint_y=None,
            height='25dp',
            halign='center',
            valign='bottom',
            bold=True,
            color=(1, 1, 1, 1)
        )
        allergies_label.bind(size=allergies_label.setter('text_size'))
        
        allergies_input = TextInput(
            multiline=True,
            text=self.user_data.get('allergies', ''),
            size_hint_y=None,
            height='100dp',
            padding=('10dp', '10dp'),
            background_color=get_color_from_hex('#F5F5F5'),
            foreground_color=get_color_from_hex('#333333')
        )
        allergies_input.bind(text=lambda instance, value: self.update_user_data('allergies', value))
        
        scroll_layout.add_widget(allergies_label)
        scroll_layout.add_widget(allergies_input)
        
        # Create ScrollView and add scroll_layout
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)
        
        # Save button
        save_btn = Button(
            text='Suggest',
            size_hint=(1, None),
            height='50dp',
            background_color=get_color_from_hex('#4CAF50'),
            background_normal='',
            bold=True
        )
        save_btn.bind(on_press=self.save_preferences)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)

    def get_ai_response(self, message):
                try:
                    response = ask_dietician(message)
                    # Extract the actual message content from the API response
                    ai_message = response['choices'][0]['message']['content']
                    self.response = ai_message
                    print(ai_message)
                except Exception as e:
                    self.add_message("Sorry, I couldn't process your request.", is_user=False)
   
    def update_user_data(self, key, value):
        self.user_data[key] = value

    def save_preferences(self, instance):
        health_goal = self.user_data.get('health_goal', 'a healthy lifestyle')
        dietary_preference = self.user_data.get('dietary_preference', 'any')
        allergies = self.user_data.get('allergies', 'none')
        message = f"I’m looking for healthy Ghanaian food options. I’m {dietary_preference} and trying to achieve {health_goal}. I have the following allergies: {allergies}. Can you help?"
        self.get_ai_response(message)
        if self.response:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            response_label = Label(
                text=self.response,
                size_hint_y=None,
                halign='left',
                valign='top',
                text_size=(self.width - 20, None),
                markup=True
            )
            response_label.bind(
                texture_size=lambda instance, value: setattr(instance, 'height', value[1])
            )
            response_label.bind(size=response_label.setter('text_size'))
            
            scroll_view = ScrollView(size_hint=(1, 1))
            scroll_view.add_widget(response_label)
            
            close_btn = Button(
                text='Close',
                size_hint=(1, None),
                height='50dp',
                background_color=get_color_from_hex('#F44336'),
                background_normal=''
            )
            close_btn.bind(on_press=lambda x: popup.dismiss())
            
            content.add_widget(scroll_view)
            content.add_widget(close_btn)
            
            popup = Popup(
                title='Dietician Suggestion',
                content=content,
                size_hint=(1, 1)
            )
            popup.open()
        

    def load_user_data(self):
        os.makedirs('data', exist_ok=True)
        try:
            with open('data/user_profile.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'health_goal': '',
                'dietary_preference': '',
                'allergies': ''
            }

    def save_user_data(self, data):
        try:
            with open('data/user_profile.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            popup = Popup(
                title='Error',
                content=Label(text=f'Failed to save preferences: {str(e)}'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
            return False

   