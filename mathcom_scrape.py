#%%
import requests
from bs4 import BeautifulSoup
import csv

mathcom_url = requests.get('http://www.math.com/')
mathcom = BeautifulSoup(mathcom_url.content, 'html5lib')
mathcom_url.close()

subjects = {}
for subject in mathcom.find_all('a',{'class':'nav_menu'}):
    href = subject.get('href')
    text = subject.get_text()
    if href.startswith('/homeworkhelp'):
        subjects[text] = href

data = []
for subject in subjects:
    mathcom_subject_url = requests.get('http://www.math.com' + subjects[subject])
    mathcom_subject = BeautifulSoup(mathcom_subject_url.content, 'html5lib')
    mathcom_subject_url.close()
    for topic in mathcom_subject.find_all('a'):
        topic_data = {}
        href = topic.get('href')
        text = topic.get_text()
        if href.startswith('/school/subject'):
            if href.endswith('Quiz.html'):
                None
            else:
                topic_data['subject'] = subject
                topic_data['subsubject'] = 'subsubject'
                topic_data['topic'] = text
                topic_data['url'] = 'http://www.math.com' + subjects[subject] + href
                data.append(topic_data)

filename = 'mathcom_scrape.csv'
with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)