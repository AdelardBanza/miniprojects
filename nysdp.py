import nltk
import re
import csv
import operator
from nltk import *
from nltk.tag import pos_tag
from multiprocessing import Pool
import networkx as nx
import itertools
import requests
from bs4 import BeautifulSoup

def get_photo_caption(photo_url): # f() to get the photocaptions from pages
    try:        
        photo_page='http://www.newyorksocialdiary.com'+str(photo_url)
        print photo_page
        r=requests.get(photo_page)
        r.content
        photo_soup=BeautifulSoup(r.content)
        namestext=photo_soup.find_all("div",{"class":"photocaption"})
        for names in namestext:
            names=names.text
            print names   #photocaptions are printed to the screen and saved 
            # as a text file, answers/Names2ANSI2.txt
           
            
    except Exception, f:
        y=f
        print "Unable to use get_photo_caption function!"+str(y)
        
def get_pages(): # function to get all the links to different photopages
    try:          
                for page in range(1,25):   #number of pages to crawl, less than 25     
                    url="http://www.newyorksocialdiary.com/party-pictures?page="+str(page)                   
                    page_url=requests.get(url)                    
                    page_url.content
                    pagesoup=BeautifulSoup(page_url.content)
                    for link in pagesoup.find_all('a'):
                        actual_link_picture_page=str(link.get('href')) # extracts the actual link of the page from the whole <a> href: thingy
                        if (len(str(actual_link_picture_page))> 25) and (actual_link_picture_page[0]=="/") :
                           get_photo_caption(actual_link_picture_page)                      
                                             
               
            
    except Exception, e:
        z=e
        print "Failed get_page function!"+str(z)
        
get_pages()

def findword(item):
    try:
        
            if (len(str(item))<250):
                
                item=str(item)
                item= item.replace("von","Von")
                item= item.replace("van","Van")
                item= item.replace("de","De")
                sentense= str(re.findall(r'''([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)''',item))
                sentense = sentense.replace("Council ","")
                sentense = sentense.replace("Councilman ","")
                sentense = sentense.replace("Councilmember ","")
                sentense = sentense.replace("Councilwoman ","")
                sentense = sentense.replace("Congresswoman ","")
                sentense = sentense.replace("New York","")
                sentense = sentense.replace("Board","")
                sentense = sentense.replace("Member","")
                sentense = sentense.replace("Congressman ","")
                sentense = sentense.replace("Gala","")
                sentense = sentense.replace("History","")
                sentense = sentense.replace("Museum","")
                sentense = sentense.replace("American","")
                sentense = sentense.replace("Congressman ","")
                sentense = sentense.replace("Night ","")
                sentense = sentense.replace("Miss ","")
                sentense = sentense.replace("USA ","")         
                sentense = sentense.replace("Mayor ","")
                sentense = sentense.replace("Event Co","")
                sentense = sentense.replace("Count ","")
                sentense = sentense.replace("Countess ","")
                sentense = sentense.replace("Chairman ","")
                sentense = sentense.replace("Chairwoman ","")
                sentense = sentense.replace("President ","")
                sentense = sentense.replace("Meuseum ","")
                sentense = sentense.replace("Chairmen ","")
                sentense = sentense.replace("DJ ","")
                sentense = sentense.replace("MD ","")
                sentense = sentense.replace("Dance ","")
                sentense = sentense.replace("Director ","")
                sentense = sentense.replace("Dr. ","")
                sentense = sentense.replace("Sir ","")
                sentense = sentense.replace("The ","")
                sentense = sentense.replace("Society","")
                sentense = sentense.replace("Memorial Sloan","")                
                sentense = sentense.replace("Jr. ","")
                sentense = sentense.replace("CEO ","")
                sentense = sentense.replace("[", "")
                sentense = sentense.replace("]", "")
                sentense = sentense.replace("' ", "'")
                sentense = sentense.replace(" ' ", "'")
                sentense = sentense.replace(" '", "'")
                sentense = sentense.replace("'", "")
                sentense = sentense.replace("Executive Director","")
                sentense = sentense.replace("Presi","")
                sentense = sentense.replace("Co ","")
                sentense = sentense.replace("Steering Committee ","")
                sentense = sentense.replace("Vice Presi ","")
                
                return list(sentense.split(','))
           
            
    except Exception, f:
        y=f
        print "Unable to perform function!"+str(y)


