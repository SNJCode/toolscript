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

global_list={}
class MyPltQWidget(QWidget):
    def __init__(self, name,parent=None) :
        super().__init__(parent)
        self.ff=Figure(figsize=(5, 3))
        self.name=name
        self.static_canvas = FigureCanvas(self.ff)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.static_canvas)
        self._static_ax = self.static_canvas.figure.subplots()
   
    def set_df(self,data_list):
        for i in data_list:
            nn=np.array(i[1])
            self._static_ax.plot(nn[:,0],nn[:,1],label=i[0])
        self._static_ax.legend()
        self._static_ax.set_title(self.name)
        self.ff.savefig(self.name)
        

class TopWidget(QWidget):   
    def __init__(self,texta, parent=None) :
        super().__init__(parent) 
        layout = QHBoxLayout()
        self.texta=texta
        layout.addWidget(QLabel(parent=self,text=texta))
        button1 = QPushButton('Show Hide')
        layout.addWidget(button1)
        self.child=None
        button1.clicked.connect(lambda: self.showhide())
        self.child=MyWidget(self) 

        self.layout2 = QVBoxLayout()
        self.layout2.addLayout(layout)
        self.layout2.addWidget(self.child)
        self.setLayout( self.layout2 )

    def add_data(self,value):
        self.child.add_data(value)

    def get_data(self):
        return self.child.get_data()

    def get_texta(self):
        return self.texta
    
    def showhide(self):
        if not self.child.isVisible():
            self.child.show()
        else:
            self.child.hide()
   
     

###########

class MyWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)  
 
        self.ll=[]
        self.ro=0
        self.ro2=0
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # Add the QListWidget to a QVBoxLayout
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
        # Create the QLabel widgets
        xx=len(self.ll)
        label = QLabel(str(xx+1))
        label1 = QLabel(text)
        label1.adjustSize()
        self.ll.append(label1)
        label2 = QLabel()
        from PyQt5.QtCore import Qt
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet('background-color:{}'.format(col_list[col%len(col_list)]))
        button1 = QPushButton('Up')
        button1.clicked.connect(lambda: self.move_item_up(item))
        button1.pressed.connect(lambda: self.move_item_press(item))
        button2 = QPushButton('Down')
        button2.clicked.connect(lambda: self.move_item_down(item))
        button2.pressed.connect(lambda: self.move_item_press(item))
        layout.addWidget(label)
        # Add the QLabel widgets to the QHBoxLayout
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
        #item.setBackground(QColor(col))
        self.list_widget.addItem(item)
        self.resize(QSize(1000,600))

    def move_item_press(self, item):
        # Show a message box with the text of the clicked item
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
        for f,i in enumerate(data):
            self.add_item(i,f)

    def get_data(self):
        ret =[]
        for i in self.ll:
                ret.append(i.text())
        return ret

       
############################################################################################

#col_list=['#7F5A7C','#F3D5D7','#959CAC','#DC8389','#6B083E','#DF9045','#B83D1B'] 
############################################################################################
def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def read_4700(path):

    ex=pd.read_excel(path,usecols=[0,1])
 
        
    icc=0
    data_isok=False
    EXWL=''
    Scanmode=''
    EXSlit=''
    EMSlit=''
    for i,row,j in ex.itertuples():    
        if row == "Data points":
            data_isok=True
            break
        elif  row == "EX WL:":
            EXWL=j
        elif  row == "Scan mode:":
            Scanmode=j[:2]
        elif  row == "EX Slit:":
            EXSlit=j
        elif  row == "EM Slit:":
            EMSlit=j
        icc=icc+1


    if not data_isok:
        print (" file is error ")
        return False,None,''
    ex=pd.read_excel(path,header=icc+2,usecols=[0,1])
    ex.columns=['excited','indensity']
    ex=ex.astype(float)
    return True,ex,'Ex{}_Scan{}_ExSlit{}_EmSlit{}'.format(EXWL,Scanmode,EXSlit,EMSlit)


