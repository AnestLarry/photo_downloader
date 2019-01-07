import url_lib , re ,timelib ,os ,Threadinglib ,sys
from collections import deque

def download_beta(path="",iter=""):
    d_ub = url_lib.url_lib()
    while iter:
        iter_data = iter.popleft()
        d_ub.url = iter_data[1]
        try:
            with open(path+"/"+path+"__"+str(iter_data[0])+".jpg" ,"wb" ,buffering=5*1024*1024+1 ) as photo_file:
                photo = d_ub.Get()
                photo_data = photo.read(5*1024*1024)
                while photo_data:
                    photo_file.write(photo_data)
                    photo_file.flush()
                    photo_data = photo.read(5*1024*1024)
        except IOError :
            print(iter_data[0]," file is fail.")
        print(iter_data[0],"file is downloaded.")

def get_jpg_list(txt="",extra_type="",url="/"):
    if not txt:
        return "txt is none"
    if url [-1] != "/":
        url+="/"
    image_type = ["jpg","png","gif","webp"]
    jpg_list = []
    if extra_type:
        image_type += extra_type
    for guess_type_element in image_type:
        print("Guess file type : "+guess_type_element)
        re_result = re.compile(r'http[^\'"> ]*'+guess_type_element).findall(txt)
        print("find the number of url: ",len(re_result))
        jpg_list += re_result
    for guess_type_element in image_type:
        print("Guess file type : "+guess_type_element)
        re_result = re.compile('[\'"][^\'"> ]*\.'+guess_type_element).findall(txt)
        print("find the number of url: ",len(re_result))
        for i in re_result:
            if "http" in i[1:]:
                jpg_list += [i[1:]]
            else:
                jpg_list += [str(url)+i[1:]]

    return jpg_list

ub = url_lib.url_lib()
while True:
    key = input("\nno suppose url ")
    if key[:4] == "http":
        ub.url = key
    else:
        print("'Normal' mode doesn't support repair.")
        continue
    txt=ub.Get()
    if txt.getcode() !=200:
        print("Error:",txt.getcode(),type(txt.getcode()))
        continue
    txt=txt.read().decode("utf-8")
    jpg_list = get_jpg_list(txt,extra_type=input("Extra type"),url=ub.url)
    if not jpg_list:
        continue
        
    jpg_url_enu=list()
    for i in enumerate(jpg_list):
        jpg_url_enu.append([i[0]+1,i[1][9:-2].replace("\\\\","\\").encode("utf-8").decode("unicode-escape")])
    jpg_url_de_iterator = deque(jpg_url_enu)
    print(jpg_url_enu)
    @timelib.Timelog
    def download_now():
        path=timelib.Showtime("$year-$mon-$day--$hour-$min-$sec")
        os.system("mkdir "+path)
        if len(jpg_list)>4:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*4,[[path,jpg_url_de_iterator]]*4) )
        else:
            Threadinglib.Delay_Threading_To_Exit( Threadinglib.Multithreading_Run([download_beta]*3,[[path,jpg_url_de_iterator]]*3) )
        with open(path+"/"+path+"_url.txt","w") as url_file:
            url_file.write(ub.url)