import requests
from bs4 import BeautifulSoup
import csv

#get math.com homepage
mathcom_url = requests.get('http://www.math.com/')
mathcom = BeautifulSoup(mathcom_url.content, 'html5lib')
mathcom_url.close()

#get the subjects from the menu on math.com
subjects = {}
for subject in mathcom.find_all('a',{'class':'nav_menu'}): #select nav menu 
    href = subject.get('href')
    text = subject.get_text()
    if href.startswith('/homeworkhelp'): #there are other resources we aren't interested in; just get the homeworkhelp ones
        subjects[text] = href

#get data
data = []
for subject in subjects: #go through each subject page
    mathcom_subject_url = requests.get('http://www.math.com' + subjects[subject])
    mathcom_subject = BeautifulSoup(mathcom_subject_url.content, 'html5lib')
    mathcom_subject_url.close()
    for topic in mathcom_subject.find_all('a'): 
        topic_data = {}
        href = topic.get('href')
        text = topic.get_text()
        if href.startswith('/school/subject'): #get all links on a subject page that got resources we want, i.e. the ones starting with /school/subject
            if href.endswith('Quiz.html'): #exclude the Quiz pages
                None
            else: #get the data
                subsubject = mathcom_subject.find(string=text).find_parent('tbody').b.get_text() #first we find the tag with the topic text string, then we move up to the tbody parent and go down again to the first b tag, which contains the subsubject
                topic_data['subject'] = subject
                topic_data['subsubject'] = " ".join(subsubject.split()) #we remove some actually appearing whitespaces from the subsubject string
                topic_data['topic'] = text
                topic_data['url'] = 'http://www.math.com' + subjects[subject] + href
                data.append(topic_data)

#write data in csv file
filename = 'mathcom_scrape.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)