from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import requests
import random


class LoginScreen(Screen):
    def check_pass(self):
        global name
        name = self.ids['name'].text
        global pubkey
        pubkey = self.ids['publickey'].text
        Data = {"Name": name,"priv_key": pubkey}
        r = requests.post('http://34.87.108.156:8000/ValidateUser/', data=Data)
        D = r.json()
        if D['user'] == "exist" and self.ids['publickey'].text:
            imp.sm.current = 'home'
        else:
            imp.sm.current = 'login'

    def create_user(self,instance):
        Data = {'SigninName': signin_name}
        r = requests.post('http://34.87.108.156:8000/CreateUser/', data=Data)
        self.ids['publickey'].text = public_key

    def on_text(self,instance,value):
        global signin_name
        signin_name = value

    def signin(self):
        layout = BoxLayout(orientation='vertical')
        popuplabel = Label(text="Enter your name")
        popuptext = TextInput(hint_text="Name", size_hint=[0.6,0.1],pos_hint={"x": 0.2},multiline=False)
        closeButton = Button(text='Signup',size_hint=[0.3,0.1],pos_hint={"x": 0.35})
        layout.add_widget(popuplabel)
        layout.add_widget(popuptext)
        layout.add_widget(closeButton)
        popup = Popup(title='SignUp',content=layout,size_hint= [0.6,0.6], auto_dismiss= False,on_dismiss=self.create_user)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)
        popuptext.bind(text=self.on_text)


class HomeScreen(Screen):

    def buy_music(self):
        Data = {'src': 'admin', 'dest': name, 'amt': 1, 'priv_key': pubkey}
        r = requests.post('http://34.87.108.156:8000/BuyMusic/', data=Data)
        d = r.json()
        self.ids['balance'].text = d['bought']

    def update_labels(self):
        Data = {'acc_name': name}
        r = requests.post('http://34.87.108.156:8000/GetBalance/', data=Data)
        D = r.json()
        self.ids['balance'].text = 'Balance: '+ str(D['ans'])
        rr = requests.get('http://34.87.108.156:8000/GetLabels/')
        D = rr.json()
        D = random.sample(D,4)
        for i in range(len(D)):
            self.ids['label'+str(i+1)].text = D[i]+' by Musician'+str(i+1)


class ProfileScreen(Screen):
    def query_account(self):
        Data = {'acc_id': name}
        r = requests.get('http://34.87.108.156:8000/QueryAccount/', data = Data)
        self.ids['response'].text = r.text

    def query_music(self,instance):
        Data = {'acc_id': name,'asset': self.cahract}
        d = requests.get('http://34.87.108.156:8000/QueryMusic/', data = Data)
        a = d.text
        re = a.replace('\n', ' ')
        self.ids['response'].text = re
        print(re)

    def on_text(self,instance,value):
        self.cahract = value

    def query_musicPopup(self):
        layout = BoxLayout(orientation='vertical')
        popuplabel = Label(text="Enter Title")
        popuptext = TextInput(hint_text="Title", size_hint=[0.6, 0.1], pos_hint={"x": 0.2}, multiline=False)
        closeButton = Button(text='Query', size_hint=[0.3, 0.1], pos_hint={"x": 0.35})
        layout.add_widget(popuplabel)
        layout.add_widget(popuptext)
        layout.add_widget(closeButton)
        popup = Popup(title='Query', content=layout, size_hint=[0.6, 0.6], auto_dismiss=False,on_dismiss=self.query_music)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)
        popuptext.bind(text=self.on_text)

    def upload_music(self,instance):
        Data = {'acc_name': name, 'asset': self.cahract, 'priv_key': pubkey}
        d = requests.post('http://34.87.108.156:8000/UploadMusic/', data=Data)
        self.ids['response'].text = d.text

    def upload_musicPopup(self):
        layout = BoxLayout(orientation='vertical')
        popuplabel = Label(text="Enter Title")
        popuptext = TextInput(hint_text="Title", size_hint=[0.6, 0.1], pos_hint={"x": 0.2}, multiline=False)
        closeButton = Button(text='Upload', size_hint=[0.3, 0.1], pos_hint={"x": 0.35})
        layout.add_widget(popuplabel)
        layout.add_widget(popuptext)
        layout.add_widget(closeButton)
        popup = Popup(title='Upload', content=layout, size_hint=[0.6, 0.6], auto_dismiss=False,on_dismiss=self.upload_music)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)
        popuptext.bind(text=self.on_text)

    def buy_coin(self,instance):
        Data = {'acc_name': name, 'amt': self.cahract}
        d = requests.post('http://34.87.108.156:8000/BuyCoin/', data=Data)
        self.ids['response'].text = d.text

    def buy_coinPopup(self):
        layout = BoxLayout(orientation='vertical')
        popuplabel = Label(text="Buy Coins")
        popuptext = TextInput(hint_text="Amount", size_hint=[0.6, 0.1], pos_hint={"x": 0.2}, multiline=False)
        closeButton = Button(text='Buy', size_hint=[0.3, 0.1], pos_hint={"x": 0.35})
        layout.add_widget(popuplabel)
        layout.add_widget(popuptext)
        layout.add_widget(closeButton)
        popup = Popup(title='Upload', content=layout, size_hint=[0.6, 0.6], auto_dismiss=False,on_dismiss=self.buy_coin)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)
        popuptext.bind(text=self.on_text)


class BlockMusicApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        return self.sm


if __name__ == '__main__':
    imp = BlockMusicApp()
    imp.run()
