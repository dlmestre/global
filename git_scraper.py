import requests,time,random,os
from bs4 import BeautifulSoup
import datetime

VERBOSE = True
LOGGING = False

def log(message):
    try:
        message = str(message)
        if VERBOSE:
            print(datetime.datetime.now().strftime('[%H:%M:%S] ') + message)
        if LOGGING:
            pass
    except Exception as e:
        print e
        print message

class scraper:
    def __init__(self,base,url,testing=None,path=""):
        self.base = base
        self.url = url
        self.tickets_links = []
        self.testing = testing
        self.path = path
        self.start()
    def start(self):
        counter = 0
        while True:
            r = self.get_response(self.url)
            self.page = BeautifulSoup(r.text, "lxml")
            self.get_tickets() 
            next_link = self.page.find("span",{"class":"next"})
            try:
                if next_link:
                    next_link = next_link.a["href"]
                    log("scraping page : {0}".format(next_link))
                    self.url = self.base + next_link
                    counter += 1
                    if self.testing and counter > 2:
                        log("breaking code")
                        log(self.tickets_links)
                        self.guard_tickets()
                        break
                else:
                    self.guard_tickets()
                    break
            except Exception as e:
                log("-----ERROR-----")
                log(e)
                log("-----ERROR-----")
                self.guard_tickets()
                break     
    def get_response(self,url):
        counter_checker = 0
        header = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0"}
        while True:
	    if counter_checker > 15:
	        log("The scraper can't access the url")
	        break
	    try:
                time.sleep(random.uniform(0.5,2))
	        r = requests.get(url, headers=header, timeout=60)
	        break
	    except Exception as e:
	        log(e)
	        time.sleep(3)
	        counter_checker += 1
	        continue
        return r
    def get_tickets(self):
        for item in self.page.findAll("td",{"class":"summary"}):
            self.tickets_links.append(self.base + item.a["href"])
    def guard_tickets(self):
        out_dir = "Tickets_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        log("Creating the folder {0} ...".format(out_dir))
        try:
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
        except Exception:
            pass
        size = len(self.tickets_links)
        for pos,link in enumerate(self.tickets_links,1):
            r = self.get_response(link)
            filename = link.replace("http://","").replace("/","_").replace(":","") + ".html"
            folder = os.path.join(self.path,out_dir,filename)
            log("Guarding html file at : {0} ({1}/{2})".format(folder,pos,size))
            with open(folder,"w") as f:
                r.encoding = "utf-8"
                f.write(r.text.encode("utf-8")) 
    

