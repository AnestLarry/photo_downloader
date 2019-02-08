# version : v1.41
import url_lib , re ,timelib ,Threadinglib ,sys
import subprocess as sp
from collections import deque

def download_beta(path="",iter=""):
    d_ub = url_lib.url_lib()
    while iter:
        iter_data = iter.popleft()
        d_ub.url = iter_data[1]
        #print(d_ub.url)
        try:
            with open(path+"/"+path+"__"+str(iter_data[0])+".jpg" ,"wb" ,buffering=5*1024*1024+1 ) as photo_file:
                photo = d_ub.Get()
                photo_data = photo.read(5*1024*1024)
                while photo_data:
                    photo_file.write(photo_data)
                    photo_file.flush()
                    photo_data = photo.read(5*1024*1024)
            print(iter_data[0],"file is downloaded.")
        except IOError :
            print(iter_data[0]," file is fail.")
        

def repair(path):
    import os
    with open(path+"/"+path+"_url.txt" ,"r" ) as url_file:
        ub.url =url_file.read()
    txt=ub.Get().read().decode("utf-8")
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        raise
    jpg_url_enu=list()
    logdata=str("\n\n")
    for i in enumerate(jpg_list):
        jpg_url_enu.append([i[0]+1,i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape")])
        logdata += i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape") + "\n"
    re_download=[]
    for i in jpg_url_enu:
        if not os.path.exists(path+"/"+path+"__"+str(i[0])+".jpg"):
            re_download+=[i]
    re_download_de_iterator = deque(re_download)
    @timelib.Timelog
    def repair_now():
        log(path,logdata)
        Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,re_download_de_iterator]]*3) )

def get_jpg_list(txt=""):
    jpg_list = re.compile(r',\\"original_path[^}]+\.jpg\\"\}').findall(txt)
    if not jpg_list:
        print("Guess file type : png")
        jpg_list = re.compile(r',\\"original_path[^}]+\.png\\"\}').findall(txt)
        if not jpg_list:
            temp = input("Can't not find photos file,input type:")
            jpg_list = re.compile(r',\\"original_path[^}]+\.'+ temp +r'\\"\}').findall(txt)
            if not jpg_list:
                return False
    temp = input("Else type is need?  ")
    if temp:
        jpg_list += re.compile(r',\\"original_path[^}]+\.'+ temp +r'\\"\}').findall(txt)
    return jpg_list

def log(path,data):
    try:
        if data.replace("\n",""):
            open(path+"/"+path+"__log.log","a").write(data)
            print("log succ")
    except IOError:
        print("Error: "+IOError)

ub = url_lib.url_lib()
if len(sys.argv)>1:
    if sys.argv[1][:4] == "http":
        ub.url = sys.argv[1]
    else:
        repair(sys.argv[1])
        exit()
    txt=ub.Get()
    txt=txt.read().decode("utf-8")
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        exit()
    
    jpg_url_enu=list()
    logdata=str("\n\n")
    for i in enumerate(jpg_list):
        jpg_url_enu.append([i[0]+1,i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape")])
        logdata += i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape") + "\n"
    jpg_url_de_iterator = deque(jpg_url_enu)
    @timelib.Timelog
    def download_now():
        path=sp.check_output("create_path.exe").decode()
        log(path,logdata)
        with open(path+"/"+path+"_url.txt","w") as url_file:
            url_file.write(ub.url)
        if len(jpg_list)>4:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*4,[[path,jpg_url_de_iterator]]*4) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )
    exit()

while True:
    key = input("\nbcy_url ")
    if key[:4] == "http":
        ub.url = key
    else:
        repair(key)
        continue
    txt=ub.Get()
    if txt.getcode() !=200:
        print("Error:",txt.getcode())
        continue
    txt=txt.read().decode("utf-8")
    
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        continue
        
    logdata=str("\n\n")
    jpg_url_enu=list()
    for i in enumerate(jpg_list):
        jpg_url_enu.append([i[0]+1,i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape")])
        logdata += i[1][21:-3].replace("\\\\","\\").encode("utf-8").decode("unicode_escape") + "\n"
    jpg_url_de_iterator = deque(jpg_url_enu)
    
    @timelib.Timelog
    def download_now():
        path=sp.check_output("create_path.exe").decode()
        log(path,logdata)
        with open(path+"/"+path+"_url.txt","w") as url_file:
            url_file.write(ub.url)
        if len(jpg_list)>4:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*4,[[path,jpg_url_de_iterator]]*4) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )

        