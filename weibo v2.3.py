import url_lib , re ,timelib ,os ,Threadinglib,sys
from collections import deque

def download_beta(path = "",iter = ""):
    d_ub = url_lib.url_lib()
    with open("weibo_Cookie.txt","r") as c: 
        d_ub.Headers["Cookie"] = c.read()
    while iter:
        iter_data = iter.popleft()
        d_ub.url =  iter_data[1]
        try:
            with open(path+"/" + path + "__"+str(iter_data[0])+".jpg" ,"wb" ,buffering = 10*1024*1024+1 ) as photo_file:
                photo = d_ub.Get()
                photo_data = photo.read(10*1024*1024)
                while photo_data:
                    photo_file.write(photo_data)
                    photo_file.flush()
                    photo_data = photo.read(10*1024*1024)
        except IOError :
            print(iter_data[0]," file is downloaded.")
        print(iter_data[0],"file is downloaded.")
    with open(path+"/"+path+"_url.txt","w") as url_file:
        url_file.write(ub.url)

def repair(path):
    with open(path+"/"+path+"_url.txt" ,"r" ) as url_file:
        ub.url =url_file.read()
    with open("weibo_Cookie.txt","r") as c: 
        ub.Headers["Cookie"] = c.read()
    txt = ub.Get().read().decode("utf-8")
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        raise
    jpg_list_emu = list()
    for i in enumerate(jpg_list):
        jpg_list_emu.append([i[0]+1,i[1][:-3].replace("\\\\","\\").encode("utf-8").decode("unicode-escape")])
    re_download = []
    for i in jpg_list_emu:
        if not os.path.exists(path+"/" + path + "__"+str(i[0])+".jpg" ):
            re_download += [i]
    re_download_de_iterator = deque(re_download)
    @timelib.Timelog
    def repair_now():
        Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,re_download_de_iterator]]*3) )

def get_jpg_list(txt=""):
    jpg_list = re.compile(r'[^%\\\/\.]*\.jpg\\">').findall(txt)
    if not jpg_list:
        print("Guess file type : png")
        jpg_list = re.compile(r'[^%\\\/\.]*\.png\\">').findall(txt)
        if not jpg_list:
            temp = input("Can't not find photos file,input type:")
            jpg_list = re.compile(r'[^%\\\/\.]*\.'+temp+'\\').findall(txt)
            if not jpg_list:
                return False
    return jpg_list

def log(path,data):
    try:
        if data.replace("\n",""):
            open(path+"/"+path+"__log.log","a").write(data)
            print("log succ")
    except IOError:
        print("Error: "+str(IOError))

ub = url_lib.url_lib()
if len(sys.argv)>1:
    if sys.argv[1][:4] == "http":
        ub.url = sys.argv[1]
    else:
        repair(sys.argv[1][:4])
        exit()
    with open("weibo_Cookie.txt","r") as c: 
        ub.Headers["Cookie"] = c.read()
    txt = ub.Get()
    if txt.getcode() !=200:
        print("Error:",txt.getcode(),type(txt.getcode()))
        exit()
    txt=txt.read().decode("utf-8")
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        exit()
    jpg_list_emu = list()
    logdata=str("\n\n")
    for i in enumerate(jpg_list):
        jpg_list_emu.append([i[0]+1, "http://wx3.sinaimg.cn/large/" + i[1][:-3]])
        logdata += "http://wx3.sinaimg.cn/large/" + i[1][:-3] + "\n"
    jpg_url_de_iterator = deque(jpg_list_emu)
    
    @timelib.Timelog
    def download_now():
        path = timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        log(path,logdata)
        if len(jpg_list)>2:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*2,[[path,jpg_url_de_iterator]]*2) )
    exit()


while True:
    key = input("\nweibo_url ")
    if key[:4] == "http":
        ub.url = key
    else:
        repair(key)
        continue
    with open("weibo_Cookie.txt","r") as c: 
        ub.Headers["Cookie"] = c.read()
    txt = ub.Get()
    if txt.getcode() !=200:
        print("Error:",txt.getcode(),type(txt.getcode()))
        continue
    txt=txt.read().decode("utf-8")
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        continue
    jpg_list_emu = list()
    logdata=str("\n\n")
    for i in enumerate(jpg_list):
        jpg_list_emu.append([i[0]+1,"http://wx3.sinaimg.cn/large/" + i[1][:-3]])
        logdata += "http://wx3.sinaimg.cn/large/" + i[1][:-3] + "\n"
    jpg_url_de_iterator = deque(jpg_list_emu)
    
    @timelib.Timelog
    def download_now():
        path = timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        log(path,logdata)
        if len(jpg_list)>2:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*2,[[path,jpg_url_de_iterator]]*2) )