def read_1000(path):
    is_1000=False

    flag,df,re_s=read_4700(path)
    if not flag:
        is_1000=True
 
    if is_1000:
        df=pd.read_csv(path)
        start=df.iloc[2,:][1]
        end=df.iloc[3,:][1]
        step=df.iloc[4,:][1]
        ex_nm=df.iloc[5,:][1]
        slit=df.iloc[16,:][1]
        scan=df.iloc[0,:][1]
        re_s='Ex{}_Scan{}_Slit{}'.format(ex_nm,scan,slit)
        print(start,end,step)
        
        df=df.iloc[20:,:2]
        df.columns=['excited','indensity']
        df=df.astype(float)
    return df,re_s.replace('nm','').replace(' ','')

def set_origin_plot(data_list,gp,mxs):
    ex_list=[]
    icc=0
    for idx,i in enumerate(data_list):
        nn=np.array(i[1])
        #top_list.append(float(nn[:,1].max()))
        ex_list.append(float(nn[:,0].max()))
        ex_list.append(float(nn[:,0].min()))
        
        mxs.from_list(icc,nn[:,0].tolist(),lname=i[0],comments=i[0]+'_ex')
        icc+=1
        mxs.from_list(icc,nn[:,1].tolist(),lname=i[0],comments=i[0])
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

class show_widget(QDialog):
    def __init__(self):      
        super().__init__()
        self.layout2 = QVBoxLayout()
        self.setLayout(self.layout2)
        self.ll=[]

    def add_lay(self,w):
        self.layout2.addWidget(w)
        self.ll.append(w)

    def closeEvent(self, event):
        for i in self.ll:
            key= i.get_texta()
            value=i.get_data()
            global_list[key]=value

def get_limit():
    LimitRange=False
    x_min=0
    x_max=10000
    normalize=0
    is_nor=False
    is_smooth=False
    smooth_k,smooth_m=0,0
    while True:
        lr = input('Limit Range ')
        if lr =='q':
            quit()
        if  lr.isdigit():
            if int(lr) == 1:
                LimitRange=True
            break 
       
    if LimitRange:
        while True:
            x_min = input('X min ')
            if x_min =='q':
                quit()
            if  x_min.isdigit():
                break 
        while True:
            x_max = input('X max ')
            if x_max =='q':
                quit()
            if  x_max.isdigit():
                break 
        
        
        while True:
            normalize= input('is normalize ')
            if normalize=='q':
                quit()
            if  normalize.isdigit():
                if int(normalize) == 1:
                    is_nor=True
                    break
                else:
                    break
        
        while True:
            smooth = input('advandce smooth  obb num  or q return ')
            if smooth =='q':
                break
            tm=int(smooth)
            if tm%2 == 1 :
                smooth_m=tm
                smooth2 = input('advandce smooth  k  num  ')
                tk=int(smooth2)
                if tk >2 and tk < tm:
                    smooth_k=tk
                    is_smooth=True
                    break

    return LimitRange,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k

def get_file():
    file_dir=''
    file_list={}
    while True:
        if file_dir == '':
            files, filetype = QFileDialog.getOpenFileNames(filter="CSV File (*.CSV),xlsx File (*.xlsx);;All Files (*)")
        else:
            files, filetype = QFileDialog.getOpenFileNames(directory=file_dir,filter="CSV File (*.CSV),xlsx File (*.xlsx);;All Files (*)")
        for i in files:
            tp=os.path.splitext(i)[1]
            if tp == '.CSV' or tp == '.csv' or tp=='.xlsx':
                dirname=os.path.dirname(i)
                if file_dir == '':
                    file_dir=os.path.dirname(os.path.join(dirname,'..','..'))
                if not dirname in file_list.keys(): 
                    file_list[dirname]=[]
                if not i in file_list[dirname]:
                    file_list[dirname].append(i.replace(dirname,''))

        if len(files)==0:
            break
    return      file_list 

def copy_data_by_limit(data_list,data_list2,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k):
    for i in data_list:
        indx_df=i[1]
        dd=indx_df[indx_df["excited"].map(lambda x:x> float(x_min) and x < float(x_max))]
        nn=np.array(dd.loc[:,'indensity'])
        if is_nor:
            nn=normalization(nn)
        if  is_smooth:
            nn = scipy.signal.savgol_filter(nn,smooth_m,smooth_k) 
        dd.loc[:,'indensity']=nn
        data_list2.append((i[0],dd))            

 

