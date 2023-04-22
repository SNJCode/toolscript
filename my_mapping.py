
from tkinter import font
import pandas as pd
import matplotlib.pylab as plt
import  numpy as np
from matplotlib import colors
import platform
if platform.system ().lower () == 'windows':
    import originpro as op


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
    col_min,col_max,row_min,row_max=find_nerigh(df,row_index,col_index,max_size)
    print('del_area',col_min,col_max,row_min,row_max)
    color_list=['white','red','black','purple']
    co=color_list[i%len(color_list)]
    heat_map.plot([col_min,col_max+1],[row_min,row_min],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_max+1],[row_max+1,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_min,col_min],[row_min,row_max+1],'--',linewidth=3,color=co)
    heat_map.plot([col_max+1,col_max+1],[row_min,row_max+1],'--',linewidth=3,color=co)
   


def find_nerigh(df,row,col,max_size):
    col_list=list(df.columns)
    row_list=list(df.index)
    source_col=col_list.index(col)
    source_row=row_list.index(row)
    max_col=len(col_list)
    max_row=len(row_list) 
    min_top=max_size*0.2
    
    col_min=source_col
    col_max=source_col
    row_min=source_row
    row_max=source_row

    col_min,col_max,row_min,row_max=find_df_borden(df,col_min,col_max,row_min,row_max,min_top,max_col,max_row,source_col,source_row)
    while True:
        _col_min,_col_max,_row_min,_row_max=spread_area(df,col_min,col_max,row_min,row_max,max_col,max_row,min_top)
        if _col_min == col_min and _col_max == col_max and _row_min == row_min and _row_max == row_max:
            col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max
            break
        
        col_min,col_max,row_min,row_max=_col_min,_col_max,_row_min,_row_max

    for i in range(col_min,col_max+1):
        for j in range(row_min,row_max+1):
            df.iloc[j,i]=0
   
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

    val=np.array(rep[21:,1:]).astype(float)
    f=pd.DataFrame(val,columns=col,index=row)
    return f.T

def read_4700(path):
    try:
        ex=pd.read_excel(path,usecols=[0])
    except:
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
    

    return ex.T,True

##############################################################################################################
   
def origin(df_global,df,row_index,col_index):
    op.set_show()

    dd=np.array(df_global)
    row=np.array(list(df_global.index)).reshape(-1)
    col=np.array(list(df_global.columns)).reshape(-1) 

    mxs = op.new_sheet('m','Dot Product global', hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    
    gp = op.new_graph('mapping global',template='heatmap2')
    p=gp[0].add_plot(mxs, colz=0)
    gp[0].rescale('z')
    gp[0].set_xlim(col.min(), col.max())
    gp[0].set_ylim(row.min(), row.max())

    z = p.zlevels
    z['minors'] = 100
    z['levels'] = [dd.min(), 0, dd.max()]
    p.zlevels = z
    
    


    dd=np.array(df)
    row=np.array(list(df.index)).reshape(-1)
    col=np.array(list(df.columns)).reshape(-1) 

    mxs = op.new_sheet('m','Dot Product', hidden=False)
    mxs.from_np(dd)
    mxs.xymap=col.min(),col.max(),row.min(),row.max()
    
    gp = op.new_graph('mapping',template='heatmap2')
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
    
    
    k=[]
    k.append('GObject myLine = [mapping]1!line1;')
    k.append('draw -n myLine -lm {'  + '{},{},{},{}'.format(col.min(),row_index,col_index,row_index)+'} ;'  )
    k.append('''myLine.lineType=2;
myLine.linewidth=3;
myLine.color=color(white);''')

    k.append('GObject myLine = [mapping]1!line2;')
    k.append('draw -n myLine -lm {'  + '{},{},{},{}'.format(col_index,row.min(),col_index,row_index)+'} ;'  )
    k.append('''myLine.lineType=2;
myLine.linewidth=3;
myLine.color=color(white);''')
    
    for i in k:
        gp.lt_exec(i)
            
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
            for i in range(num):
                row_index,col_index,max_size=get_max_df(df)#get_max_map(df,heat_map,row_list,col_list)
                del_area(df,row_index,col_index,max_size,heat_map,i)
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
        target_res=x_list > xmin
    else:
        target_res=np.ones(len(col), dtype=bool)

    if xmax > x_list.min():
        target_res2=x_list< xmax
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
        target_res=x_list > ymin
    else:
        target_res=np.ones(len(col), dtype=bool)

    if ymax > x_list.min():
        target_res2=x_list< ymax
    else:
        target_res2=np.ones(len(col), dtype=bool)
  
    target= target_res & target_res2
    l=[]
    for i,v  in enumerate(target):
        if v:
            l.append(col[i])
    return df.loc[l,:]
    
def get_range(df):
    while True:
            x_min = input('X min,input num or q is quit ')
            if x_min =='q':
                quit()
            if  x_min.isdigit():
               break 

    while True:
        x_max = input('X max,input num or q is quit ')
        if x_max =='q':
            quit()
        if  x_max.isdigit():
            break 

    while True:
        y_min = input('Y min,input num or q is quit ')
        if y_min =='q':
            quit()
        if  y_min.isdigit():
            break        
    
    while True:
        y_max = input('Y max,input num or q is quit ')
        if y_max =='q':
            quit()
        if  y_max.isdigit():
            break  
              
    while True:
        grid_num= input('input grid num 0-3,input num or q is quit ')
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



def read_d(path,pa):
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
            is_origin = input('open origin is,input 1 or q is quit  ')
            if is_origin =='q':
                quit()
            if  int(is_origin)==1: 
                if platform.system ().lower () == 'windows':
                    origin(df_global,df,r,c)
                break
            else:
                break

class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        
        super(fileDialogdemo, self).__init__(parent)
        dig=QFileDialog()
        if dig.exec():
            filenames=dig.selectedFiles()
            print(filenames)
            print(filenames[0])
            dig.close()

        read_d(filenames[0],self)
        
          
import sys
if __name__=="__main__":
    app = QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())

