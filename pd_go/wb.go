package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	Worker "pd_go/worker"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

var w sync.WaitGroup

func main() {
	q := Worker.NewQueue()
	fmt.Println("wb photo downloader is working ...")
	for i := 1; i < 5; i++ {
		go Worker.Work(q, int32(i))
		fmt.Printf("Worker[%d] has waitting ...\n", i)
	}
	for {
		inputUrl := ""
		fmt.Scanln(&inputUrl)
		if inputUrl[:4] != "http" {
			Worker.Repair(inputUrl, q)
			continue
		}
		inputUrl = "https://m.weibo.cn/status" + inputUrl[strings.LastIndex(inputUrl, "/"):]
		body, e := Worker.GET(inputUrl, nil)
		if e != 200 {
			fmt.Printf("Get Page Error. Status Code %d\n", e)
		}
		//txt, _ := utf8.DecodeRune(body)
		var imageList []string
		Worker.ProtectRun(func() {
			imageList = getImageList(body)
		})
		if len(imageList) == 0 {
			fmt.Println("No image link.")
			continue
		}
		logData := make(map[string]string, 0)

		timeStr := time.Now().Format("2006-01-02--15-04-05")
		os.Mkdir(timeStr, 0644)
		if strings.Contains(inputUrl, "?") {
			saveToFile(
				fmt.Sprintf("%s/%s__url.txt", timeStr, timeStr),
				[]byte(inputUrl[:strings.LastIndex(inputUrl, "?")]))
		} else {
			saveToFile(
				fmt.Sprintf("%s/%s__url.txt", timeStr, timeStr),
				[]byte(inputUrl))
		}
		for i := 0; i < len(imageList); i++ {
			logData[strconv.Itoa(i)] = imageList[i]
			q.AppendValue([]string{strconv.Itoa(i), imageList[i], timeStr})
		}
		fmt.Printf("Enqueue %d task(s) in the queue.", len(imageList))
		logDataJson, _ := json.Marshal(logData)
		saveToFile(fmt.Sprintf("%s/%s__log.txt", timeStr, timeStr),
			logDataJson)
		//fmt.Println(inputUrl)
	}
}

func getImageList(txt []byte) []string {
	imageList := make([]string, 0)
	r := regexp.MustCompile("\\\"url\\\"\\: \\\"https\\://wx[0-9]\\.sinaimg\\.cn/large/([./A-z0-9]*)\\\",")

	rawJson := r.FindAllStringSubmatch(string(txt), -1)
	for _, i := range rawJson {
		imageList = append(imageList, "http://wx3.sinaimg.cn/large/"+i[1])
	}
	//fmt.Println(imageList)
	return imageList
}
func saveToFile(path string, body []byte) {
	ioutil.WriteFile(path, body, 0644)
}
