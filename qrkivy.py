from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import qrcode
#from qrcode
from kivy.core.window import Window
from kivy.uix.popup import Popup

class MainApp(App):
    def build(self):
        self.user_info = {}
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ایجاد تکس باکس‌ها
        self.name_input = TextInput(hint_text='name')
        self.family_name_input = TextInput(hint_text='family')
        self.id_number_input = TextInput(hint_text='ss')
        self.national_id_input = TextInput(hint_text='sm')
        
        # اضافه کردن تکس باکس‌ها به لایه
        layout.add_widget(self.name_input)
        layout.add_widget(self.family_name_input)
        layout.add_widget(self.id_number_input)
        layout.add_widget(self.national_id_input)
        
        # ایجاد دکمه ثبت
        submit_button = Button(text='ثبت', size_hint=(1, 0.2))
        submit_button.bind(on_press=self.submit_info)
        layout.add_widget(submit_button)
        
        return layout
    
    def submit_info(self, instance):
        # ذخیره اطلاعات کاربر
        self.user_info['name'] = self.name_input.text
        self.user_info['family_name'] = self.family_name_input.text
        self.user_info['id_number'] = self.id_number_input.text
        self.user_info['national_id'] = self.national_id_input.text
        
        # تولید کد QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.user_info)
        qr.make(fit=True)
        image = qr.make_image(fill='black', back_color='white')
        #qr_image = qr.make_image(fill='black', back_color='white')
        # نمایش کد QR در یک پنجره جدید
        popup_layout = BoxLayout(orientation='vertical')
        qr_code_label = Label(text='کد QR شما:')
        popup_layout.add_widget(qr_code_label)
        image.save("user_qr.png") # ذخیره تصویر کد QR
        """qr_image = image(source='user_qr.png')
        popup_layout.add_widget(qr_image)
        popup = Popup(title='کد QR', content=popup_layout)
        popup.open()"""
        # بستن پنجره فعلی
        Window.close()
if __name__ == '__main__':
    MainApp().run()