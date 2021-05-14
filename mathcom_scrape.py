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
        subjects[text]=href

print(subjects)