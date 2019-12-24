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
        rating=float(ratingtext[0])
        ratingcount=int(ratingtext[1])

        entry=[goodreads_id,name,author,rating,ratingcount]
        print(entry)


def parse_list(url):
    print("\t"+url)

    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    pagecount= find_pagecount(soup)
    generate_list(soup)

    for x in range(2,pagecount+1):
        newUrl=url+"?page="+str(x)
        print("\t"+newUrl)
        sauce = urllib.request.urlopen(newUrl).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        generate_list(soup)
    


filepath = 'fantasytest'
with open(filepath) as fp:
    line = fp.readline().replace('\n','')
    cnt = 1
    while line:
        parse_list(line)
        line = fp.readline().replace('\n','')
        cnt += 1