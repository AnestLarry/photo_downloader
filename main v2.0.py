import url_lib , re ,timelib ,os ,Threadinglib

def download_2(start=0,path=""):
    pre_url_str="http://wx3.sinaimg.cn/large/"
    for j in range(start,len(jpg_list),2):
        ub.url=pre_url_str+jpg_list[j][:-3]
        try:
            photo=ub.Get().read()
            with open(path+"/"+str(j+1)+".jpg" ,"wb" ) as photo_file:
                photo_file.write(photo)
        except IOError:
            print(IOError,"\n",str(j+1)+" file fail")
        print(j+1," file is downloaded.")

def download_3(start=0,path=""):
    pre_url_str="http://wx3.sinaimg.cn/large/"
    for j in range(start,len(jpg_list),3):
        ub.url=pre_url_str+jpg_list[j][:-3]
        try:
            photo=ub.Get().read()
            with open(path+"/"+str(j+1)+".jpg" ,"wb" ) as photo_file:
                photo_file.write(photo)
        except IOError:
            print(IOError,"\n",str(j+1)+" file fail")
        print(j+1," file is downloaded.")



ub = url_lib.url_lib()
while True:
    ub.url = input("url ")
    with open("Cookie.txt","r") as c: 
        ub.Headers["Cookie"]=c.read()
    txt=ub.Get().read().decode("utf-8")
    jpg_list = re.compile(r'[^%\\\/\.]*\.jpg\\">').findall(txt)
    if not jpg_list:
        continue    
    @timelib.Timelog
    def download_now():
        pre_url_str="http://wx3.sinaimg.cn/large/"
        path=timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        if len(jpg_list)>2:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_3]*3,[[0,path],[1,path],[2,path]]) )
        elif len(jpg_list)>1:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_2]*2,[[0,path],[1,path]]) )
        else:
            pre_url_str="http://wx3.sinaimg.cn/large/"
            ub.url=pre_url_str+jpg_list[0][:-3]
            try:
                photo=ub.Get().read()
                with open(path+"/1.jpg" ,"wb" ) as photo_file:
                    photo_file.write(photo)
            except IOError:
                print(IOError,"\n","1 file fail")
            print("1 file is downloaded.")
