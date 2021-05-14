#%%
import requests
from bs4 import BeautifulSoup

mathcom_url = requests.get('http://www.math.com/')
mathcom = BeautifulSoup(mathcom_url.content, 'html5lib')
mathcom_url.close()

subjects = {}
for subject in mathcom.find_all('a',{'class':'nav_menu'}):
    href = subject.get('href')
    text = subject.get_text()
    if href.startswith('/homeworkhelp'):
        subjects[text] = href

topics = {}
for subject in subjects:
    mathcom_subject_url = requests.get('http://www.math.com' + subjects[subject])
    mathcom_subject = BeautifulSoup(mathcom_subject_url.content, 'html5lib')
    mathcom_subject_url.close()
    for topic in mathcom_subject.find_all('a'):
        href = topic.get('href')
        text = topic.get_text()
        if href.startswith('/school/subject'):
            topics[text] = href
