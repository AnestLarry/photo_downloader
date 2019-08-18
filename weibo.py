# Version : 2.35
import re
import timelib
import Threadinglib
import json
import os
from collections import deque
import requests


def handle_url(url: str):
    return "https://m.weibo.cn/status"+url[url.rindex("/"):]


def download_beta(path="", iter=""):
    while iter:
        iter_data = iter.popleft()
        try:
            with open(path+"/" + path + "__"+str(iter_data[0])+".jpg", "wb") as photo_file:
                photo = requests.get(iter_data[1]).content
                photo_data = photo
                photo_file.write(photo_data)
                photo_file.flush()
                #photo_data = photo.read()
        except IOError:
            print(iter_data[0], " file is downloaded.")
        print(iter_data[0], "file is downloaded.")


def repair(path):
    import os
    print(path+"/"+path+"_url.txt")
    with open(path+"/"+path+"_url.txt", "r") as url_file:
        url = handle_url(json.loads(url_file.read())["mobile"])
    res = requests.get(url)
    txt: str = res.text
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        print(jpg_list)
        raise "not url in it"
    jpg_list_emu = list()
    for i in enumerate(jpg_list):
        jpg_list_emu.append([i[0]+1, "http://wx3.sinaimg.cn/large/"+i[1]])
    re_download = []
    for i in jpg_list_emu:
        if not os.path.exists(path+"/" + path + "__"+str(i[0])+".jpg"):
            re_download += [i]
    re_download_de_iterator = deque(re_download)
    print(re_download_de_iterator)
    @timelib.Timelog
    def repair_now():
        Threadinglib.Delay_Threading_To_Exit(Threadinglib.Multithreading_Run(
            [download_beta]*3, [[path, re_download_de_iterator]]*3))


def get_jpg_list(txt: str):
    jpg_list = re.compile(
        '\"url\"\: \"https\://wx[0-9]\.sinaimg\.cn/large/([./A-z0-9]*)\",', re.S).findall(txt)
    print(jpg_list)
    return jpg_list


def log(path, data):
    try:
        if data.replace("\n", ""):
            open(path+"/"+path+"__log.log", "a").write(data)
            print("log succ")
    except IOError:
        print("Error: "+str(IOError))


while True:
    key = input("\nweibo_url ")
    if key[:4] == "http":
        try:
            url = handle_url(key[:key.index("?")])
            key = key[:key.index("?")]
        except:
            url = handle_url(key)
    else:
        repair(key)
        continue
    txt = requests.get(url)
    txt = txt.text
    jpg_list = get_jpg_list(txt)
    if not jpg_list:
        continue
    jpg_list_emu = list()
    logdata = dict()
    for i in enumerate(jpg_list):
        jpg_list_emu.append([i[0]+1, "http://wx3.sinaimg.cn/large/" + i[1]])
        logdata[i[0]+1] = "http://wx3.sinaimg.cn/large/" + i[1]
    jpg_url_de_iterator = deque(jpg_list_emu)

    @timelib.Timelog
    def download_now():
        path = timelib.Showtime(r"$year-$mon-$day--$hour-$min-$sec")
        os.mkdir(path)
        log(path, json.dumps(logdata))
        with open(path+"/"+path+"_url.txt", "w") as url_file:
            url_file.write(json.dumps(dict({"mobile": url, "origan": key})))
        if len(jpg_list) > 2:
            Threadinglib.Delay_Threading_To_Exit(Threadinglib.Multithreading_Run(
                [download_beta]*3, [[path, jpg_url_de_iterator]]*3))
        else:
            Threadinglib.Delay_Threading_To_Exit(Threadinglib.Multithreading_Run(
                [download_beta]*2, [[path, jpg_url_de_iterator]]*2))
