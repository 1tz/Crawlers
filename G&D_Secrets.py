# -*- coding: utf-8 -*-
import requests, re
from bs4 import BeautifulSoup

outfile = open('secrets.txt', 'w')

r = requests.get('https://www.taptap.com/topic/99880', verify=True)
soup = BeautifulSoup(r.text, "html.parser")
result_raw = soup.find('div', {'class': 'main-first-body bbcode-body'})
result_lines = str(result_raw).split('<br/>')
for line in result_lines:
    if line.find("今日限时密令")!=-1:
        s = line
        break
outfile.write(s[len(s)-10:len(s)-4]+'\n')

r = requests.get('https://www.taptap.com/topic/96965', verify=True)
soup = BeautifulSoup(r.text, "html.parser")
result_raw = soup.find('div', {'class': 'main-first-body bbcode-body'})
result_lines = str(result_raw).split('<br/>')
result = []

for oneline in result_lines:
    if oneline == "":
        continue
    if oneline[0] == '<':
        continue
    elif oneline[0] == '-':
        continue
    elif oneline.find("（") != -1:
        continue
    elif oneline.find("【") != -1:
        continue
    else:
        s = ''
        char = ''
        for char in oneline:
            if char == '(':
                break
            s = s + char
        if char != '\n':
            outfile.write(s + "\n")
        else:
            outfile.write(s)
outfile.close()