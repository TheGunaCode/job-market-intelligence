import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
url ='https://www.naukri.com/jobs-in-india'
response=requests.get(url)
print(response)
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "html.parser")
data=[]
cards = soup.find_all('div',class_='srp-jobtuple-wrapper')

for card in cards:

        company_name = card.find('span', class_='comp-dtls-wrap')

        experience =card.find('span',class_='expwdth')

        salary = card.find('span',class_='ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal')

        location=card.find('span',class_='locWdth')

        info=card.find('div',class_=' row4')

        skills = card.find_all('li', class_='dot-gt tag-li')

        skills_list = [skill.text.strip() for skill in skills]

        job_link = card.find('a', class_='title')

        data.append({
            "company_name": company_name.text.strip() if company_name else "",
            "Experience": experience.text.strip() if experience else "",
            "salary": salary.text.strip() if salary else "",
            "location": location.text.strip() if location else "",
            "info":info.text.strip() if info else"",
            "Skills": ", ".join(skills_list),
            "Job_URL": job_link.get('href') if job_link else ""
        })



ws= pd.DataFrame(data)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
ws.fillna('missing')
print(ws)
ws.to_csv('job_market_intelligence.csv')


