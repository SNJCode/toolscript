from pymol import cmd



cmd.set('label_distance_digits', '2')


   		

def draw_file(frex):
    print('open _file----'+frex)
    f = open(frex,"r") 
    lines = f.readlines()      #读取全部内容 ，并以列表方式返回
    f.close()
    icc=0
    
    for line in lines:
    	icc+=1
    	if icc % 2 == 1:
                xp=line.split('_')
		#print('aaaaa',xp)
                str_s='A'+str(xp[2]).strip()+'_'+str(icc)
                cmd_4(xp,str_s)
           
        
            
            
    

def cmd_4(xp,s):
    print(xp[0],xp[1],s)
    cmd.distance(s,"index {}".format(int(xp[0])+1),"index {}".format( int(xp[1])+1))

def cmd_2(xp,p,s):
    print(xp,p,s)
    cc=''
    for i in xp:
        cc=cc+'+'+str(int(i)+1)
    cc=cc[1:]
    #print(cc)
    
    name='tmp'
    pname='ptmp'
    cmd.select(name,'index '+cc) 
    cmd.pseudoatom(pname,name)
    cmd.distance(s,"index {}".format(int(p)+1),pname)
    cmd.delete(name)
    cmd.delete(pname)
   
def cmd_0(xp,p,s):
    print(xp,p,s)
    cc=''
    for i in xp:
        cc=cc+'+'+str(int(i)+1)
    cc=cc[1:]
    #print(cc)
    
    dd=''
    for i in p:
        dd=dd+'+'+str(int(i)+1)
    dd=dd[1:]
    #print(dd)
    
    name='tmp'
    pname='ptmp'
    cmd.select(name,'index '+cc) 
    cmd.pseudoatom(pname,name)
    
    name2='tmp2'
    pname2='ptmp2'
    cmd.select(name2,'index '+dd) 
    cmd.pseudoatom(pname2,name2)
    
    
    cmd.distance(s,pname2,pname)
    cmd.delete(name)
    cmd.delete(pname)
    cmd.delete(name2)
    cmd.delete(pname2)

def draw_file_pi(frex):
    print('open _file----'+frex)
    f = open(frex,"r") 
    lines = f.readlines()      #读取全部内容 ，并以列表方式返回
    f.close()
    icc=0
    pcc=0
    phlist=[]
    for line in lines:
        xp=line.split('_')
        phlist.append(xp[1])
        if icc > 4:
        	pcc+=1
        	str_s='B'+str(xp[2]).strip()+'_'+str(pcc)
        	cmd_2(phlist,xp[0],str_s)
        	phlist.clear()
        	icc=-1
       
        	
        icc+=1
        
def draw_file_pipi(frex):
    print('open _file----'+frex)
    f = open(frex,"r") 
    lines = f.readlines()      #读取全部内容 ，并以列表方式返回
    f.close()
    icc=0
    pcc=0
    ind=0
    phlist=[]
    phlist2=[]
    for line in lines:
        xp=line.split('_')
        
        if icc % 2 == 0 :
        	phlist.append(xp[0])
        if icc > 10:
                #print(pcc)
                pcc+=1
                phlist2.append(xp[0])
                if pcc > 5 :
                	pcc = 0
                	#print(phlist,phlist2)
                	ind+=1
                	str_s='C'+str(xp[2]).strip()+'_'+str(ind)
                	cmd_0(phlist,phlist2,str_s)
                	phlist2.clear() 
                phlist.clear()   
                icc=-1
        
                   
       
        	
        icc+=1
        


draw_file('pymol_dist_list.txt')
draw_file_pi('pymol_pidist_list.txt')
draw_file_pipi('pymol_pipidist_list.txt')



