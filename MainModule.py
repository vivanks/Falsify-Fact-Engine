import numpy as np
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
from bs4 import BeautifulSoup
import nltk
import requests
import re
import heapq

def FactEngine(input_msg):
    target_text=str(input_msg)
    #Scrapes and Writes into File
    fo = open("news.txt", "w",encoding = 'UTF-8')
    fo.seek(0, 0)
    for n in range(0,10,10):
        num=int((n/10)+1)
        fo.write("From Page "+str(num)+"\n\n")
        target_url="https://www.google.com/search?q="+str(target_text)+"&tbm=nws&start="+str(n)
        raw = get(target_url).text
        page = fromstring(raw)
        for result in page.cssselect(".r a"):
            url = result.get("href")
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
                fo.write("\n\n"+url[0])
                response = requests.get(url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                links = soup.findAll("p")
                fo.write("\n\n"+re.sub('<[^>]+>', '',str(links))) 
    
    #NE Tagging Target Text, Important Words Shortlisted          
    namedEnt = nltk.pos_tag(nltk.word_tokenize(target_text))
    named_entities = []
    search_query = []
    for x in namedEnt:
        if x[1] == 'NNP':
            named_entities.append(x[0])
    i=0
    
    while(True):
        try:
                search_query.append(str(named_entities[i][0][0]))
        except Exception as e:
            break
        i+=1
    
    #Reading back from File
    k=g=0
    count=[0]*len(search_query)
    while(k<len(search_query)):
        search_text=search_query[k]
        with open('news.txt', 'r',encoding = 'UTF-8') as myfile:
            data=myfile.read().replace('\n', '')
            for i in data:
                if(i==search_text):
                    count[k]+=1
        k+=1
    
    min2=heapq.nsmallest(2,count)[-1]
    rel=(min(count)/min2)*100
    
    if(rel>60):
        print("Trust Me. It's True.")
    else:
        print("Oh Snap. It's a Lie!")
    return 0