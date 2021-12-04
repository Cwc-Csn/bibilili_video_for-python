#-*-codeing=utf-8 -*-
#@Time :2021/9/4 22:05
#@Author :Csn
#@File:Qtdesginer
#@Software:PyCharm

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QFile
from aip import AipOcr
from bs4 import  BeautifulSoup
import  re #正则表达式
import requests
import time
import requests
import re
import ast
import json
import pprint
import subprocess
from threading import Thread


class ui:

    def __init__(self):
        self.app=QApplication(sys.argv)
        self.file=QFile("ui/bilibili.ui")
        self.file.open(QFile.ReadOnly)


        self.loader=QUiLoader()
        self.win=self.loader.load(self.file)
        #self.win.line.setText('https://www.huya.com/g/4079')
        self.win.pushButton.clicked.connect(self.pushButton)
        self.win.pushButton_2.clicked.connect(self.pushButton_2)
        self.win.pushButton_3.clicked.connect(self.pushButton_3)
        self.win.pushButton_4.clicked.connect(self.pushButton_4)
        self.win.show()



        sys.exit(self.app.exec_())

    def pushButton(self):
        header=self.win.plainTextEdit.toPlainText()
        print(type(header))

        headers=ast.literal_eval(header)
        print(type(headers))
        #https://www.bilibili.com/bangumi/play/ep409607
        #url=self.win.line.displayText()
        url=self.win.line.text()
        title=self.win.line_2.text()
        print(url)
        video =self.video_info(url,title)
        self.save(video[0], video[1], video[2])
        self.merge_date(title)
        QMessageBox.about(self.win,
                          '结果',
                          '保存成功'
                          )

    def thredget(self,text):
        self.win.plainTextEdit.appendPlainText(text)
    def pushButton_2(self):
        # openfile=QFileDialog.getOpenFileName(self.win,'打开图片','','*.jpg *.png')
        # print(openfile[0])
        # print(type(openfile))
        # self.win.line.setText(openfile[0])
        text=self.win.line.displayText()


    def pushButton_3(self):
        # headers=self.win.plainTextEdit.toPlainText()
        text=self.win.plainTextEdit.toPlainText()
        print(text)

    def pushButton_4(self):
        APP_ID = '24699283'
        API_KEY = 'cdkqito0IsBxKXmfnbA1hxab'
        SECRET_KEY = 'NgHnMsHmkb6leKeLLsNM9OiS4G6QAPY2'

    def getresponse(self,url):
        header =self.win.plainTextEdit.toPlainText()
        headers = ast.literal_eval(header)
        response = requests.get(url=url, headers=headers)
        return response
    def video_info(self,url,title):
        response = self.getresponse(url)
        # print(response.text)

        # title=re.findall('<h1 title="侦探已死：第3话 这就是唯喵品质！">(.*?)</h1>',response.text)[0]
        title = title.replace(' ', '')
        # print(title)
        html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]
        json_data = json.loads(html_data)
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
        video_url = json_data['data']['dash']['video'][0]['baseUrl']
        video_info = [title, audio_url, video_url]
        return video_info
        # pprint.pprint(json_data)
        # print(html_data)

    def save(self,title, audio_url, vedio_url):
        audio_content = self.getresponse(audio_url).content
        vedio_content = self.getresponse(vedio_url).content
        with open(title + '.mp3', mode='wb') as f:
            f.write(audio_content)
        with open(title + '.mp4', mode='wb') as f1:
            f1.write(vedio_content)
        print('ok')

    def merge_date(self,video_name):
        # ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strtict experimental output.mp4
        i = 1
        print(video_name)
        COMMAND = f'ffmpeg -i {video_name}.mp4 -i {video_name}.mp3 -c:v copy -c:a aac -strict experimental {video_name}ou.mp4'
        # ffmpeg -i ou.mp4 -i ou.mp3 -c:v copy -c:a aac -strict experimental ou.mp4
        print(COMMAND)
        # ffmpeg -i 侦探已死：第3话这就是唯喵品质！.mp4 -i 侦探已死：第3话这就是唯喵品质！.mp3 -c:v copy -c:a aac -strict experimental output.mp4
        # p=subprocess.Popen(COMMAND, shell=True,encoding='utf-8',cwd=r'F:\代码存储\Python\bilibili')
        p = subprocess.Popen(COMMAND, shell=True)
        print(p.stderr)
ui()
input()