# FB-downloder




from logging import FATAL
from server.clint import MYapp
from kivy.app import App
from kivy.core import window
from kivy.uix.label import Label
from kivy.uix.textinput import Selector, TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.core.window import Window
import re
import requests
from datetime import datetime
import os
from kivy.app import user_data_dir
from os.path import dirname, join
join(dirname(user_data_dir), 'DCIM')
from kivy.utils import platform


Window.size = (300, 500)


class MyApp(App):
    def build(self):
        self.screen = Screen()
        self.l = Label(text="WELCOME TO FACEBOOK DOWNLODER",
                       font_size='15', pos_hint={"center_x": .5, "center_y": .9})
        self.l1 = Label(text="URL", font_size='15', pos_hint={
                        "center_x": .1, "center_y": .8})
        self.url1 = TextInput(font_size='15', size_hint=(.8, .05), pos_hint={
                              "center_x": .55, "center_y": .8}, multiline=False, padding_x=0, padding_y=0)
        self.succes = Label(text="", font_size='15', pos_hint={
            "center_x": .5, "center_y": .5})
        self.hd = Button(text="HD Download", size_hint=(.3, .05),
                         pos_hint={"center_x": .25, "center_y": .2})
        self.sd = Button(text="SD Download", size_hint=(.3, .05),
                         pos_hint={"center_x": .65, "center_y": .2})
        self.qu = Label(text='', font_size='20', pos_hint={
            "center_x": .5, "center_y": .6})
        self.hd.bind(on_press=self.hddwn)
        self.sd.bind(on_press=self.sddwn)
        self.screen.add_widget(self.l)
        self.screen.add_widget(self.url1)
        self.screen.add_widget(self.l1)
        self.screen.add_widget(self.succes)
        # self.screen.add_widget(self.btn)
        self.screen.add_widget(self.hd)
        self.screen.add_widget(self.sd)
        self.screen.add_widget(self.qu)
        return self.screen

    def hddwn(self, instance):
        self.hd.disabled = True
        self._input_1 = 'A'
        self.main()

    def sddwn(self, instance):
        self.sd.disabled = True
        self._input_1 = 'B'
        self.main()

    def main(self):
        try:
            if self._input_1 == "A":
                self.download_video("HD")
            else:
                self.download_video("SD")
        except(KeyboardInterrupt):
            print("\nProgramme Interrupted")
        self.hd.disabled = False
        self.sd.disabled = False

    def download_video(self, quality):
        self.qu.text = ''
        self.succes.text = ''
        self.url = self.url1.text

        try:
            if self.url:
                self.html = requests.get(self.url).content.decode('utf-8')

            """Download the video in HD or SD quality"""
            self.qu.text = f"Download the video in {quality} quality"
            video_url = re.search(
                rf'{quality.lower()}_src:"(.+?)"', self.html).group(1)
            file_size_request = requests.get(video_url, stream=True)
            file_size = int(file_size_request.headers['Content-Length'])
            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            # t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
            with open(filename + '.mp4', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    # t.update(len(data))
                    f.write(data)
            # t.close()
            self.succes.text = "FACEBOOK VIDEO DOWNLODED SUCCESFULLY"
        except Exception as e:
            self.succes.text = "FACEBOOK VIDEO DOWNLODE FAILED"

if __name__=='__main__':
    a=MYapp()
    a.run()
