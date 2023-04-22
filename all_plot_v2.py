import os
import platform
if platform.system ().lower () == 'windows':
    import originpro as op
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog,QWidget,QApplication
import matplotlib.pylab as plt
import scipy
import sys
from PyQt5.QtWidgets import QApplication,QPushButton,QDialog,QAbstractItemView,QLabel,QHBoxLayout, QWidget, QVBoxLayout, QListWidget,QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas

class MyPltQWidget(QWidget):
    def __init__(self, parent=None) :
        super().__init__(parent)
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(static_canvas)
        self._static_ax = static_canvas.figure.subplots()

    def set_df(self,data_list):
        for i in data_list:
            nn=np.array(i[1])
            norlist=normalization(nn[:,1])
            self._static_ax.plot(nn[:,0],norlist,label=i[0])
        self._static_ax.legend()
        
global_list=[]
class MyWidget(QDialog):
    def __init__(self):
        super().__init__()    
        self.ll=[]
        self.ro=0
        self.ro2=0
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        
        layout = QVBoxLayout()
        self.ti=300
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.timer = QTimer()  
        self.timer.timeout.connect(self.time)
        self.timer2 = QTimer()  
        self.timer2.timeout.connect(self.time2)

    def add_item(self, text,col):
        # Create a QListWidgetItem with the given text and add it to the list widget
        item = QListWidgetItem(self.list_widget)
        widget=QWidget(self.list_widget)   
        layout = QHBoxLayout()
    
        label = QLabel(str(len(self.ll)+1))
        label1 = QLabel(text)
        label1.adjustSize()
        self.ll.append(label1)
        label2 = QLabel()
        from PyQt5.QtCore import Qt
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet('background-color:{}'.format(col))
        button1 = QPushButton('Up')
        button1.clicked.connect(lambda: self.move_item_up(item))
        button1.pressed.connect(lambda: self.move_item_press(item))
        button2 = QPushButton('Down')
        button2.clicked.connect(lambda: self.move_item_down(item))
        button2.pressed.connect(lambda: self.move_item_press(item))
        layout.addWidget(label)
        layout.addWidget(label1)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(label2)
        layout.setStretchFactor(label, 1)
        layout.setStretchFactor(label1, 3)
        layout.setStretchFactor(button1, 1)
        layout.setStretchFactor(button2, 1)
        layout.setStretchFactor(label2, 1)
        widget.setLayout(layout)
        self.list_widget.setItemWidget(item, widget)
        item.setSelected(False)
        item.setSizeHint(QSize(self.list_widget.width(),50))
        
        self.list_widget.addItem(item)
        self.resize(QSize(1000,600))
        
    def move_item_press(self, item):
        row = self.list_widget.row(item)
        self.ll[row].setStyleSheet('background-color:rgba(0, 132, 255)')
        self.timer2.start(self.ti)
        self.ro2=row
    
    def move_item_up(self, item):
        row = self.list_widget.row(item)
        if row > 0:
            last=self.ll[row-1]
            current=self.ll[row]
            la=last.text()
            cu=current.text()
            last.setText(cu)
            current.setText(la)
            self.ll[row-1].setStyleSheet('background-color:rgba(0, 132, 255)')
            self.timer.start(self.ti)
            self.ro=row-1

    def time(self):
        self.ll[self.ro].setStyleSheet('background-color:white')        

    def time2(self):
        self.ll[self.ro2].setStyleSheet('background-color:white')       

    def move_item_down(self, item):
        row = self.list_widget.row(item)
        max=len(self.ll)
        if row < max-1:
            last=self.ll[row+1]
            current=self.ll[row]
            la=last.text()
            cu=current.text()
            last.setText(cu)
            current.setText(la)
            self.ll[row+1].setStyleSheet('background-color:rgba(0, 132, 255)')
            self.ro=row+1
            self.timer.start(self.ti)
            
    def add_data(self,data):
        for i in data:
            self.add_item(i[0],i[1])

    def closeEvent(self, event):
        for i in self.ll:
                global_list.append(i.text())
       
############################################################################################
col_list=['#df9dc0'
 ,'#5f7cdb'
 ,'#312d50'
 ,'#62599d'
 ,'#87547a'
 ,'#0e0b13'
 ,'#aaacf1'
 ,'#ac8cb4'
 ,'#685c84'
 ,'#b4445c']
