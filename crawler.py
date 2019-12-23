import bs4 as bs
import urllib.request
import string
import re

def find_pagecount(localsoup):
    preva=""
    for a in localsoup.find_all('a'):
        if "next" in a.text.lower():
            break
        preva=a.text
    try:
        return int(preva)
    except ValueError:
        return 1
    

def generate_list(localsoup):
    table =  localsoup.table
    table_rows=table.find_all('tr')
    for tr in table_rows:
        goodreads_id=tr.find('div',class_='u-anchorTarget')['id']
        name=tr.find('a',class_="bookTitle").find('span').text
        author=tr.find('a',class_="authorName").find('span',itemprop="name").text
        ratingtext=re.sub(r'([a-zA-Z,])','',tr.find('span', class_="minirating").text).split("—")
        #ratingtext=tr.find('span', class_="minirating").text.split("—")

        rating=float(ratingtext[0])
        
        ratingcount=int(ratingtext[1])

        entry=[goodreads_id,name,author,rating,ratingcount]
        print(entry)


url='https://www.goodreads.com/list/show/51.The_Best_Urban_Fantasy?page='
sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce,'lxml')
pagecount= find_pagecount(soup)
generate_list(soup)
#print(len(table_rows))
#print(table_rows[0])
#nav = soup.nav

#f= open("guru99.txt","w+")
#f.write(soup.text)

#soup.find_all('div')







#f.write(a.text+"\n")