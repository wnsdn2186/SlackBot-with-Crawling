import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

URL = ""
ID = ""
PWD = ""
ChromeDriverPath = ""

# Send message to Slack
def send(text):
    url = URL
    payload = {"text": text}
    requests.post(url, json=payload)

#Chrome Options
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(ChromeDriverPath, options=options)

#Open my.knu.ac.kr
OpenUrl = 'https://my.knu.ac.kr/stpo/comm/support/loginPortal/loginForm.action?redirUrl=%2Fstpo%2Fstpo%2Fmain%2Fmain.action'
driver.get(OpenUrl)
driver.implicitly_wait(10)

# Automatic Login (my.knu.ac.kr)
driver.find_element_by_name('user.usr_id').send_keys(ID)
driver.find_element_by_name('user.passwd').send_keys(PWD)
driver.find_element_by_id('loginBtn').click()
driver.implicitly_wait(10)

#Open KNUCUBE
driver.get('http://knucube.knu.ac.kr/index.jsp?gubun=my')
driver.get('http://knucube.knu.ac.kr/site/program/program/programlist?menuid=001002003002&programgroupno=1')
driver.implicitly_wait(10)

#Find out the Time
Date = datetime.today().strftime("%m/%d %H:%M")

#Html Parsing
Element = driver.find_elements_by_css_selector(
    "div.table_style1.mt10 > table > tbody")

#Generate File
filereader = open('count.txt', 'r')
pastCnt = filereader.read()
filereader.close()

#Getting Information and Sent to Slack
for tr in Element:
    td = tr.find_elements_by_tag_name("td")
    if (int)(td[0].text) > (int)(pastCnt):
        for i in range((int)(td[0].text) - (int)(pastCnt) -1, -1, -1):
            j = i*10
            s = "*#{}*\n*[{}]*\n*[{}][{}][{}]*\n*[실습기간] : {}*\n*[지원기간] : {}*\n".format(
                td[j].text, td[j + 1].text, td[j + 2].text, td[j + 3].text, td[j + 4].text, td[j + 5].text.replace('\n', ""), td[j + 6].text.replace('\n', ""))
            filewriter = open('count.txt', 'w')
            filewriter.write(td[0].text)
            filewriter.close()
            print(s)
            send(s)

#Quit
driver.quit()
quit()
