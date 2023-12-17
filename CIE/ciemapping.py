import colour
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from adjustText import adjust_text

import sys 
xmap5='0'
xmap1='0'
xmap2='0'
xmap3='0'
xmap4='0'

arglist=sys.argv[2:]
if len(arglist)==5:
    try:
        xmap1=float(arglist[0])
    except:
        xmap1='0'
    try:
        xmap2=float(arglist[1])
    except:
        xmap2='0'
    try:
        xmap3=float(arglist[2])
    except:
        xmap3='0'
    try:
        xmap4=float(arglist[3])
    except:
        xmap4='0'    
    try:
        xmap5=float(arglist[4])
    except:
        xmap5='0'
elif len(arglist)==4:
    try:
        xmap1=float(arglist[0])
    except:
        xmap1='0'
    try:
        xmap2=float(arglist[1])
    except:
        xmap2='0'
    try:
        xmap3=float(arglist[2])
    except:
        xmap3='0'
    try:
        xmap4=float(arglist[3])
    except:
        xmap4='0' 
elif len(arglist)==1:
    try:
        xmap5=float(arglist[0])
    except:
        xmap5='0'
          
    
print(arglist)  
print(xmap1,xmap2,xmap3,xmap4,xmap5)


#############


from tkinter import font
import pandas as pd
import matplotlib.pylab as plt
import  numpy as np
from matplotlib import colors
import platform
if platform.system ().lower () == 'windows':
    import originpro as op

global_range_list=[]

def get_max_map(df,heat_map,row_list,col_list):
    row_index,col_index,max_size=get_max_df(df)
    row_index_v= row_list.index(row_index)
    col_index_v= col_list.index(col_index)
    heat_map.plot([col_index_v,col_index_v],[0,row_index_v],'--',linewidth=3,color='white')
    heat_map.plot([0,col_index_v],[row_index_v,row_index_v],'--',linewidth=3,color='white')
    return row_index,col_index,max_size   

def get_max_df(df):
    maxValueIndex = df.idxmax()
    max_size=0
    row_index=0
    col_index=0
    is_First=True
    
    for v in maxValueIndex.items():
        x=df.loc[v[1],v[0]]
        if is_First:
            max_size = x
            is_First=False
            row_index=v[1]
            col_index=v[0]
        else:
            if max_size < x:
                max_size = x
                row_index=v[1]
                col_index=v[0]

    #print(row_index,col_index,max_size)
    return row_index,col_index,max_size

##############################################################################################################
def find_df_borden(df,col_min,col_max,row_min,row_max,min_top,max_col,max_row,source_col,source_row):
    step=0
    while True:
        if col_max+step < max_col:
            next_col_value=df.iloc[source_row,col_max+step]
            if next_col_value > min_top:
                step+=1
                continue
            else:
                col_max=col_max+step
                break
        else:
            col_max=col_max+step-1
            break

    step=0

    while True:
        if col_min-step > 0 :
            next_col_value=df.iloc[source_row,col_min-step]
            if next_col_value > min_top:
                step+=1
                continue
            else:
                col_min=col_min-step
                break
        else:
            col_min=col_min-step
            break   
  
    #****************************
    step=0
    while True:
        if row_max+step < max_row:
            next_row_value=df.iloc[row_max+step,source_col]
            if next_row_value > min_top:
                step+=1

                continue
            else:
                row_max=row_max+step
                break
        else:
            row_max=row_max+step-1
            break

    step=0
    while True:
        if row_min-step >0 :
            next_row_value=df.iloc[row_min-step,source_col]
            if next_row_value > min_top:
                step+=1
                continue
            else:
                row_min=row_min-step
                break
        else:
            row_min=row_min-step
            break 
    
    return     col_min,col_max,row_min,row_max 



def spread_area(df,col_min,col_max,row_min,row_max,max_col,max_row,max_size):
    
    left=df.iloc[row_min:row_max,col_min]
    #print(left.max(),max_size)
    if left.max() > max_size:
        if col_min -1 > 0:
            col_min=col_min-1
        else:
            col_min=0
    
    right=df.iloc[row_min:row_max,col_max]
    
    if right.max() > max_size:
        if col_max +1 < max_col:
            col_max=col_max+1
        else:
            col_max=max_col-1

    top=df.iloc[row_min,col_min:col_max]
    if top.max() > max_size:
        if row_min -1 > 0:
            row_min=row_min-1
        else:
            row_min=0
    
    bottom=df.iloc[row_max,col_min:col_max]
    if bottom.max() > max_size:
        if row_max +1 < max_row:
            row_max=row_max+1
        else:
            row_max=max_row-1
    return col_min,col_max,row_min,row_max

def del_area(df,row_index,col_index,max_size,heat_map,i):
    col_list2=list(df.columns)
    row_list2=list(df.index)
    col_min,col_max,row_min,row_max=find_nerigh(df,row_index,col_index,max_size)
    print('del_area',col_list2[col_min],col_list2[col_max],row_list2[row_min],row_list2[row_max])
    color_list=['white','red','black','purple']
    print('white','red','black','purple')
    co=color_list[i%len(color_list)]
    heat_map.plot([col_min,col_max+1],[row_min,row_min],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_max+1],[row_max+1,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_min],[row_min,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_max+1,col_max+1],[row_min,row_max+1],'--',linewidth=3,color=co)
    return col_list2[col_min],col_list2[col_max],row_list2[row_min],row_list2[row_max]


