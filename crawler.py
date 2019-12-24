import bs4 as bs
import urllib.request
import string
import re


import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def add_fantasy_entry(conn, entry):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT OR IGNORE INTO books(goodreads_id,book_title,author,rating,number_of_ratings)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid

database = r"fantasy.db"
sql_create_table = """ CREATE TABLE IF NOT EXISTS books (
                                    goodreads_id integer PRIMARY KEY,
                                    book_title text NOT NULL,
                                    author text,
                                    rating float,
                                    number_of_ratings integer
                                ); """
connextion = create_connection(database)
create_table(connextion, sql_create_table)

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

        entry=(goodreads_id,name,author,rating,ratingcount)
        add_fantasy_entry(connextion,entry)

        #print(entry)


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
    


filepath = 'fantasylists'
with open(filepath) as fp:
    line = fp.readline().replace('\n','')
    cnt = 1
    while line:
        parse_list(line)
        line = fp.readline().replace('\n','')
        cnt += 1

connextion.commit()
