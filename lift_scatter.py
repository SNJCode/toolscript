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
from PyQt5.QtWidgets import QApplication,QPushButton,QDialog,QAbstractItemView,QLabel,QHBoxLayout, QWidget, QVBoxLayout, QListWidget,QListWidgetItem,QScrollArea
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
beishu=1000000
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

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare

colorlist=['red','green','purple','orange','black']
colorlist2=['pink','aquamarine','teal','gray','salmon']
beishu=1000000
t_bounds = (0, 10000*beishu)
y_bonds=1000
p0_num_b=200
p0_num_t=100*beishu
p0_num_y=1

def get_str(b1):
    return  str(round(b1,2)).ljust(20)

def read_1000(path):
    df=pd.read_csv(path,header=33)
    df=df.iloc[:,:2].astype(float)
    df.columns=['life','count']
    return df,df[df["count"].map(lambda x:x>0)]

def fun5(x,b1,b2,b3,b4,b5,t1,t2,t3,t4,t5,y0):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    z4=b4*np.exp(-x/t4)
    z5=b5*np.exp(-x/t5)
    return z1+z2+z3+z4+z5+y0

def fun4(x,b1,b2,b3,b4,t1,t2,t3,t4,y0):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    z4=b4*np.exp(-x/t4)
    return z1+z2+z3+z4+y0

def fun3(x,b1,b2,b3,t1,t2,t3,y0):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    return z1+z2+z3+y0

def fun2(x,b1,b2,t1,t2,y0):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    return z1+z2+y0

def fun1(x,b1,t1,y0):
    z1=b1*np.exp(-x/t1)
    return z1+y0
#####################
def afun5(x,b1,b2,b3,b4,b5,t1,t2,t3,t4,t5):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    z4=b4*np.exp(-x/t4)
    z5=b5*np.exp(-x/t5)
    return z1+z2+z3+z4+z5

def afun4(x,b1,b2,b3,b4,t1,t2,t3,t4):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    z4=b4*np.exp(-x/t4)
    return z1+z2+z3+z4

def afun3(x,b1,b2,b3,t1,t2,t3):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    z3=b3*np.exp(-x/t3)
    return z1+z2+z3

def afun2(x,b1,b2,t1,t2):
    z1=b1*np.exp(-x/t1)
    z2=b2*np.exp(-x/t2)
    return z1+z2

def afun1(x,b1,t1):
    z1=b1*np.exp(-x/t1)
    return z1

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


##############
class MyPltQWidget(QWidget):
    def __init__(self, name,parent=None) :
        super().__init__(parent)
        self.ff=Figure(figsize=(5, 3))
        self.name=name
        self.static_canvas = FigureCanvas(self.ff)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.static_canvas)
        self._static_ax = self.static_canvas.figure.subplots()
        self.fit_param=[]

    def get_fit_param(self):
        return pd.DataFrame(self.fit_param,columns=['graph','A','t','R2','RMSE','chi_test','life1','life2','y0'])

    def set_df(self,x,y,x2,y2,b_bounds,isp0b):
        self._static_ax.scatter(x2/beishu, np.log10(y2))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,1,fun1,True,isp0b))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,2,fun2,True,isp0b))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,3,fun3,True,isp0b))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,4,fun4,True,isp0b))
        self._static_ax.legend()
        self._static_ax.set_title(self.name)
        self._static_ax.set_ylim(-1,math.log10(y2.max())+1)

    def set_df2(self,x,y,x2,y2,b_bounds):
        self._static_ax.scatter(x2/beishu, np.log10(y2))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,1,afun1,False))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,2,afun2,False))
        self.fit_param.append(self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,3,afun3,False))
        self.fit_param.append( self.plot_fit(x,y,x2,y2,b_bounds,t_bounds,4,afun4,False))
        self._static_ax.legend()
        self._static_ax.set_title(self.name)
        self._static_ax.set_ylim(-1,math.log10(y2.max())+1)
     
    def plot_fit(self,x,y,x2,y2,b_bounds,t_bounds,num,func,isy0,isp0b):
        p0=[]
        first_ret=[]
        for i in range(num):
            first_ret.append(b_bounds[0])
            bb=int(b_bounds[0]/2)
            if isp0b:   
                if  p0_num_b > bb:
                    p0.append(bb)
                else:
                    p0.append(p0_num_b)
            else:
                p0.append(bb)

        for i in range(num):
            first_ret.append(t_bounds[0])
            p0.append(p0_num_t)
        if isy0:
            first_ret.append(-y_bonds)  
            p0.append(p0_num_y)

        second_ret=[]
        for i in range(num):
            second_ret.append(b_bounds[1])
        for i in range(num):
            second_ret.append(t_bounds[1])

        if isy0:
            second_ret.append(y_bonds) 

        bounds = (first_ret,second_ret)
        #if isp0b:
        popt, pcov = curve_fit(func, x, y,maxfev=5000000,bounds=bounds,p0=np.array(p0))
        #else:
        #    popt, pcov = curve_fit(func, x, y,maxfev=5000000,bounds=bounds)
        #popt, pcov = curve_fit(func, x, y,maxfev=5000000,p0=np.array(p0))
        chi_test=0
        yvals = func(x,*popt) 
        yvals2 = func(x2,*popt) 

        slist=[]
        for i in range(num):
            slist.append('b{}={}'.format(i,get_str(popt[i])))
        slist.append('\n')
        for i in range(num):
            slist.append('t{}={}'.format(i,get_str(popt[num+i]/beishu)))
        if isy0:
            slist.append('\n')
            slist.append('y0={}'.format(get_str(popt[num*2])))
        s=''
        for i in slist:
            s=s+i
        print('*'*20,str(b_bounds),'*'*20,'\n')
        print(s)
        
        ssr = ((yvals - y.mean())**2).sum() 
        sst = ((y - y.mean())**2).sum()  
        r2 = ssr/sst
        try:
            chi2, p = chisquare(y, yvals)
            chi_test='{:.2f}'.format(chi2/(x2.shape[0]- len(popt)))
        except:
            pass

        rmse= math.sqrt((((yvals - y)**2).sum()) /len(x))
        print('R2={:.2f} RMSE={:.2f} chi_test={}'.format(r2,rmse,chi_test))
        
        blist=[]
        tlist=[]
        for i in range(num):
            blist.append(popt[i])
            tlist.append(popt[i+num])

        blist=np.array(blist)
        tlist=np.array(tlist)
        anp=blist*(tlist**2)
        bnp=blist*tlist
        life=anp.sum()/bnp.sum()
    
        cnp=bnp/bnp.sum()
        dnp=cnp*(tlist**2)
        enp=cnp*tlist
        life2=dnp.sum()/enp.sum()
        print('life={:.2f} ms life2={:.2f} ms'.format(life/beishu,life2/beishu),'\n')
        color=colorlist[num-1]
        rss_str='{:.2f}'.format(rmse).ljust(7)
        tt_str='{:.2f}'.format(life/beishu).ljust(7)
        tt_str2='{:.2f}'.format(life2/beishu).ljust(7)
        print('*'*20,str(b_bounds),'*'*20,'\n')
        self._static_ax.plot(x2/beishu, np.log10(yvals2),color=color,label=str(num)+' R2={:.2f} RMSE={}'.format(r2,rss_str)+' t1={} chi={}'.format(tt_str,chi_test))  
        if isy0:
            return str(b_bounds),str(np.around(blist,decimals=2)),str(np.around(tlist/beishu,decimals=2)),'{:.2f}'.format(r2),rss_str,chi_test,tt_str,tt_str2,'{:.2f}'.format(popt[num*2])
        else:
            return str(b_bounds),str(np.around(blist,decimals=2)),str(np.around(tlist/beishu,decimals=2)),'{:.2f}'.format(r2),rss_str,chi_test,tt_str,tt_str2,'0'

