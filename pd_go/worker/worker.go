package Worker

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"
	"time"
)

var lock sync.Mutex

type Queue struct {
	data [][]string
}
func NewQueue() *Queue {
	return &Queue{data: [][]string{}}
}
func (q *Queue) AppendValue(s []string) {
	lock.Lock()
	(*q).data = append((*q).data, s)
	lock.Unlock()
}
func (q *Queue) getOne() []string {
	lock.Lock()
	var temp []string
	fmt.Println(len(q.data))
	if len((*q).data) > 0 {
		temp = (*q).data[0]
		(*q).data = (*q).data[1:]
	}
	lock.Unlock()
	return temp
}
func (q *Queue) isNil() bool {
	return len((*q).data)==0
}

func Work(q *Queue,WorkId int32) {
	for {
		//fmt.Println(q.isNil())
		for !(*q).isNil() {
			fmt.Printf("Worker[%d] has receviced a task.\n",WorkId)
			aUrl := (*q).getOne()
			timeStr := aUrl[2]
			// timeStr:=time.Now().Format("2006-01-02--15-04-05")
			// os.Mkdir(timeStr,0644)
			// ioutil.WriteFile(fmt.Sprintf("%s/%s__url.txt", timeStr, timeStr), []byte(url), 0644)
			fmt.Println("before get")
			res := GET(aUrl[1], nil)
			fmt.Println("after get")
			ioutil.WriteFile(
				fmt.Sprintf("%s/%s__%s.%s", timeStr, timeStr, aUrl[0], aUrl[1][strings.LastIndex(aUrl[1], ".")+1:]),
				res, 0644,
			)
			fmt.Println("after write")
		}
	}
}

func GET(url string, headers map[string]string) []byte {
	client := &http.Client{Timeout: 5 * time.Second}
	reqest, err := http.NewRequest("GET", url, nil) //建立一个请求
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		return []byte("")
	}
	//Add Header
	reqest.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0")
	if headers != nil {
		for k, v := range headers {
			reqest.Header.Add(k, v)
		}
	}
	response, err := client.Do(reqest)
	defer response.Body.Close()
	// cookies := response.Cookies() //遍历cookies
	//for _, cookie := range cookies {
	//	fmt.Println("cookie:", cookie)
	//}

	responseBody, _ := ioutil.ReadAll(response.Body)
	//if err1 != nil {
	//	// handle error
	//}
	//fmt.Println(string(response_body)) //网页源码
	return responseBody
}
