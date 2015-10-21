import urlparse
from bs4 import BeautifulSoup
import urllib2
import threading
from Queue import Queue
import re
import time

start = time.time()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class crawler:
    def __init__(self,url):
        self.url = url
        self.visited = [url]
        self.urls = [url]
        self.urls_home_page = [url]
        self.errors = []
        self.q = Queue()
        self.soups = []
        
        self.crawl_home_page()
    def crawl_home_page(self):
        try:
            req = urllib2.Request(self.urls[0], headers=hdr)
            html_text = urllib2.urlopen(req)
            
            soup = BeautifulSoup(html_text)
            
            for item in soup.find_all("a",href=True):
                item["href"] = urlparse.urljoin(self.url,item["href"])
                if self.url in item["href"] and item["href"] not in self.visited:
                    self.urls_home_page.append(item["href"])
                    print(item["href"])
        except Exception as e:
            print(e)
    def crawl(self):
        while len(self.urls) > 0:
            try:
                req = urllib2.Request(self.urls[0], headers=hdr)
                html_text = urllib2.urlopen(req)
            except Exception as e:
                print(e)
                self.errors.append(self.urls[0])
            soup = BeautifulSoup(html_text)
            
            self.urls.pop(0)
            
            for item in soup.find_all("a",href=True):
                item["href"] = urlparse.urljoin(self.url,item["href"])
                if self.url in item["href"] and item["href"] not in self.visited:
                    self.urls.append(item["href"])
                    self.visited.append(item["href"])
                    print(item["href"])
        return self.visited
    def get_urls(self):
        return self.urls_home_page
    
    def generate_soups(self): 

        links = self.urls_home_page

        for url in links:
            self.list_append(self.soups,url)

        return self.soups
    
    def list_append(self,out_list,url):
        req = urllib2.Request(url, headers=hdr)
        html_text = urllib2.urlopen(req)
        soup = BeautifulSoup(html_text)
        out_list.append(soup)
    
    def score(self,words):

        Titles = []
        Heads = []
        Bodies = []

        Words = words.split()
        
        links = self.urls_home_page

        lists = []

        for Word in Words:
            tmp = []
            for link in links:
                if Word in link:
                    tmp.append(True)
                else:
                    tmp.append(False)
            lists.append(any(tmp))
        link_score = 40 * lists.count(True)/float(len(lists))    

        for word in Words:

            body_list = []
            title_list = []
            head_list = []

            for soup in self.soups:
                b = False
                t = False
                h = False
                total_head = soup.head(text = re.compile(word))
                title = soup.head.title(text = re.compile(word))
                body = soup.body(text = re.compile(word))
                head = [i for i in total_head if i not in title]

                title = len(title)
                body = len(body)
                head = len(head)

                if body > 0:
                    b = True
                if title > 0:
                    t = True
                if head > 0:
                    h = True
                body_list.append(b)
                title_list.append(t)
                head_list.append(h)

            Titles.append(any(title_list))
            Bodies.append(any(body_list))
            Heads.append(any(head_list))

        body_score = 35 * Bodies.count(True)/float(len(Bodies))
        title_score = 15 * Titles.count(True)/float(len(Titles))
        head_score = 10 * Heads.count(True)/float(len(Heads))

        return link_score + body_score + title_score + head_score

url = r"url"
obj =  crawler(url)
s = obj.generate_soups()
scores = obj.score("SEO")

print(time.time() - start)
