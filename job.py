import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL="Input Yout URL"

def send(text, link):
    url=URL
    payload={"text": text + "\n" + "<%s|[자세히 보기]>" % link}
    requests.post(url, json=payload)

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument('disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path='/home/ec2-user/KNUCUBE-Crawling/chromedriver', options=options)

OpenUrl='https://cse.knu.ac.kr/06_sub/03_sub.html'
driver.get(OpenUrl)
driver.implicitly_wait(10)

for i in range (1, 66):
    Xpath="//*[@id=\"content\"]/article/article[2]/div[1]/table/tbody/tr[" + str(i) + "]/td[1]"
    Element=driver.find_element_by_xpath(Xpath)
    try:
        int(Element.text)
        recentCnt=int(Element.text)
        break
    except ValueError:
        continue

filereader = open('jobCnt.txt', 'r')
pastCnt = int(filereader.read())
filereader.close()

if recentCnt > pastCnt:
    for j in range(i + recentCnt - pastCnt - 1, i - 1, -1):
        Xpath2="//*[@id=\"content\"]/article/article[2]/div[1]/table/tbody/tr[" + str(j) + "]/td[2]/a"
        Element2=driver.find_element_by_xpath(Xpath2)
        href = Element2.get_attribute('href')
        s = "*{}*".format(Element2.text)
        send(s, href)
    
filewriter = open('jobCnt.txt', 'w')
filewriter.write(str(recentCnt))
filewriter.close()

driver.quit()
quit()