#col_list=['#7F5A7C','#F3D5D7','#959CAC','#DC8389','#6B083E','#DF9045','#B83D1B'] 
############################################################################################
def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def read_1000(path):
    df=pd.read_csv(path)
    start=df.iloc[2,:][1]
    end=df.iloc[3,:][1]
    step=df.iloc[4,:][1]
    ex_nm=df.iloc[5,:][1]
    print(start,end,step)
    
    df=df.iloc[20:,:2]
    df.columns=['excited','indensity']
    df=df.astype(float)
    return df,int(float(ex_nm))

def set_origin_plot(data_list,num,k,gp,mxs):
    ex_list=[]
    icc=0
    for idx,i in enumerate(data_list):
        nn=np.array(i[1])
        #top_list.append(float(nn[:,1].max()))
        ex_list.append(float(nn[:,0].max()))
        ex_list.append(float(nn[:,0].min()))
        
        mxs.from_list(icc,nn[:,0].tolist(),lname=i[0],comments=i[0]+'_ex')
        icc+=1
        if num > 0:
            norlist=normalization(nn[:,1]) 
            y_smooth = scipy.signal.savgol_filter(norlist,num,k)  
        else:
            y_smooth=nn[:,1]
        mxs.from_list(icc,y_smooth.tolist(),lname=i[0],comments=i[0])
        icc+=1
        p=gp[0].add_plot(mxs,icc-1,icc-2,type='l')
        p.color=col_list[idx%len(col_list)]
        
    xl=int(min(ex_list)-100)
    xl=xl-xl%100
    xm=int(max(ex_list)+100)
    xm=xm-xm%100
    st=(xm-xl)/5
    st=st-st%100
    gp[0].set_xlim(xl,xm ,step=st)
    gp[0].set_ylim(-0.02, 1.2)
    gp[0].rescale('x')
    
class fileDialogdemo(QWidget):
    def __init__(self):      
        super().__init__()
        data_list=[]
        file_list=[]
        while True:
            files, filetype = QFileDialog.getOpenFileNames()
            for i in files:
                tp=os.path.splitext(i)[1]
                if tp == '.CSV' or tp == '.csv':
                    if not i in file_list:
                        file_list.append(i)
            if len(files)==0:
                break
        print(file_list)
        w_list=[]
        for k,i in enumerate(file_list):
                w_list.append((i,col_list[k%len(col_list)]))    

        widget = MyWidget()
        widget.add_data(w_list)
        widget.exec()
        print(global_list)
        for i in global_list:    
            df,ex_nm=read_1000(i)
            ss=os.path.dirname(i)  
            nm=ss.split('/')[-1]+'_Ex-{}'.format(ex_nm)          
            data_list.append((nm,df))
        #print(data_list)

        myplt=MyPltQWidget()
        myplt.set_df(data_list)
        myplt.show()

        while True:
            while True:
                x_min = input('X min, input num or q is quit ')
                if x_min =='q':
                    quit()
                if  x_min.isdigit():
                    break 

            while True:
                x_max = input('X max, input num or q is quit ')
                if x_max =='q':
                    quit()
                if  x_max.isdigit():
                    break 

            data_list2=[]
            for i in data_list:
                indx_df=i[1]
                dd=indx_df[indx_df["excited"].map(lambda x:x> float(x_min) and x < float(x_max))]
                data_list2.append((i[0],dd))

            myplt2=MyPltQWidget()
            myplt2.set_df(data_list2)
            myplt2.show()
            myplt.show()
            
            is_origin = input('is quit open origin,input q or other ')
            if  is_origin =='q':
                break         
        ###############################
        if platform.system ().lower () != 'windows':
            quit()
        op.set_show()
        mxs = op.new_sheet('w',' source  Product', hidden=False)
        gp = op.new_graph('plot_source ',template='LINE_plot')
        set_origin_plot(data_list,0,0,gp,mxs)

        mxs = op.new_sheet('w',' x limit normal Product', hidden=False)
        gp = op.new_graph('x limit plot_source ',template='LINE_plot')
        set_origin_plot(data_list2,21,3,gp,mxs)
        
        while True:
                obb_num = input('smooth  obb num, input num or q is quit  ')
                if obb_num =='q':
                    break
                tm=int(obb_num)
                if tm%2 == 1 :
                    #********************************************
                    k_num = input('smooth  k  num, input num or q is quit  ')
                    tk=int(k_num)
                    if tk >2 and tk < tm:
                        mxs = op.new_sheet('w','x limit normal Product {}_{}'.format(tm,tk), hidden=False)
                        gp = op.new_graph('plot_g {}_{}'.format(tm,tk),template='LINE_plot')
                        set_origin_plot(data_list2,tm,tk,gp,mxs)
                
                #****************************
        ma
        quit()
   
           

import sys
if __name__=="__main__":
    app = QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())


