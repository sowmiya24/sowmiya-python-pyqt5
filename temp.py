from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import requests
import matplotlib.pyplot as plt
import collections
import pandas as pd
from  more_itertools import unique_everseen
import matplotlib.colors as mcolors
import mplcursors



req = requests.get('http://localhost:2000/getcsvfile/strenght-weakness_bp')

value = req.json()
data = value.get('data')


colorarr=[]
labelarr = []
textarr = []
xdata=[]
timearr=[]
index=[]
happyval=[]
sadval=[]
disgustval=[]
contval=[]
angerval=[]
surpriseval=[]
fearval=[]
valarr=[]
newarr=[]



for idx,i in enumerate(data):
   
    if (i.get('text') != 'neutral'):
       textarr.append(i.get('text'))
       timearr.append(i.get('time'))
       colorarr.append(i.get('color'))
    if(i.get('text')=='happy'):   
       happyval.append(i.get('time'))
       valarr.append(happyval)
    elif(i.get('text')=='sad'): 
       sadval.append(i.get('time'))
       valarr.append(sadval)
    elif(i.get('text')=='anger'): 
       angerval.append(i.get('time'))
       valarr.append(angerval)
    elif(i.get('text')=='disgust'): 
       disgustval.append(i.get('time'))
       valarr.append(disgustval)
    elif(i.get('text')=='contempt'): 
       contval.append(i.get('time'))
       valarr.append(contval)
    elif(i.get('text')=='surprise'): 
       surpriseval.append(i.get('time'))
       valarr.append(surpriseval)
    elif(i.get('text')=='fear'): 
       fearval.append(i.get('time'))
       valarr.append(fearval)

counter=collections.Counter(textarr) 

for idx,key in enumerate(counter):
    xdata.append(counter[key])
    labelarr.append(key)
   
#valarr=[fearval,surpriseval,angerval,contval,disgustval,sadval,happyval]

#newdata = np.random.random((len(labelarr), len(timearr)))
 


longest = valarr[sorted([(i,len(l)) for i,l in enumerate(valarr)], key=lambda t: t[1])[-1][0]]   

for idx,val in  enumerate(longest):
      index.append(idx);

np.random.shuffle(index)
finalarr=pd.DataFrame(valarr).drop_duplicates().values
finalarr = finalarr[:,index]
newarr=np.array(np.transpose(finalarr))
colorarr=list(unique_everseen(colorarr))
cmap=mcolors.ListedColormap(colorarr)

def get_hsvcmap(i, N,rot=0.):
   
    nsc = 2
    chsv = mcolors.rgb_to_hsv(cmap(((np.arange(N)/N)) % 1.)[i,:3])
    rhsv = mcolors.rgb_to_hsv(cmap(np.linspace(.2,1,nsc))[:,:3])
    arhsv = np.tile(chsv,nsc).reshape(nsc,3)
    arhsv[:,1:] = rhsv[:,1:]
    rgb = mcolors.hsv_to_rgb(arhsv)
    return mcolors.LinearSegmentedColormap.from_list('',rgb)
   

def columnwise_heatmap(array, ax=None, **kw):
    ax = ax or plt.gca()
   
    premask = np.tile(np.arange(array.shape[1]), array.shape[0]).reshape(array.shape)
    images = []
    
    for i in range(array.shape[1]):
       
        col = np.ma.array(array, mask = premask != i)
        im = ax.imshow(col, cmap=get_hsvcmap(i, array.shape[1]), **kw,interpolation='nearest')
        images.append(im)
        cursor = mplcursors.cursor(im, hover=True)
        @cursor.connect("add")
        def on_add(sel):
               i,j = sel.target.index
               if(np.isnan(newarr[i,j]) == False):
                 sel.annotation.set_text(newarr[i,j])
               else:
                 sel.annotation.set_text('')
    return images
    

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        title = "Python charts"
        top = 400
        left = 400
        width = 900
        height = 900
 
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.MyUI()
      
    def MyUI(self):
 
       
        canvas1 = Heatmap(self)
        canvas1.move(0, 400)
        canvas = Canvas(self, width=9, height=4)
        canvas.move(0, 0)
        #canvas2 = Bar(self, width=9, height=4)
        #canvas2.move(0,0 ) 
  
       

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 9, height = 3, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        self.plot()
    def plot(self):
        x = np.array(xdata) 
        labels = labelarr
        colors = colorarr
        ax = self.figure.add_subplot(111)
        ax.pie(x, colors=colors,autopct=lambda p: '{:.1f}%'.format(p,(p/100)))
        ax.legend(labels, bbox_to_anchor=(0.9, 1), loc='upper left', borderaxespad=0.)

class Heatmap(FigureCanvas):
    def __init__(self, parent = None, width = 9, height = 5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()
        
   
    def plot(self):
        
         df = pd.DataFrame(newarr,columns=labelarr, index=index)
         ax = self.figure.add_subplot(111)
         
         ims = columnwise_heatmap(df.values, ax=ax)
         
         ax.set(xticks=np.arange(len(df.columns))+0.5,yticks=np.arange(len(df.index))+0.5,yticklabels='',xticklabels='')
         ax.tick_params(right= False,top= False,left= False, bottom= False)
         ax.autoscale(tight=True)
         ax.grid(linewidth=0.2)
         self.figure.canvas.mpl_connect('button_press_event', self.onclick)
         #orange_rgb =  mcolors.hex2color(mcolors.cnames['orange'])
         #ax.patch.set_facecolor((1.,0.,0.95689655))
         #ax.patch.set(hatch='xx', edgecolor='gray')
         #ax.axis('off')
       
        
        # print(finalarr,"valarr")
        # print(np.transpose(finalarr),"zip")
         #arr=np.nan_to_num(newarr)
         
         #for i in range(len(df.index)):
             #for j in range(len(df.columns)):
                
                # if(np.isnan(finalarr[j,i]) == False):
                   #text = ax.text(i, j, np.around(finalarr[j, i], decimals=2),
                   #ha="center", va="center", color="black")
                 #  print(finalarr[j,i])
                 
         
    
    def onclick(self,event):               
     x = int(np.round(event.xdata))
     y = int(np.round(event.ydata))
     print(x,y,'index')
     print(newarr[y,x],'time')
     
   
class Bar(FigureCanvas):
    def __init__(self, parent = None, width = 9, height = 3, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        self.plot()
    def plot(self):       
        ax = self.figure.add_subplot()
        arr=np.nan_to_num(newarr)
        x = np.arange(arr.shape[0])
        print(arr.shape[0],'new')
        dx = (np.arange(arr.shape[1])-arr.shape[1]/2.)/(arr.shape[1]+2.)
        d = 1./(arr.shape[1]+2.)
        for i in range(arr.shape[1]):
             #bottom=np.sum(arr[:,0:i], axis=1)  
             ax.bar(x+dx[i],arr[:,i], width=d, label=labelarr[i],color=colorarr[i])
             #ax.bar(x,arr[:,i], bottom=bottom,color=colorarr[i])
             ax.legend(labels=labelarr, bbox_to_anchor=(0.9, 1), loc='upper left', borderaxespad=0.)
          
          
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()