class fileDialogdemo(QWidget):
    def __init__(self):      
        super().__init__()

        file_list=get_file()
        print(file_list)
        sw=show_widget()    
        for key, value in file_list.items():
            a=TopWidget(key,sw)
            a.add_data(value)
            sw.add_lay(a)
        sw.exec()

        plt_list=[]
        to_origin_list={}
        global_data_list=[]
        is_Multi_Fold=False
        while True:
            ooo = input('is show multi folder ')
            if ooo =='q':
                quit()
            if  ooo.isdigit():
                if int(ooo) == 1:
                    is_Multi_Fold=True
                    break
                else:
                    break

        for key, value in global_list.items():
            key_name=key.split('/')[-1]
            data_list=[]
            for i in value:
                path=key+i
                df,ex_nm=read_1000(path)
                data_list.append(   ( '{}_{}'.format(key_name,ex_nm)   ,df)  )
                global_data_list.append(  ( '{}_{}'.format(key_name,ex_nm)   ,df) )

            if is_Multi_Fold:
                data_top_list=[]
                data_top_list.append(('global',data_list))

                myplt=MyPltQWidget(key_name+'_global')
                myplt.set_df(data_list)
                myplt.setWindowTitle(key)
                if len(plt_list) > 0:
                    lastwi=plt_list[len(plt_list)-1]
                    myplt.move(lastwi.x()+int(lastwi.width()*1.1),myplt.y())
                myplt.show() 
                plt_list.append(myplt)

                while True:
                    print('current key file fold',key)
                    LimitRange,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k=get_limit()
                    if  LimitRange:
                        data_list2=[]            
                        copy_data_by_limit(data_list,data_list2,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k)
                        myplt2=MyPltQWidget('{}_normal_{}_smooth_{}_{}'.format(key_name,is_nor,smooth_m,smooth_k))
                        myplt2.set_df(data_list2)
                        myplt2.setWindowTitle(key)
                        plt_list.append(myplt2)
                        data_top_list.append(('normal_{}_smooth_{}_{}'.format(is_nor,smooth_m,smooth_k),data_list2))
                        for ip in plt_list:
                            ip.show()

                    ooo = input('num is break input ')
                    if ooo =='q':
                        quit()
                    if  ooo.isdigit():
                       break

                to_origin_list[key]=data_top_list
                         

        data_top_list=[]
        while True:
            ooo = input('is show one ')
            if ooo =='q':
                quit()
            if  ooo.isdigit():
                if int(ooo) == 1:
                    LimitRange,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k=get_limit()
                    data_list3=[]
                    copy_data_by_limit(global_data_list,data_list3,x_min,x_max,is_nor,is_smooth,smooth_m,smooth_k)
                    data_top_list.append(( 'normal_{}_smooth_{}_{}'.format(is_nor,smooth_m,smooth_k) ,data_list3))
                    myplt2=MyPltQWidget('All_normal_{}_smooth_{}_{}'.format(is_nor,smooth_m,smooth_k))
                    myplt2.set_df(data_list3)
                    myplt2.setWindowTitle('all')
                    plt_list.append(myplt2)
                    for ip in plt_list:
                        ip.show()
                else:
                    break
                                
              
        to_origin_list['global']=data_top_list           
        ooo = input('is open origin ')
        if ooo =='q':
            quit()      
        ###############################
        if platform.system ().lower () != 'windows':
            quit()
        op.set_show()
        fold_num_list=[]
        for key, value in to_origin_list.items():
            print(key,'lennnnn',len(value)) 
            if key !='global':
                name=key.split('/')[-1]
            else:
                name=key
            fold_num_list.append(key)
            op.pe.cd('/UNTITLED')
            op.pe.mkdir(name)
            op.pe.cd(name)
            for nm in value:
                mxs = op.new_sheet('w','w_{}'.format(nm[0]), hidden=False)
                gp = op.new_graph('g_{}'.format(nm[0]),template='LINE_plot3')
                set_origin_plot(nm[1],gp,mxs)
            op.pe.cd('/UNTITLED')

        
        input('sfsf')  
        ma
        quit()
   
           

import sys
if __name__=="__main__":
    app = QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())