#To open the crawled list of names from the website and feed it into the function findword which will find different names in the text.
list_of_words=[]    
f=open('answers/Names2ANSI2.txt', 'r') 
for line in iter (f):
    w=findword(line)
    list_of_words.append(w)
f.close()
list_of_words = [x for x in list_of_words if x != []]


# open the list of names stored in 'names-after-re.txt' and create combinations of all the names present in a photograph together.
# for example a photo with 3 names creates 3 tuples with all possible non-repeated combinations. This would help us later when adding 
# nodes into the graph and maping relationships. We use the networkx library in python to create this graph.

data_combo=[]
data=[]
f=open('answers/names-after-re.txt','r')
for line in list_of_words: 
        #print line    
        data.append(line)                    
f.close()



for line in list_of_words:
 
    try:
        k=(list(itertools.combinations(line,2)))   #creating all possible two tuple name combinations of names that are in a picture 
        data_combo.append(k)
    
    except:   
        pass


# adding tuples of names as related nodes connected with an edge of weight 1. This creates a weieghted 
#undirected multigraph between the nodes. We use the 

M1 = nx.MultiGraph()
G1 = nx.Graph()

for line in data_combo:
    for node in line:
        try:                  
                M1.add_node(node[0])
                M1.add_node(node[1])
                M1.add_edge(node[0], node[1], weight = 1)
                
        except Exception, e:
            print str(e)
            pass


#this creates a graph with nodes and edges
w=0
bestfr=[]
name1=[]
name2=[]
wt=[]
for u,v,data in M1.edges_iter(data=True):
    w = data['weight']
    if G1.has_edge(u,v):
        G1[u][v]['weight'] += w
    else:
        G1.add_edge(u, v, weight=w)
for line in G1.edges(data=True):
    if (str(line[0])!='') and (str(line[0])!=''):        
        name1.append(str(line[0]))
        name2.append(str(line[1]))
        k=line[2].get('weight')
        wt.append(k)


#This creating a list of 3 elements (name1,name2,weight of the edges between these names)
name_wt=zip(name1,name2,wt)


# Sort the list by the 3rd element, i.e. weight
edgesortall=[]
edgesortall = sorted(name_wt,key=lambda x:(x[2]), reverse=True)


# To save the ouptout as a csv file
import csv
with open("answers/degree.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(edgesortall)


#to find the number of times a name appears we ouput the number of names and degrees
nod=[]
deg=[]
for line in M1.nodes():
      nod.append(str(line))
      deg.append(M1.degree(line))
final=zip(nod,deg)


final1=final
final1 = filter(None, final1)
import re
final_list=[]
finalnames=[]
final100sort=[]
for line in final1:        
            finalnames.append(line)
        
final100sort= sorted(finalnames,key=lambda x:(x[1]), reverse=True)
print final100sort


# To save the ouput of the number of times a name appears as a csv file
import csv
with open("answers/popularity.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(final100sort)


#function to sort the number of edges between different nodes
edgesort100=[]
edgesort100 = sorted(name_wt,key=lambda x:(x[1]), reverse=True)[:100]
print edgesort100


#to create pagerank of the names using pagerank from networkx library
pgrank=[]
pgsortall=[]
import operator
pgrank=nx.pagerank(G1)
pgsortall = sorted(pgrank.items(), key=operator.itemgetter(1), reverse=True)


# To save the pagerank output as a csv file
import csv
with open("answers/pagerank.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(pgsortall)
