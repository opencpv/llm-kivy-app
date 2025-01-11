from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.clock import Clock
from ai_response import send_chat_message
from kivy.graphics import Color, Rectangle

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10)
        
        # Header with back button
        header = BoxLayout(size_hint_y=0.1, spacing=10)
        back_button = Button(
            text='Back',
            size_hint_x=0.2,
            background_color=get_color_from_hex('#2196F3'),
            background_normal=''
        )
        back_button.bind(on_press=self.go_back)
        
        header_label = Label(
            text='AI Health Assistant',
            font_size='20sp',
            bold=True
        )
        
        header.add_widget(back_button)
        header.add_widget(header_label)
        
        # Chat history scroll view
        self.chat_history = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.chat_history.bind(minimum_height=self.chat_history.setter('height'))
        
        scroll_view = ScrollView(size_hint_y=0.8)
        scroll_view.add_widget(self.chat_history)
        
        # Input area
        input_area = BoxLayout(size_hint_y=0.1, spacing=10)
        self.message_input = TextInput(
            multiline=False,
            size_hint_x=0.8,
            hint_text='Type your health question...'
        )
        self.message_input.bind(on_text_validate=self.send_message)
        
        send_button = Button(
            text='Send',
            size_hint_x=0.2,
            background_color=get_color_from_hex('#4CAF50'),
            background_normal=''
        )
        send_button.bind(on_press=self.send_message)
        
        input_area.add_widget(self.message_input)
        input_area.add_widget(send_button)
        
        # Add all widgets to main layout
        layout.add_widget(header)
        layout.add_widget(scroll_view)
        layout.add_widget(input_area)
        
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'

    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:
            # Add user message to chat
            self.add_message(message, is_user=True)
            
            # Clear input
            self.message_input.text = ''
            
            # Get AI response
            Clock.schedule_once(lambda dt: self.get_ai_response(message), 0.1)

    def get_ai_response(self, message):
        try:
            response = send_chat_message(message)
            # Extract the actual message content from the API response
            ai_message = response['choices'][0]['message']['content']
            self.add_message(ai_message, is_user=False)
        except Exception as e:
            self.add_message("Sorry, I couldn't process your request.", is_user=False)

    def add_message(self, text, is_user=True):
        message_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=1.0,
            padding=10,
            spacing=5
        )
        
        # Message bubble
        message = Label(
            text=text,
            text_size=(Window.width * 0.9, None),
            size_hint_y=None,
            halign='left',
            valign='middle',
            padding=(15, 10),
            color=(1, 1, 1, 1) if is_user else (0, 0, 0, 1)
        )
        message.bind(texture_size=message.setter('size'))
        
        # Set the message_box height based on the message content
        message.bind(texture_size=lambda *x: setattr(message_box, 'height', message.texture_size[1] + 20))
        
        # Create a colored background using canvas
        with message.canvas.before:
            Color(*get_color_from_hex('#2196F3' if is_user else '#E0E0E0'))
            self.rect = Rectangle(pos=message.pos, size=message.size)
        
        # Update rectangle position and size when label size changes
        def update_rect(instance, value):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(*get_color_from_hex('#2196F3' if is_user else '#E0E0E0'))
                self.rect = Rectangle(pos=instance.pos, size=instance.size)
        message.bind(pos=update_rect, size=update_rect)
        
        message_box.add_widget(message)
        self.chat_history.add_widget(message_box)