def find_nerigh(df,row,col,max_size):
    col_list=list(df.columns)
    row_list=list(df.index)
    #print('find_nerigh',col,col_list)
    #try:
    source_col=col_list.index(col)
    source_row=row_list.index(row)
    #except:
        #source_col=col_list.index(row)
        #source_row=row_list.index(col)
    max_col=len(col_list)
    max_row=len(row_list)
  
    min_top=max_size*0.1
    
    col_min=source_col
    col_max=source_col
    row_min=source_row
    row_max=source_row

    col_min,col_max,row_min,row_max=find_df_borden(df,col_min,col_max,row_min,row_max,min_top,max_col,max_row,source_col,source_row)
    while True:
        #print('aaaaa',col_min,col_max,row_min,row_max,max_col,max_row,min_top)
        _col_min,_col_max,_row_min,_row_max=spread_area(df,col_min,col_max,row_min,row_max,max_col,max_row,min_top)
        #print('bbbb',_col_min,_col_max,_row_min,_row_max,max_col,max_row,min_top)
        if _col_min == col_min and _col_max == col_max and _row_min == row_min and _row_max == row_max:
            col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max
            break
        #print('is diff')
        col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max

    for i in range(col_min,col_max+1):
        for j in range(row_min,row_max+1):
            df.iloc[j,i]=0
    #print('end area',col_min,col_max,row_min,row_max)
    return     col_min,col_max,row_min,row_max 

##############################################################################################################

def get_add_point_df(df):
    xl=len(list(df.columns))
    col_list=df.columns.values
    row_list=df.index.values
    con_list=[df]
    for col in  range(xl-1):
        current_col=col
        x1=df.iloc[:,current_col]
        x1_col=col_list[col]
        x2=df.iloc[:,current_col+1]
        x2_col=col_list[col+1]

        x1_np=np.array(x1.values.tolist())
        x2_np=np.array(x2.values.tolist())
        x3=(x1_np+x2_np)/2
        ss=pd.DataFrame(x3,columns=[(x1_col+x2_col)/2],index=row_list)
        con_list.append(ss)
        
    df=pd.concat(con_list,join='inner', axis=1, sort=False)
    
    col_list=list(df.columns)
    col_list.sort()
    df=df.loc[:,col_list]
    return df

def add_point_df(df):
    r=get_add_point_df(df)
    x=get_add_point_df(r.T)
    return x.T
##############################################################################################################
def read_ex(path):
    
    df,flag=read_4700(path)
    if flag:
        return df
    else:
        return read_1000(path)
                    
    
            
def read_1000(path):
    df=pd.read_csv(path)
    ret=[]
    for i in df.index:
        tmp=[]
        for j in i:
            tmp.append(j)
        ret.append(tmp)


    rep=np.array(ret)
    col=np.array(rep[6,1:]).astype(float)
    row=np.array(rep[21:,0]).astype(float)

    val=np.array(rep[21:,1:])
    val[np.where(val==' ')]=0
    val=val.astype(float)
    f=pd.DataFrame(val,columns=col,index=row)
    return f.T

def read_4700(path):
    try:
        ex=pd.read_excel(path,usecols=[0])
    except:
        print('read 4700 error')
        return '',False
        
    icc=0
    data_isok=False

    for i,row in ex.itertuples():
            if row == "Data points":
                data_isok=True
                break
            icc=icc+1

    if not data_isok:
        print (" file is error ")
        return _,False
    ex=pd.read_excel(path,header=icc+2,index_col=0)
    ex=ex.astype(float)
    #print(ex2)
    return ex.T,True

##############################################################################################################
   
