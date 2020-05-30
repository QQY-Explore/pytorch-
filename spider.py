import requests
import random
from bs4 import BeautifulSoup
import time
import json

class Spider(object):
    def __init__(self):
        self.msg = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.42 Safari/537.36",
        }
        self.data_num = 0
    # 获取网页
    def get_html(self, url):
        try:
            rqs = requests.get(url, timeout=18)
            rqs.encoding = 'utf-8'
            html_txt = rqs.text
            soup = BeautifulSoup(html_txt, 'lxml')
            return soup

        except Exception as e:
            print('a', str(e))


    # 过滤板块的文章数少于2000的，并获取符合条件板块的网址
    def get_content(self):
        main_url = "http://www.agronet.com.cn/Tech"#中国农业网农业科技板块网址
        soup1 = self.get_html(main_url)
        pattern = soup1.find(class_="product_list_class")
        #print(pattern)
        pattern = pattern.find_all("li")
        data_url = []
        for item in pattern:
            data = item.find_all("a")
            for iiem in data:
                data_href = iiem.get("href")
                data_name = iiem.string
                soup2 = self.get_html(data_href)
                data_num = soup2.find("div",class_="page_info")
                data_num = data_num.find_all("strong")[1].string
                if int(data_num) >= 2000:
                    data_url.append([data_name,data_href])#栽培1-园林花卉，栽培2-大田作物，栽培3-水果
        return data_url

    #获取数据
    def get_data(self):
        data_url = self.get_content()#获取板块名和对应url
        print(data_url)
        # 写入文件
        flag = 0
        with open(r"data/articles/articles.json", "w",encoding='utf-8') as f:
            for item in data_url:
                self.data_num = 0 #此处对计数进行清零 （新的一个板块）
                article_and_url = self.article_hea(item)#获取文章名和对应url  获取67页共2010篇文章
                #time.sleep(1)
                if item[0] == "栽培技术":
                    flag += 1
                    if flag == 1:
                        item[0] = "栽培技术1"
                    elif flag == 2:
                        item[0] = "栽培技术2"
                    elif flag == 3:
                        item[0] = "栽培技术3"
                else:
                    pass
                for items in article_and_url:#获取文章文本并拼接
                    data_2010_dict = {}
                    txt_data = self.get_one_article(items[1])
                    if txt_data == "no":
                        pass
                    else:
                        if self.data_num <= 1999:
                            data_2010_dict["classify"] = item[0]
                            data_2010_dict["title"] = items[0].replace("\r\n","")
                            data_2010_dict["txt"] = txt_data.replace("　　","")
                            json_data = json.dumps(data_2010_dict, ensure_ascii=False)
                            f.write(json_data)
                            f.write('\n')
                            self.data_num += 1
                        else:
                            continue
    #获取一篇文章的内容
    def get_one_article(self,article_and_url):
        print("目标url-->%s" % article_and_url)
        try:
            soup = self.get_html(article_and_url)
            find_bottom = soup.find("div", id="fontzoom")
            find_p = find_bottom.find_all("p")
            article_txt = ''
            for item in find_p:
                article_txt = article_txt+item.text
            return article_txt
        except:
            return "no"

    #板块文章名称和对应url
    def article_hea(self,item):
        data_list = []
        for num in range(1, 68):  # 1~67
            #time.sleep(1)
            article_url = item[1][:-5] + "_p" + str(num) + ".html"  # 文章url
            print(article_url)
            soup1 = self.get_html(article_url)
            if soup1 is not "no":
                find_dd = soup1.find("dl", class_="arrow_700")
                find_span = find_dd.find_all("span")
                for item_url in find_span:
                    find_a = item_url.find("a", target="_blank")
                    if find_a is not None:
                        if find_a.get("href").find("http") == -1:
                            date_url = "http://www.agronet.com.cn/" + find_a.get("href")  # 文章网址
                        else:
                            date_url = find_a.get("href")
                        date_name = find_a.string.replace(" ", "")  # 文章名
                        data_list.append([date_name,date_url])
        return data_list
'''
#获取数据
    def get_data(self):
        data_url = self.get_content()#获取板块名和对应url
        print(data_url)
        # 写入文件
        flag = 0
        os.remove(r"data/articles/articles.json")
        os.mkdir(r"data/articles/articles.json")
        for item in data_url:
            self.data_num = 0 #此处对计数进行清零 （新的一个板块）
            article_and_url = self.article_hea(item)#获取文章名和对应url  获取67页共2010篇文章
            #time.sleep(1)
            if item[0] == "栽培技术":
                flag += 1
                if flag == 1:
                    item[0] = "栽培技术1"
                elif flag == 2:
                    item[0] = "栽培技术2"
                elif flag == 3:
                    item[0] = "栽培技术3"
            else:
                pass
            for items in article_and_url:#获取文章文本并拼接
                data_2010_dict = {}
                txt_data = self.get_one_article(items[1])
                if txt_data == "no":
                    pass
                else:
                    if self.data_num <= 1999:
                        data_2010_dict["classify"] = item[0]
                        data_2010_dict["title"] = items[0].replace("\r\n","")
                        data_2010_dict["txt"] = txt_data.replace("　　","")
                        json_data = json.dumps(data_2010_dict, ensure_ascii=False)
                        with open(r"data/articles/articles.json", "a", encoding='utf-8') as f:
                            f.write(json_data)
                            f.write('\n')
                        self.data_num += 1
                    else:
                        continue
'''
if __name__ == "__main__":
    spider = Spider()
    spider.get_data()











