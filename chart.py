from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
from  more_itertools import unique_everseen
from random import shuffle as sf
 

#req = requests.get('http://localhost:2000/getcsvfile/trial')
req = requests.get('http://localhost:2000/getcsvfile/strenght-weakness_bp')
#file = requests.get('http://localhost:2000/getMp4video/strenght-weakness_bp.wmv')


##print(file,"file")


value = req.json()
data = value.get('data')



colorarr=[]
labelarr= []
Cols = []
index=[]
timearr=[]

for idx,i in enumerate(data):
   
    if (i.get('text') != 'neutral'):
       labelarr.append(i.get('text'))
       timearr.append(i.get('time'))
       colorarr.append(i.get('color'))
       index.append(idx)
       
       
final = np.array(timearr)
sf(final)

def Convert(final): 
    final = np.array(final) 
    return list(-final)



newarr=Convert(final)



class Window(QWidget):
    def __init__(self):
        super().__init__()
 
       
       
 
        p =self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)
        title = "Python charts"
        top = 400
        left = 400
        width = 700
        height = 500
 
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
 
        self.init_ui()
 
 
        self.show()
 
 
    def init_ui(self):
 
        #create media player object
 
    
    
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
       
        #create videowidget object
 
        videowidget = QVideoWidget()
 
 
        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
 
 
 
        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
 
 
 
        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
 
 
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        fig = plt.figure(figsize=(1,1))
        
        ax = fig.add_subplot(111)
        y_pos = np.arange(len(labelarr))
        d = 1./(len(final)+2.)
        ax.bar(y_pos, final,color=colorarr)
        ax.bar(y_pos,newarr,color=colorarr)
        ax.set(yticklabels='',xticklabels='')
        ax.tick_params(right= False,top= False,left= False, bottom= False)
      
      
        self.plotWidget = FigureCanvas(fig)
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
 
 
 
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.plotWidget)
        vboxLayout.addWidget(self.label)
        
 
 
        self.setLayout(vboxLayout)
 
        self.mediaPlayer.setVideoOutput(videowidget)
 
 
        #media player signals
 
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_errors) 
        
        def onclick(event):  
          print('hiiiii')
          x = int(np.round(event.xdata))
          print(x,"index")
          print(final[x],'newarray')
   
        fig.canvas.mpl_connect('button_press_event', onclick)
   
        
        
       
      
 
 
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
 
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            print(filename,"file") 
 
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print(self.mediaPlayer.state(),"00000")
 
        else:
            self.mediaPlayer.play()
            print(self.mediaPlayer.state(),"2222")
 
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
 
            )
 
    def position_changed(self, position):
        self.slider.setValue(position)
 
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
 
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
 
 
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
        print(self.mediaPlayer.error, 'error')
        print('error: ' + str(self.mediaPlayer.error()))
      
   
 
 
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())