def origin(df_global,df,row_index,col_index,name):
    op.set_show()
    dd=np.array(df_global)
    row=np.array(list(df_global.index)).reshape(-1).astype(float)
    col=np.array(list(df_global.columns)).reshape(-1).astype(float)
    print('----col.min(),col.max(),row.min(),row.max()--------',col.min(),col.max(),row.min(),row.max())
    #新建矩阵表
    mxs = op.new_sheet('m','global_{}'.format(name), hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    #新建热图
    gp = op.new_graph('mapping global',template='heatmap2')
    p=gp[0].add_plot(mxs, colz=0)
    #调整热图坐标
    gp[0].set_xlim(col.min(), col.max())
    gp[0].set_ylim(row.min(), row.max())
    gp[0].rescale('z')
    #调整热图标尺
    z = p.zlevels
    z['minors'] = 100
    z['levels'] = [dd.min(), 0, dd.max()]
    p.zlevels = z
    #第二个热图
    dd=np.array(df)
    row=np.array(list(df.index)).reshape(-1).astype(float)
    col=np.array(list(df.columns)).reshape(-1).astype(float)
    mxs = op.new_sheet('m','Product_{}' .format(name), hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    mapping_name='mapping_{}_{}'.format(int(row_index),int(col_index))
    gp = op.new_graph(mapping_name,template='heatmap4')
    p=gp[0].add_plot(mxs, colz=0)
    gp[0].rescale('z')
    gp[0].set_xlim(col.min(), col.max())
    gp[0].set_ylim(row.min(), row.max())
    z = p.zlevels
    z['minors'] = 100
    z['levels'] = [dd.min(), 0, dd.max()]
    p.zlevels = z
    print('max_peek',row_index,col_index)
    print('*'*30,'\n')
    
    #划线图形
    k=[]
    k.append('GObject myLine = [{}]1!line1;'.format(mapping_name))
    k.append('draw -n myLine -lm {'  + '{},{},{},{}'.format(col.min(),row_index,col_index,row_index)+'} ;'  )
    k.append('''myLine.lineType=2;
myLine.linewidth=3;
myLine.color=color(white);''')

    k.append('GObject myLine2 = [{}]1!line2;'.format(mapping_name))
    k.append('draw -n myLine2 -lm {'  + '{},{},{},{}'.format(col_index,row.min(),col_index,row_index)+'} ;'  )
    k.append('''myLine2.lineType=2;
myLine2.linewidth=3;
myLine2.color=color(white);''')
    
    for i in k:
        gp.lt_exec(i)
        print(i)
            
    print('*'*30,'\n')
    ma
    op.exit() 
##############################################################################################################     
def color_bar():
	uip=['#0000FF']
	for x in range(1,12):
		a='#00'+str(hex(x*21))[2:]+'FF'
		#print(a)
		uip.append(a)
	for x in range(1,12):
		a='#00FF'+str(hex(255-x*21))[2:]
		#print(a)
		uip.append(a)
	uip.append('#00FF00')
	for x in range(1,12):
		a='#'+str(hex(x*21))[2:]+'FF00'
		#print(a)
		uip.append(a)
	uip.append('#FFFF00')
	for x in range(1,12):
		a='#FF'+str(hex(255-x*21))[2:]+'00'
		#print(a)
		uip.append(a)
	return uip

##############################################################################################################
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas



class MyQWidget(QWidget):
    def __init__(self, parent=None) :
        super().__init__(parent)
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(static_canvas)
        self._static_ax = static_canvas.figure.subplots()

    def set_df(self,df,num):
        row_list=list(df.index)
        col_list=list(df.columns)
        print('data row col',len(row_list),len(col_list))
        xla=int(len(row_list)/5)
        yla=int(len(col_list)/5)
        import seaborn as sns
        cmap = colors.ListedColormap(color_bar())
        heat_map = sns.heatmap( df ,cmap=cmap,square=False,ax=self._static_ax ,yticklabels=xla,xticklabels=yla)
        heat_map.invert_yaxis()
        
        if num > 0:
            global_range_list.clear()
            for i in range(num):
                row_index,col_index,max_size=get_max_df(df)#get_max_map(df,heat_map,row_list,col_list)
                global_range_list.append(del_area(df,row_index,col_index,max_size,heat_map,i))
        else:
            row_index,col_index,max_size=get_max_map(df,heat_map,row_list,col_list)

        return   row_index,col_index

def get_min(df,xmin,xmax):
    xmin=int(xmin)
    xmax=int(xmax)
    x_list=np.array(list(df.columns))
    #y_list=df.index.values
    col=df.columns.values
    if xmin < x_list.max():
        target_res=x_list >= xmin-(x_list[1]-x_list[0])
    else:
        target_res=np.ones(len(col), dtype=bool)

    if xmax > x_list.min():
        target_res2=x_list<= xmax+(x_list[1]-x_list[0])
    else:
        target_res2=np.ones(len(col), dtype=bool)

    target= target_res & target_res2
    l=[]
    for i,v  in enumerate(target):
        if v:
            l.append(col[i])
    return df.loc[:,l]
    
def get_ymin(df,ymin,ymax):
    ymin=int(ymin)
    ymax=int(ymax)
    x_list=np.array(list(df.index))
    #y_list=df.index.values
    col=df.index.values
    if ymin < x_list.max():
        target_res=x_list >= ymin-(x_list[1]-x_list[0])
    else:
        target_res=np.ones(len(col), dtype=bool)

    if ymax > x_list.min():
        target_res2=x_list<= ymax+(x_list[1]-x_list[0])
    else:
        target_res2=np.ones(len(col), dtype=bool)
  
    target= target_res & target_res2
    l=[]
    for i,v  in enumerate(target):
        if v:
            l.append(col[i])
    return df.loc[l,:]
    
def get_range(df):
    is_choose_peek=False
    is_choose_peek_num=0
    while True:
            x_min = input('X min ')
            if x_min =='q':
                quit()
            if 'p' in x_min:
                is_choose_peek=True
                x_min=int(x_min[1:].strip())
                is_choose_peek_num=x_min
                break
            if  x_min.isdigit():
               break 
    if not is_choose_peek:
        while True:
            x_max = input('X max ')
            if x_max =='q':
                quit()
            if  x_max.isdigit():
                break 

        while True:
            y_min = input('Y min ')
            if y_min =='q':
                quit()
            if  y_min.isdigit():
                break        
        
        while True:
            y_max = input('Y max ')
            if y_max =='q':
                quit()
            if  y_max.isdigit():
                break  
    else:
        x_min,x_max,y_min,y_max=global_range_list[(is_choose_peek_num-1)%len(global_range_list)]

    
    while True:
        grid_num= input('input grid num 0-3 ')
        if grid_num == 'q':
            quit()
        if  grid_num.isdigit():
            if int(grid_num) < 4:
                break   

    df=get_min(df,x_min,x_max)
    df=get_ymin(df,y_min,y_max)

    for i in range(int(grid_num)):
        df=add_point_df(df)
        df=add_point_df(df)

    return df


import os
def read_d(path,pa):
    file_name_top=os.path.splitext(os.path.basename(path))[0]
    import copy
    df_global=read_ex(path)
    df_g=copy.deepcopy(df_global)
    while True:
        peek = input('show top peek ')
        if peek =='q':
            quit()
        if  peek.isdigit():
            break  

    global_sd=MyQWidget()
    global_sd.set_df(df_g,int(peek))
    global_sd.show()

   
    sd_window=None
    for i in range(100):  
        df_g=copy.deepcopy(df_global)
        df=get_range(df_g)
        is_okt=False
        while True:
            peek = input('show top peek ')
            if peek =='q':
                quit()
            if  peek.isdigit():
                break  
            
               

        if not sd_window is None:
            sd_window.close()
        sd_window=MyQWidget()
        r,c=sd_window.set_df(df,int(peek))
        sd_window.show()
        global_sd.show()

    while True:
        x_min = input('quit select value  ')
        if x_min =='q':
            quit()
        if  int(x_min)==0: 
            return

class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        
        super(fileDialogdemo, self).__init__(parent)
        #self.layout = QtWidgets.QVBoxLayout(self)
        #实例化QFileDialog
        dig=QFileDialog()
        if dig.exec():
            filenames=dig.selectedFiles()
            print(filenames)
            print(filenames[0])
            dig.close()

        read_d(filenames[0],self)
        
    #def get_lay(self):
     #    return self.layout
           



from tkinter import font
import pandas as pd
import matplotlib.pylab as plt
import  numpy as np
from matplotlib import colors
import platform
if platform.system ().lower () == 'windows':
    import originpro as op

global_range_list=[]

def get_max_map(df,heat_map,row_list,col_list):
    row_index,col_index,max_size=get_max_df(df)
    row_index_v= row_list.index(row_index)
    col_index_v= col_list.index(col_index)
    heat_map.plot([col_index_v,col_index_v],[0,row_index_v],'--',linewidth=3,color='white')
    heat_map.plot([0,col_index_v],[row_index_v,row_index_v],'--',linewidth=3,color='white')
    return row_index,col_index,max_size   

def get_max_df(df):
    maxValueIndex = df.idxmax()
    max_size=0
    row_index=0
    col_index=0
    is_First=True
    
    for v in maxValueIndex.items():
        x=df.loc[v[1],v[0]]
        if is_First:
            max_size = x
            is_First=False
            row_index=v[1]
            col_index=v[0]
        else:
            if max_size < x:
                max_size = x
                row_index=v[1]
                col_index=v[0]

    #print(row_index,col_index,max_size)
    return row_index,col_index,max_size

##############################################################################################################
def find_df_borden(df,col_min,col_max,row_min,row_max,min_top,max_col,max_row,source_col,source_row):
    step=0
    while True:
        if col_max+step < max_col:
            next_col_value=df.iloc[source_row,col_max+step]
            if next_col_value > min_top:
                step+=1
                continue
            else:
                col_max=col_max+step
                break
        else:
            col_max=col_max+step-1
            break

    step=0

    while True:
        if col_min-step > 0 :
            next_col_value=df.iloc[source_row,col_min-step]
            if next_col_value > min_top:
                step+=1
                continue
            else:
                col_min=col_min-step
                break
        else:
            col_min=col_min-step
            break   
  
    #****************************
    step=0
    while True:
        if row_max+step < max_row:
            next_row_value=df.iloc[row_max+step,source_col]
            if next_row_value > min_top:
                step+=1

                continue
            else:
                row_max=row_max+step
                break
        else:
            row_max=row_max+step-1
            break

    step=0
    while True:
        if row_min-step >0 :
            next_row_value=df.iloc[row_min-step,source_col]
            if next_row_value > min_top:
                step+=1
                continue
            else:
                row_min=row_min-step
                break
        else:
            row_min=row_min-step
            break 
    
    return     col_min,col_max,row_min,row_max 



def spread_area(df,col_min,col_max,row_min,row_max,max_col,max_row,max_size):
    
    left=df.iloc[row_min:row_max,col_min]
    #print(left.max(),max_size)
    if left.max() > max_size:
        if col_min -1 > 0:
            col_min=col_min-1
        else:
            col_min=0
    
    right=df.iloc[row_min:row_max,col_max]
    
    if right.max() > max_size:
        if col_max +1 < max_col:
            col_max=col_max+1
        else:
            col_max=max_col-1

    top=df.iloc[row_min,col_min:col_max]
    if top.max() > max_size:
        if row_min -1 > 0:
            row_min=row_min-1
        else:
            row_min=0
    
    bottom=df.iloc[row_max,col_min:col_max]
    if bottom.max() > max_size:
        if row_max +1 < max_row:
            row_max=row_max+1
        else:
            row_max=max_row-1
    return col_min,col_max,row_min,row_max

def del_area(df,row_index,col_index,max_size,heat_map,i):
    col_list2=list(df.columns)
    row_list2=list(df.index)
    col_min,col_max,row_min,row_max=find_nerigh(df,row_index,col_index,max_size)
    print('del_area',col_list2[col_min],col_list2[col_max],row_list2[row_min],row_list2[row_max])
    color_list=['white','red','black','purple']
    print('white','red','black','purple')
    co=color_list[i%len(color_list)]
    heat_map.plot([col_min,col_max+1],[row_min,row_min],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_max+1],[row_max+1,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_min],[row_min,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_max+1,col_max+1],[row_min,row_max+1],'--',linewidth=3,color=co)
    return col_list2[col_min],col_list2[col_max],row_list2[row_min],row_list2[row_max]


def find_nerigh(df,row,col,max_size):
    col_list=list(df.columns)
    row_list=list(df.index)
    #print('find_nerigh',col,col_list)
    #try:
    source_col=col_list.index(col)
    source_row=row_list.index(row)
    #except:
        #source_col=col_list.index(row)
        #source_row=row_list.index(col)
    max_col=len(col_list)
    max_row=len(row_list)
  
    min_top=max_size*0.1
    
    col_min=source_col
    col_max=source_col
    row_min=source_row
    row_max=source_row

    col_min,col_max,row_min,row_max=find_df_borden(df,col_min,col_max,row_min,row_max,min_top,max_col,max_row,source_col,source_row)
    while True:
        #print('aaaaa',col_min,col_max,row_min,row_max,max_col,max_row,min_top)
        _col_min,_col_max,_row_min,_row_max=spread_area(df,col_min,col_max,row_min,row_max,max_col,max_row,min_top)
        #print('bbbb',_col_min,_col_max,_row_min,_row_max,max_col,max_row,min_top)
        if _col_min == col_min and _col_max == col_max and _row_min == row_min and _row_max == row_max:
            col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max
            break
        #print('is diff')
        col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max

    for i in range(col_min,col_max+1):
        for j in range(row_min,row_max+1):
            df.iloc[j,i]=0
    #print('end area',col_min,col_max,row_min,row_max)
    return     col_min,col_max,row_min,row_max 

##############################################################################################################

def get_add_point_df(df):
    xl=len(list(df.columns))
    col_list=df.columns.values
    row_list=df.index.values
    con_list=[df]
    for col in  range(xl-1):
        current_col=col
        x1=df.iloc[:,current_col]
        x1_col=col_list[col]
        x2=df.iloc[:,current_col+1]
        x2_col=col_list[col+1]

        x1_np=np.array(x1.values.tolist())
        x2_np=np.array(x2.values.tolist())
        x3=(x1_np+x2_np)/2
        ss=pd.DataFrame(x3,columns=[(x1_col+x2_col)/2],index=row_list)
        con_list.append(ss)
        
    df=pd.concat(con_list,join='inner', axis=1, sort=False)
    
    col_list=list(df.columns)
    col_list.sort()
    df=df.loc[:,col_list]
    return df

def add_point_df(df):
    r=get_add_point_df(df)
    x=get_add_point_df(r.T)
    return x.T
##############################################################################################################
def read_ex(path):
    
    df,flag=read_4700(path)
    if flag:
        return df
    else:
        return read_1000(path)
                    
    
            
def read_1000(path):
    df=pd.read_csv(path)
    ret=[]
    for i in df.index:
        tmp=[]
        for j in i:
            tmp.append(j)
        ret.append(tmp)


    rep=np.array(ret)
    col=np.array(rep[6,1:]).astype(float)
    row=np.array(rep[21:,0]).astype(float)

    val=np.array(rep[21:,1:])
    val[np.where(val==' ')]=0
    val=val.astype(float)
    f=pd.DataFrame(val,columns=col,index=row)
    return f.T

def read_4700(path):
    try:
        ex=pd.read_excel(path,usecols=[0])
    except:
        print('read 4700 error')
        return '',False
        
    icc=0
    data_isok=False

    for i,row in ex.itertuples():
            if row == "Data points":
                data_isok=True
                break
            icc=icc+1

    if not data_isok:
        print (" file is error ")
        return _,False
    ex=pd.read_excel(path,header=icc+2,index_col=0)
    ex=ex.astype(float)
    #print(ex2)
    return ex.T,True

##############################################################################################################
   
def origin(df_global,df,row_index,col_index,name):
    op.set_show()
    dd=np.array(df_global)
    row=np.array(list(df_global.index)).reshape(-1).astype(float)
    col=np.array(list(df_global.columns)).reshape(-1).astype(float)
    print('----col.min(),col.max(),row.min(),row.max()--------',col.min(),col.max(),row.min(),row.max())
    #新建矩阵表
    mxs = op.new_sheet('m','global_{}'.format(name), hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    #新建热图
    gp = op.new_graph('mapping global',template='heatmap2')
    p=gp[0].add_plot(mxs, colz=0)
    #调整热图坐标
    gp[0].set_xlim(col.min(), col.max())
    gp[0].set_ylim(row.min(), row.max())
    gp[0].rescale('z')
    #调整热图标尺
    z = p.zlevels
    z['minors'] = 100
    z['levels'] = [dd.min(), 0, dd.max()]
    p.zlevels = z
    #第二个热图
    dd=np.array(df)
    row=np.array(list(df.index)).reshape(-1).astype(float)
    col=np.array(list(df.columns)).reshape(-1).astype(float)
    mxs = op.new_sheet('m','Product_{}' .format(name), hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    mapping_name='mapping_{}_{}'.format(int(row_index),int(col_index))
    gp = op.new_graph(mapping_name,template='heatmap4')
    p=gp[0].add_plot(mxs, colz=0)
    gp[0].rescale('z')
    gp[0].set_xlim(col.min(), col.max())
    gp[0].set_ylim(row.min(), row.max())
    z = p.zlevels
    z['minors'] = 100
    z['levels'] = [dd.min(), 0, dd.max()]
    p.zlevels = z
    print('max_peek',row_index,col_index)
    print('*'*30,'\n')
    
    #划线图形
    k=[]
    k.append('GObject myLine = [{}]1!line1;'.format(mapping_name))
    k.append('draw -n myLine -lm {'  + '{},{},{},{}'.format(col.min(),row_index,col_index,row_index)+'} ;'  )
    k.append('''myLine.lineType=2;
myLine.linewidth=3;
myLine.color=color(white);''')

    k.append('GObject myLine2 = [{}]1!line2;'.format(mapping_name))
    k.append('draw -n myLine2 -lm {'  + '{},{},{},{}'.format(col_index,row.min(),col_index,row_index)+'} ;'  )
    k.append('''myLine2.lineType=2;
myLine2.linewidth=3;
myLine2.color=color(white);''')
    
    for i in k:
        gp.lt_exec(i)
        print(i)
            
    print('*'*30,'\n')
    ma
    op.exit() 
##############################################################################################################     
def color_bar():
	uip=['#0000FF']
	for x in range(1,12):
		a='#00'+str(hex(x*21))[2:]+'FF'
		#print(a)
		uip.append(a)
	for x in range(1,12):
		a='#00FF'+str(hex(255-x*21))[2:]
		#print(a)
		uip.append(a)
	uip.append('#00FF00')
	for x in range(1,12):
		a='#'+str(hex(x*21))[2:]+'FF00'
		#print(a)
		uip.append(a)
	uip.append('#FFFF00')
	for x in range(1,12):
		a='#FF'+str(hex(255-x*21))[2:]+'00'
		#print(a)
		uip.append(a)
	return uip

##############################################################################################################
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas



class MyQWidget(QWidget):
    def __init__(self, parent=None) :
        super().__init__(parent)
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(static_canvas)
        self._static_ax = static_canvas.figure.subplots()

    def set_df(self,df,num):
        row_list=list(df.index)
        col_list=list(df.columns)
        print('data row col',len(row_list),len(col_list))
        xla=int(len(row_list)/5)
        yla=int(len(col_list)/5)
        import seaborn as sns
        cmap = colors.ListedColormap(color_bar())
        heat_map = sns.heatmap( df ,cmap=cmap,square=False,ax=self._static_ax ,yticklabels=xla,xticklabels=yla)
        heat_map.invert_yaxis()
        
        if num > 0:
            global_range_list.clear()
            for i in range(num):
                row_index,col_index,max_size=get_max_df(df)#get_max_map(df,heat_map,row_list,col_list)
                global_range_list.append(del_area(df,row_index,col_index,max_size,heat_map,i))
        else:
            row_index,col_index,max_size=get_max_map(df,heat_map,row_list,col_list)

        return   row_index,col_index

def get_min(df,xmin,xmax):
    xmin=int(xmin)
    xmax=int(xmax)
    x_list=np.array(list(df.columns))
    #y_list=df.index.values
    col=df.columns.values
    if xmin < x_list.max():
        target_res=x_list >= xmin-(x_list[1]-x_list[0])
    else:
        target_res=np.ones(len(col), dtype=bool)

    if xmax > x_list.min():
        target_res2=x_list<= xmax+(x_list[1]-x_list[0])
    else:
        target_res2=np.ones(len(col), dtype=bool)

    target= target_res & target_res2
    l=[]
    for i,v  in enumerate(target):
        if v:
            l.append(col[i])
    return df.loc[:,l]
    
def get_ymin(df,ymin,ymax):
    ymin=int(ymin)
    ymax=int(ymax)
    x_list=np.array(list(df.index))
    #y_list=df.index.values
    col=df.index.values
    if ymin < x_list.max():
        target_res=x_list >= ymin-(x_list[1]-x_list[0])
    else:
        target_res=np.ones(len(col), dtype=bool)

    if ymax > x_list.min():
        target_res2=x_list<= ymax+(x_list[1]-x_list[0])
    else:
        target_res2=np.ones(len(col), dtype=bool)
  
    target= target_res & target_res2
    l=[]
    for i,v  in enumerate(target):
        if v:
            l.append(col[i])
    return df.loc[l,:]
    
def get_range(df):
    is_choose_peek=False
    is_choose_peek_num=0
    while True:
            x_min = input('X min ')
            if x_min =='q':
                quit()
            if 'p' in x_min:
                is_choose_peek=True
                x_min=int(x_min[1:].strip())
                is_choose_peek_num=x_min
                break
            if  x_min.isdigit():
               break 
    if not is_choose_peek:
        while True:
            x_max = input('X max ')
            if x_max =='q':
                quit()
            if  x_max.isdigit():
                break 

        while True:
            y_min = input('Y min ')
            if y_min =='q':
                quit()
            if  y_min.isdigit():
                break        
        
        while True:
            y_max = input('Y max ')
            if y_max =='q':
                quit()
            if  y_max.isdigit():
                break  
    else:
        x_min,x_max,y_min,y_max=global_range_list[(is_choose_peek_num-1)%len(global_range_list)]

    
    while True:
        grid_num= input('input grid num 0-3 ')
        if grid_num == 'q':
            quit()
        if  grid_num.isdigit():
            if int(grid_num) < 4:
                break   

    df=get_min(df,x_min,x_max)
    df=get_ymin(df,y_min,y_max)

    for i in range(int(grid_num)):
        df=add_point_df(df)
        df=add_point_df(df)

    return df


import os
def read_d(path,pa):
    file_name_top=os.path.splitext(os.path.basename(path))[0]
    import copy
    df_global=read_ex(path)
    df_g=copy.deepcopy(df_global)
    while True:
        peek = input('show top peek ')
        if peek =='q':
            quit()
        if  peek.isdigit():
            break  

    global_sd=MyQWidget()
    global_sd.set_df(df_g,int(peek))
    global_sd.show()

   
    sd_window=None
    for i in range(100):  
        df_g=copy.deepcopy(df_global)
        df=get_range(df_g)
        is_okt=False
        while True:
            peek = input('show top peek ')
            if peek =='q':
                quit()
            if  peek.isdigit():
                break  
            
               

        if not sd_window is None:
            sd_window.close()
        sd_window=MyQWidget()
        r,c=sd_window.set_df(df,int(peek))
        sd_window.show()
        global_sd.show()

        while True:
            x_min = input('seleecv  ')
            if x_min =='q':
                quit()
            if  int(x_min)==0: 
                return df.T
                
def get_pic(mydata):
    data=pd.read_csv('lin2012xyz2e_1_7sf.csv')
    data.columns=['nm','x','y','z']
    data['nm']=data['nm'].astype(int)    
    all_data=pd.merge(mydata,data,on='nm',how='inner')

    x=[]
    y=[]
    def cal_line_xyz(end):
      end['ciex']=end['au']*end['x']
      end['ciey']=end['au']*end['y']
      end['ciez']=end['au']*end['z']
      #print(end)
      ciex=np.array(end.iloc[:,5])
      ciey=np.array(end.iloc[:,6])
      ciez=np.array(end.iloc[:,7])
      vx=integrate.trapz(ciex)
      vy=integrate.trapz(ciey)
      vz=integrate.trapz(ciez)
      linex=vx/(vx+vy+vz)
      liney=vy/(vx+vy+vz)
      linez=vz/(vx+vy+vz)
      #print('ciexy',linex,liney)
      return linex,liney
      
    nmz=[]  
    line_col=mydata.columns[:-1]
    for i in line_col:
      #end=all_data[[i,'nm','x','y','z']]
      end=all_data.loc[:,[i,'nm','x','y','z']]
      end.columns=['au','nm','x','y','z']
      #print(end)
      xh,yh=cal_line_xyz(end)
      x.append(xh)
      y.append(yh)
      nmz.append((xh,yh,i))
     
    st_color=(139,0,255)
    bluec=(0,0,255)
    qing=(0,255,255)
    green=(0,255,0)
    yellow=(255,255,0)
    en_color=(255,0,0)

    b_s=int(len(x)/5)
    r_s=len(x)-b_s*4

    g_color=[]
    def color_list(st_color,en_color,num_step):
        rva=np.linspace(st_color[0],en_color[0],num_step)
        gva=np.linspace(st_color[1],en_color[1],num_step)
        bva=np.linspace(st_color[2],en_color[2],num_step)
        for i in range(num_step):
            color=(int(rva[i])/255,int(gva[i])/255,int(bva[i])/255)
            g_color.append(color)

    color_list(st_color,bluec,b_s+1)
    color_list(bluec,qing,b_s+1)
    color_list(qing,green,b_s+1)
    color_list(green,yellow,b_s+1)
    color_list(yellow,en_color,r_s)
    print('*'*40)
    g_color=list(set(g_color))
    print(g_color)
    print(len(x))
    print(len(g_color))


    rlen=len(g_color)
    rinex=0
    #print(g_color)
    print(x)


    colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)  
    for i in range(len(x)):
        #plt.scatter(x[i],y[i],s=10,color=g_color[rinex])  # 绘图
        plt.scatter(x[i],y[i],s=10,color=(0,0.5,0))  # 绘图
        if rinex < len(g_color)-1:
            rinex+=1
    for i in nmz:
       plt.text(i[0],i[1], str(int(i[2])))
       
    #plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
    plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
    plt.show()




    rinex=0
    colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)  
    for i in range(len(x)):
        #plt.scatter(x[i],y[i],s=10,color=g_color[rinex])  # 绘图
        plt.scatter(x[i],y[i],s=10,color=(0,0.5,0))  # 绘图
        if rinex < len(g_color)-1:
            rinex+=1

       
    #plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
    plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
    plt.show()

    name=''
    csv_text=pd.DataFrame(nmz)

    for i in sys.argv[1:]:
        name=name+'-'+str(i)
       
    name = name.replace('.', '')
    name = name.replace('\\' , '')


    csv_text.to_csv(name+'.csv')

class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        
        super(fileDialogdemo, self).__init__(parent)
        #self.layout = QtWidgets.QVBoxLayout(self)
        #实例化QFileDialog


        f=read_d(sys.argv[1],self)
        col=f.columns
        f['nm']=f.index.astype(int)
         
        #f=f.loc[f.index > 500 ]
        '''if len(arglist)==7 and  len(arglist)==6 :
            col2=[i for i in col if ( i >=  xmap1 and i <= xmap2 ) ]
            #print(col2)
            #col2.append('nm')
            #f=f.loc[:,col2]
            for x in col2:
                ll=f[x]
                #print(ll)
                re=[]
                for va in ll.items():
                    if va[0] <= xmap4 and va[0] >= xmap3:
                        re.append(0)
                    else:
                        re.append(va[1])
                f[x]=re'''

        if xmap5 != '0' :
            step_co=int(xmap5/(col[1]-col[0]))
            col3=[i for ind,i in enumerate(col) if ( ind%step_co==0 ) ]
            col3.append('nm')
            f=f.loc[:,col3]
            
        print(f)    
        
        get_pic(f)

           
    
import sys
if __name__=="__main__":
    if len(sys.argv)==3 and  sys.argv[2] == 'C':
        app = QApplication(sys.argv)

        ex=fileDialogdemo()
        ex.show()
        sys.exit(app.exec_())
    else:
        def read_10002(path):
            df=pd.read_csv(path)
            ret=[]
            for i in df.index:
                tmp=[]
                for j in i:
                    tmp.append(j)
                ret.append(tmp)


            rep=np.array(ret)
            col=np.array(rep[6,1:]).astype(float)
            row=np.array(rep[21:,0]).astype(float)

            val=np.array(rep[21:,1:])
            val[np.where(val==' ')]=0
            val=val.astype(float)
            f=pd.DataFrame(val,columns=col,index=row)
         
            
            f['nm']=f.index.astype(int)
            #f=f.loc[f.index > 500 ]
            if len(arglist)==7 and  len(arglist)==6 :
                col2=[i for i in col if ( i >=  xmap1 and i <= xmap2 ) ]
                #print(col2)
                #col2.append('nm')
                #f=f.loc[:,col2]
                for x in col2:
                    ll=f[x]
                    #print(ll)
                    re=[]
                    for va in ll.items():
                        if va[0] <= xmap4 and va[0] >= xmap3:
                            re.append(0)
                        else:
                            re.append(va[1])
                    f[x]=re

            if xmap5 != '0' :
                step_co=int(xmap5/(col[1]-col[0]))
                col3=[i for ind,i in enumerate(col) if ( ind%step_co==0 ) ]
                col3.append('nm')
                f=f.loc[:,col3]

            #print(f)
            '''_,_,max_size,oklist=get_max_df(f)
            print(max_size,oklist)
            oklist.append('nm')
            f=f.loc[:,oklist]'''
            return f
        f=read_10002(sys.argv[1])
        get_pic(f)






##############


'''def get_max_df(df):
    maxValueIndex = df.idxmax()
    max_size=0
    row_index=0
    col_index=0
    is_First=True
    out=[]
    for v in maxValueIndex.items():
        x=df.loc[v[1],v[0]]
        out.append((v[0],x))
        if is_First:
            max_size = x
            is_First=False
            row_index=v[1]
            col_index=v[0]
        else:
            if max_size < x:
                max_size = x
                row_index=v[1]
                col_index=v[0]
    #print(out)
    re=[i[0] for i in out[:-1] if(i[1] > max_size/10) ]
    #print(re)
    #print(row_index,col_index,max_size)
    return row_index,col_index,max_size,re

def mysq(x):
    print(type(x))
def read_1000(path):
    df=pd.read_csv(path)
    ret=[]
    for i in df.index:
        tmp=[]
        for j in i:
            tmp.append(j)
        ret.append(tmp)


    rep=np.array(ret)
    col=np.array(rep[6,1:]).astype(float)
    row=np.array(rep[21:,0]).astype(float)

    val=np.array(rep[21:,1:])
    val[np.where(val==' ')]=0
    val=val.astype(float)
    f=pd.DataFrame(val,columns=col,index=row)
 
    
    f['nm']=f.index.astype(int)
    #f=f.loc[f.index > 500 ]
    if len(arglist)==7 and  len(arglist)==6 :
        col2=[i for i in col if ( i >=  xmap1 and i <= xmap2 ) ]
        #print(col2)
        #col2.append('nm')
        #f=f.loc[:,col2]
        for x in col2:
            ll=f[x]
            #print(ll)
            re=[]
            for va in ll.items():
                if va[0] <= xmap4 and va[0] >= xmap3:
                    re.append(0)
                else:
                    re.append(va[1])
            f[x]=re

    if xmap5 != '0' :
        step_co=int(xmap5/(col[1]-col[0]))
        col3=[i for ind,i in enumerate(col) if ( ind%step_co==0 ) ]
        col3.append('nm')
        f=f.loc[:,col3]

    

    #print(f)
    _,_,max_size,oklist=get_max_df(f)
    print(max_size,oklist)
    oklist.append('nm')
    f=f.loc[:,oklist]
    return f

'''


'''mydata=read_1000(sys.argv[1])

print(mydata)

data=pd.read_csv('lin2012xyz2e_1_7sf.csv')
data.columns=['nm','x','y','z']
data['nm']=data['nm'].astype(int)
def open_atommap(path):
    li=[]
    with  open(path, "r") as myfile:
        for line in myfile:
            rex=line.split()
            li.append(rex)
    a=pd.DataFrame(li,columns=['nm','au'])     
    return a   
    
#mydata=open_atommap('data.txt')  
#mydata['nm']=mydata['nm'].astype(int)
#mydata['au']=mydata['au'].astype(float)

all_data=pd.merge(mydata,data,on='nm',how='inner')
#print(data)
#print(mydata)
#print(all_data)

x=[]
y=[]
def cal_line_xyz(end):
  end['ciex']=end['au']*end['x']
  end['ciey']=end['au']*end['y']
  end['ciez']=end['au']*end['z']
  #print(end)
  ciex=np.array(end.iloc[:,5])
  ciey=np.array(end.iloc[:,6])
  ciez=np.array(end.iloc[:,7])
  vx=integrate.trapz(ciex)
  vy=integrate.trapz(ciey)
  vz=integrate.trapz(ciez)
  linex=vx/(vx+vy+vz)
  liney=vy/(vx+vy+vz)
  linez=vz/(vx+vy+vz)
  #print('ciexy',linex,liney)
  return linex,liney
nmz=[]  
line_col=mydata.columns[:-1]
for i in line_col:
  #end=all_data[[i,'nm','x','y','z']]
  end=all_data.loc[:,[i,'nm','x','y','z']]
  end.columns=['au','nm','x','y','z']
  #print(end)
  xh,yh=cal_line_xyz(end)
  x.append(xh)
  y.append(yh)
  nmz.append((xh,yh,i))
  



st_color=(139,0,255)
bluec=(0,0,255)
qing=(0,255,255)
green=(0,255,0)
yellow=(255,255,0)
en_color=(255,0,0)


b_s=int(len(x)/5)
r_s=len(x)-b_s*4


tcol=(65,105,225)
g_color=[]
def color_list(st_color,en_color,num_step):
    rva=np.linspace(st_color[0],en_color[0],num_step)
    gva=np.linspace(st_color[1],en_color[1],num_step)
    bva=np.linspace(st_color[2],en_color[2],num_step)
    for i in range(num_step):
        color=(int(rva[i])/255,int(gva[i])/255,int(bva[i])/255)
        g_color.append(color)


def get_color(from_rgb,to_rbg,step):
    color_num = step + 1
    one = np.ones(color_num)

    colors = [((from_rgb[0] + (to_rbg[0]-from_rgb[0])/step*i),
              (from_rgb[1] + (to_rbg[1]-from_rgb[1])/step*i),
              (from_rgb[2] + (to_rbg[2]-from_rgb[2])/step*i))
              for i in range(color_num)]
              
    for index, color in enumerate(colors):
        print(index, color)

    colors = [((from_rgb[0] + (to_rbg[0]-from_rgb[0])/step*i) / 255,
              (from_rgb[1] + (to_rbg[1]-from_rgb[1])/step*i) / 255,
              (from_rgb[2] + (to_rbg[2]-from_rgb[2])/step*i) / 255)
              for i in range(color_num)]
              
    return colors
#color_list(st_color,bluec,b_s+1)
#color_list(bluec,qing,b_s+1)
#color_list(qing,green,b_s+1)
#color_list(green,yellow,b_s+1)
#color_list(bluec,tcol,len(x))
#print('*'*40)
#g_color=list(set(g_color))
#print(g_color)
#print(len(x))
#print(len(g_color))
g_color=get_color(bluec,en_color,len(x))

rlen=len(g_color)
rinex=0
#print(g_color)
#print(x)

#rr=colour.plotting.common.camera(KwargsCamera=colour.plotting.common.KwargsCamera(figsize=(300,300)))
#fig,axp=colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False,camera=rr)  

#plt.figure(figsize=(30,30))
colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False,title='\n')  

for i in range(len(x)):
    plt.scatter(x[i],y[i],s=10,color=g_color[rinex])  # 绘图
    if rinex < len(g_color)-1:
        rinex+=1
texts=[]
for i in nmz:
   texts.append(plt.text(i[0],i[1], str(int(i[2]))))
name=''
csv_text=pd.DataFrame(nmz)

for i in arglist:
    name=name+'-'+str(i)
    


name = name.replace('.', '')
name = name.replace('\\' , '')


csv_text.to_csv(name+'.csv')
#adjust_text(texts)
#plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()

##############'''
'''rinex=0 
for i in range(len(x)):
    plt.scatter(x[i],y[i],s=10,color=g_color[rinex])  # 绘图
    if rinex < len(g_color)-1:
        rinex+=1
#texts=[]
#for i in nmz:
#   texts.append(plt.text(i[0],i[1], str(int(i[2]))))
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()'''
############################
'''rinex=0
colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False,title='\n')  #,axes_visible=False
for i in range(len(x)):
    plt.scatter(x[i],y[i],s=10,color=g_color[rinex])  # 绘图
    #if rinex < len(g_color)-1:
    #    rinex+=1

   
#plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()'''
