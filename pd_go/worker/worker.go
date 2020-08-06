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
	data   [][]string
	length int
}

func NewQueue() *Queue {
	return &Queue{data: [][]string{}, length: 0}
}
func (q *Queue) AppendValue(s []string) {
	lock.Lock()
	(*q).data = append((*q).data, s)
	(*q).length++
	lock.Unlock()
}
func (q *Queue) getOne() []string {
	lock.Lock()
	var temp []string
	//fmt.Println(len(q.data))
	//if len((*q).data) > 0 {
	if (*q).length > 0 {
		temp = (*q).data[0]
		(*q).data = (*q).data[1:]
		(*q).length--
	}
	lock.Unlock()
	return temp
}
func (q *Queue) isNil() bool {
	return (*q).length == 0
}

func Work(q *Queue, WorkId int32) {
	for {
		//fmt.Println(q.isNil())
		for !(*q).isNil() {
			fmt.Printf("Worker[%d] receviced a task.\n", WorkId)
			aUrl := (*q).getOne()
			timeStr := aUrl[2]
			// timeStr:=time.Now().Format("2006-01-02--15-04-05")
			// os.Mkdir(timeStr,0644)
			// ioutil.WriteFile(fmt.Sprintf("%s/%s__url.txt", timeStr, timeStr), []byte(url), 0644)
			res, err := GET(aUrl[1], nil)
			if err != 200 {
				fmt.Printf("HTTP Error: Code [%d]\n", err)
				continue
			}
			ioutil.WriteFile(
				fmt.Sprintf("%s/%s__%s.%s", timeStr, timeStr, aUrl[0], aUrl[1][strings.LastIndex(aUrl[1], ".")+1:]),
				res, 0644,
			)
			fmt.Printf("Worker[%d] finished a task.\t%d task(s) left in the queue\n", WorkId, (*q).length)
		}
	}
}

func Repair(folder string, q *Queue) {

}

func GET(url string, headers map[string]string) ([]byte, int) {
	client := &http.Client{Timeout: 5 * time.Second}
	reqest, err := http.NewRequest("GET", url, nil) //建立一个请求
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		return []byte(""), 0
	}
	//Add Header
	reqest.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0")
	if headers != nil {
		for k, v := range headers {
			reqest.Header.Add(k, v)
		}
	}
	response, err := client.Do(reqest)
	if err != nil {
		fmt.Println(err.Error())
		return []byte(""), 0
	}
	defer response.Body.Close()
	// cookies := response.Cookies() //遍历cookies
	//for _, cookie := range cookies {
	//	fmt.Println("cookie:", cookie)
	//}

	responseBody, _ := ioutil.ReadAll(response.Body)
	Code := response.StatusCode
	//if err1 != nil {
	//	// handle error
	//}
	//fmt.Println(string(response_body)) //网页源码
	return responseBody, Code
}