def get_file():
    file_dir=''
    file_list=[]
    files, filetype = QFileDialog.getOpenFileNames(filter="CSV File (*.CSV);;xlsx File (*.xlsx);;All Files (*)")       
    for i in files:
        tp=os.path.splitext(i)[1]
        if tp == '.CSV' or tp == '.csv' or tp=='.xlsx':
                file_list.append(i)
    return  file_list 
        
class fileDialogdemo(QWidget):
    def __init__(self):      
        super().__init__()

        file_list=get_file()
        print(file_list,'\n')
        for i in file_list:
            name=os.path.basename(i)
            name=os.path.splitext(name)[0]
            self.setWindowTitle(name)
            df,df2=read_1000(i)
            x=np.array(df.iloc[1:,0]).reshape(-1).astype(float)
            y=np.array(df.iloc[1:,1]).reshape(-1).astype(float)
            x2=np.array(df2.iloc[1:,0]).reshape(-1).astype(float)
            y2=np.array(df2.iloc[1:,1]).reshape(-1).astype(float)
            qvt=QVBoxLayout()

            hb=QHBoxLayout()
            ret=[]
            ret2=[]
            num=128
            for j in [(0,num),(0,num*2),(0,num*4),(0,num*8),(0,num*16)]:
                qv=QVBoxLayout()
                name='bound='+str(j)
                myplt=MyPltQWidget(name+' intercept p0 True ',parent=self)
                myplt.set_df(x,y,x2,y2,j,True)
                ret.append(myplt.get_fit_param())
                qv.addWidget(myplt)
                '''myplt2=MyPltQWidget(name+' no intercept',parent=self)
                myplt2.set_df2(x,y,x2,y2,j)
                ret2.append(myplt2.get_fit_param())'''

                bond=(j[0],j[1]*32)
                name='bound='+str(bond)
                myplt2=MyPltQWidget(name+' intercept p0 True',parent=self)
                myplt2.set_df(x,y,x2,y2,bond,True)
                ret.append(myplt2.get_fit_param())
                qv.addWidget(myplt2)

                bond=(j[0],j[1]*32)
                name='bound='+str(bond)
                myplt3=MyPltQWidget(name+' intercept p0 False',parent=self)
                myplt3.set_df(x,y,x2,y2,bond,False)
                ret2.append(myplt3.get_fit_param())
                qv.addWidget(myplt3)

  


                hb.addLayout(qv)

            qvt.addLayout(hb)
            qv2=QHBoxLayout()
            a=QTableView(self)
            a.setModel(pandasModel(pd.concat(ret)))
            a2=QTableView(self)
            a2.setModel(pandasModel(pd.concat(ret2)))    
            qv2.addWidget(a)
            qv2.addWidget(a2)
            qvt.addLayout(qv2)
            self.setLayout(qvt)
            break
        
import sys
if __name__=="__main__":
    app = QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.showMaximized()
    ex.show()
    sys.exit(app.exec_())


