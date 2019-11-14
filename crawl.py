from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import csv
import time
from openpyxl import Workbook

chromedriverLocation = "./chromedriver/mac/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chromedriverLocation, chrome_options=chrome_options)

url = "https://entertain.naver.com/tvBrand/6487748"
driver.get(url)
time.sleep(1)

talk_textExtracted = []

page = driver.page_source
soup = BeautifulSoup(page, "html.parser")

totalCount = soup.find('span', {'class': 'u_cbox_count'}).get_text()
totalCount = totalCount.replace(",", "")
totalCount = int(totalCount)

title = soup.find('strong', {'class': 'tit'}).get_text()
print(title)

finished = 0
nextButton = driver.find_element_by_xpath("//a[@title='다음 페이지 목록으로 이동하기']")

while True:
    time.sleep(0.2)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    talkList = soup.find_all('span', {'class': 'u_cbox_contents'})
    for talk in talkList:
        talk = talk.get_text()
        print(talk)
        talk_textExtracted.append(talk)
        if len(talk_textExtracted) == totalCount:
            finished = 1
            break

    if finished == 1:
        break
    else:
        nextButton.click()

f = open(title + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

write_wb = Workbook()
write_ws = write_wb.active


for talk in talk_textExtracted:
    wr.writerow([talk])
    write_ws.append([talk])

f.close()
fileName = title + ".xlsx"
write_wb.save(fileName)