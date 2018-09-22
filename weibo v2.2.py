import url_lib , re ,timelib ,os ,Threadinglib ,Class

def download_beta(path="",iter=""):
    d_ub = url_lib.url_lib()
    with open("weibo_Cookie.txt","r") as c: 
        d_ub.Headers["Cookie"]=c.read()
    pre_url_str="http://wx3.sinaimg.cn/large/"
    while iter.check():
        iter_data = iter.get()
        d_ub.url = pre_url_str + iter_data[1]
        try:
            with open(path+"/"+str(iter_data[0])+".jpg" ,"wb" ,buffering=10*1024*1024+1 ) as photo_file:
                photo = d_ub.Get()
                photo_data = photo.read(10*1024*1024)
                while photo_data:
                    photo_file.write(photo_data)
                    photo_file.flush()
                    photo_data = photo.read(10*1024*1024)
        except IOError :
            print(iter_data[0]," file is downloaded.")
        print(iter_data[0],"file is downloaded.")
    with open(path+"/url.txt","w") as url_file:
        url_file.write(ub.url)

def repair(path):
    with open(path+"/url.txt" ,"r" ) as url_file:
        ub.url =url_file.read()
    with open("weibo_Cookie.txt","r") as c: 
        ub.Headers["Cookie"]=c.read()
    txt=ub.Get().read().decode("utf-8")
    jpg_list = re.compile(r'[^%\\\/\.]*\.jpg\\">').findall(txt)
    if not jpg_list:
        raise
    for i in range(len(jpg_list)):
        jpg_list[i]=jpg_list[i][:-3]
        jpg_list[i]=[i+1,jpg_list[i].replace("\\\\","\\").encode("utf-8").decode("unicode-escape")]
    re_download=[]
    for i in jpg_list:
        if not os.path.exists(path+"/"+ str(i[0]) +".jpg"):
            re_download+=[i]
    re_download_de_iterator = Class.De_Iterator(re_download)
    @timelib.Timelog
    def repair_now():
        Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,re_download_de_iterator]]*3) )



ub = url_lib.url_lib()
while True:
    key = input("\nurl ")
    if key[:4] == "http":
        ub.url = key
    else:
        repair(key)
        continue
    with open("weibo_Cookie.txt","r") as c: 
        ub.Headers["Cookie"]=c.read()
    txt=ub.Get().read().decode("utf-8")
    jpg_list = re.compile(r'[^%\\\/\.]*\.jpg\\">').findall(txt)
    if not jpg_list:
        continue
    for i in range(len(jpg_list)):
        jpg_list[i]=jpg_list[i][:-3]
        jpg_list[i]=[i+1,jpg_list[i]]
    jpg_url_de_iterator = Class.De_Iterator(jpg_list)
    
    @timelib.Timelog
    def download_now():
        pre_url_str="http://wx3.sinaimg.cn/large/"
        path=timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        if len(jpg_list)>2:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*2,[[path,jpg_url_de_iterator]]*2) )
