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
	fmt.Println("bcy photo downloader is working ...")
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
	r := regexp.MustCompile("\\\\\"multi\\\\\":(\\[[^\\]]+\\])")

	rawJson := r.FindStringSubmatch(string(txt))[1]

	jsons := make([]map[string]interface{}, 0)

	s, e := strconv.Unquote(fmt.Sprintf("\"%s\"", rawJson))
	////s,e := strconv.Unquote(rawJson)
	if e != nil {
		fmt.Println(e.Error())
	}
	rawJson = s

	err := json.Unmarshal([]byte(rawJson), &jsons)
	if err != nil {
		fmt.Println(err.Error())
	}

	for _, v := range jsons {
		imageList = append(imageList, v["original_path"].(string))
	}
	return imageList
}
func saveToFile(path string, body []byte) {
	ioutil.WriteFile(path, body, 0644)
}
