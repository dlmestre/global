import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html as html_package

class SendSearchResults:
    def __init__(self,user,pwd,destiny,subject,dictionary_results):
        self.user = user
        self.pwd = pwd
        self.destiny = destiny
        self.subject = subject
        self.results = dictionary_results
        self.message = MIMEMultipart('alternative')
    def send(self):
        h = html_package.HTML()
        
        search_terms = results.keys()
        search_terms_string = ", ".join(search_terms)
        html_list = []
        
        for key in search_terms:
            for link in results[key]:
                html_list.append(h.a(key,href=link))
                
        t1 = h.table(border="0")
        for html_result in html_list:
            r = t1.tr
            r.td(html_result)

        html_code = """
                <html>
                <head></head>
                <body>
                <h3>Your search on the Links service for <b>""" + search_terms_string + """</b> 
                found the following records:</h3>
                </br>""" + str(t1) + """ </br>
                </br>
                </body>
                </html>"""

        self.message['Subject'] = self.subject
        self.message['From'] = self.user
        self.message['To'] = self.destiny
        html_content = MIMEText(html_code,'html')
        self.message.attach(html_content)

        try:
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.ehlo()
            server.starttls()
            server.login(self.user,self.pwd)
            server.sendmail(self.user,self.destiny,str(self.message))
            server.close()
        except Exception as e:
            print(e)
