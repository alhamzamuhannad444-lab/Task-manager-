from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
try:
    from plyer import vibrator
except ImportError:
    vibrator = None

class TodoApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        
        self.add_widget(Label(text="منظم المهام الذكي مع المؤقت", font_size=20))
        
        self.task_input = TextInput(hint_text="اكتب المهمة هنا", size_hint_y=None, height=40)
        self.add_widget(self.task_input)
        
        timer_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.timer_checkbox = CheckBox(active=False)
        timer_layout.add_widget(self.timer_checkbox)
        timer_layout.add_widget(Label(text="تفعيل مؤقت (10 ثوانٍ للتجربة)"))
        self.add_widget(timer_layout)
        
        button = Button(text="إضافة مهمة", size_hint_y=None, height=40)
        button.bind(on_press=self.add_task)
        self.add_widget(button)
        
        self.tasks_label = Label(text="المهام:\n")
        self.add_widget(self.tasks_label)
        
        self.tasks = []
        
    def add_task(self, instance):
        task_name = self.task_input.text
        has_timer = self.timer_checkbox.active
        if task_name:
            self.tasks.append({'name': task_name, 'timer': has_timer})
            self.update_tasks_display()
            self.task_input.text = ""
            
            if has_timer:
                Clock.schedule_once(lambda dt: self.task_time_up(task_name), 10)

    def update_tasks_display(self):
        display_text = "المهام:\n"
        for i, t in enumerate(self.tasks):
            timer_status = " (مؤقت مفعل)" if t['timer'] else ""
            display_text += f"{i+1}. {t['name']}{timer_status}\n"
        self.tasks_label.text = display_text

    def task_time_up(self, task_name):
        if vibrator:
            try:
                vibrator.vibrate(time=2)
            except Exception:
                pass
        print(f"انتهى وقت المهمة: {task_name}")

class MyApp(App):
    def build(self):
        return TodoApp()

if __name__ == '__main__':
    MyApp().run()
  
