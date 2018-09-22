import url_lib , re ,timelib ,os

ub = url_lib.url_lib()
while True: 
    ub.url = input("url ")
    with open("Cookie.txt","r") as c: 
        ub.Headers["Cookie"]=c.read()
    txt=ub.Get().read().decode("utf-8")
    jpg_list = re.compile(r'[^%\\\/\.]*\.jpg\\">').findall(txt)
    @timelib.Timelog
    def download_now():
        pre_url_str="http://wx3.sinaimg.cn/large/"
        path=timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        n=1
        for i in jpg_list :
            ub.url=pre_url_str+i[:-3]
            try:
                photo=ub.Get().read()
                with open(path+"/"+str(n)+".jpg" ,"wb" ) as photo_file:
                    photo_file.write(photo)
            except IOError:
                print(IOError,"\n",str(n)+" file fail")
                n+=1
                continue
            print(n," file is downloaded.")
            n+=1


