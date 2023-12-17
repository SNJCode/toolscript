import colour
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

import sys 

arglist=sys.argv[1:]
if len(arglist) == 0:
  print('input file')
  quit()
print(arglist)

def read_1000(path):
   df=pd.read_csv(path)
   start=df.iloc[2,:][1]
   end=df.iloc[3,:][1]
   step=df.iloc[4,:][1]
   ex_nm=df.iloc[5,:][1]
   slit=df.iloc[16,:][1]
   scan=df.iloc[0,:][1]
   re_s='Ex{}_Scan{}_Slit{}'.format(int(float(ex_nm)),scan[0:2],slit)
   re_s=re_s.replace(' ','').replace('nm','')
   #print(start,end,step)
   df=df.iloc[20:,:2]
   df.columns=['nm','au']
   df=df.astype(float)
   return df

data=pd.read_csv('lin2012xyz2e_1_7sf.csv')
data.columns=['nm','x','y','z']
data['nm']=data['nm'].astype(int)


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
  print('ciexy',linex,liney)
  return linex,liney
 
 
cie_list=[]  
def get_cie(nmae):
    mydata=read_1000(nmae)
    #print(mydata)
    all_data=pd.merge(mydata,data,on='nm',how='inner')
    #print(all_data)
    xh,yh=cal_line_xyz(all_data)
    cie_list.append((xh,yh,nmae))
    #print('aaaaaa',cie_list)
 
for i in arglist:
  get_cie(i)
  
colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)  
for i in cie_list:
   plt.plot(i[0],i[1],'o',markersize=8,color=(0,0.5,0))  # 绘图
   plt.text(i[0],i[1], i[2])
#plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()


print(cie_list)
csv_text=pd.DataFrame(cie_list)
print(csv_text)
name=''
for i in arglist:
    name=name+'-'+str(i)
    


name = name.replace('.', '')
name = name.replace('\\' , '')
csv_text.to_csv(name+'.csv')

colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)  
for i in cie_list:
   plt.plot(i[0],i[1],'o',markersize=8,color=(0,0.5,0))  # 绘图
   #plt.text(i[0],i[1], i[2])
#plt.plot([liney],[linex],'o',markersize=8,color=(0,0.5,0))  # 绘图
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()


