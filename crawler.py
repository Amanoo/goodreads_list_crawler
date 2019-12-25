import bs4 as bs
import urllib.request
import string
import re
from goodreads import client
from goodreads.request import GoodreadsRequestException


import sqlite3
from sqlite3 import Error

import time


gc = client.GoodreadsClient("f4YcFGIKNiejrGv59xXQ", "WO8By9ua8KPF9x9c9PiPaAhYSwzGjhqB0JEVgos")


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
 
    sql = ''' INSERT OR IGNORE INTO books(goodreads_id,book_title,author,rating,number_of_ratings,rating_distribution,text_reviews,pub_date)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid

database = r"fantasy.db"
sql_create_table = """ CREATE TABLE IF NOT EXISTS books (
                                    goodreads_id integer PRIMARY KEY,
                                    book_title text NOT NULL,
                                    author text,
                                    rating float,
                                    number_of_ratings integer,
                                    rating_distribution integer,
                                    text_reviews integer,
                                    pub_date datetime
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
        exceptcount=4
        while exceptcount > 0:
            try:    #sometimes this crashes for no reason, so we retry a few times if this is the case.
                goodreads_id=tr.find('div',class_='u-anchorTarget')['id']
                author=tr.find('a',class_="authorName").find('span',itemprop="name").text

                print(goodreads_id)
                book=gc.book(goodreads_id)

                name=book.title
                rating=book.average_rating
                ratingcount=book.ratings_count
                ratingdist=book.rating_dist
                text_reviews=book.text_reviews_count
                date=str(book.publication_date[2])+"-"+str(book.publication_date[0])+"-"+str(book.publication_date[1])

                entry=(goodreads_id,name,author,rating,ratingcount,ratingdist,text_reviews,date)

                #gotta check if we really are dealing with fantasy
                isFantasy=False
                shelves=book.popular_shelves

                if len(shelves)>0: #don't process this book if it doesn't have any shelves
                    for shelf in shelves:
                        if shelf.name == 'fantasy':
                            isFantasy=True
                            break

                if isFantasy:
                   add_fantasy_entry(connextion,entry)
                exceptcount=0
            except GoodreadsRequestException:
                exceptcount=exceptcount-1
                print("encountered goodreadsexception")
                if exceptcount == 0:
                    print("skipping book")
                time.sleep(3)


def parse_list(url):
    pagecount= 1
    x=1
    while x <= pagecount:
        newUrl=url+"?page="+str(x)
        print("\t"+newUrl)
        sauce = urllib.request.urlopen(newUrl).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        if x == 1:
            pagecount= find_pagecount(soup)
        generate_list(soup)
        connextion.commit() #commit once per page, don't want too many writes on our file system
        x += 1
    

#filepath = 'fantasytest.txt'
filepath = 'fantasylists.txt'
with open(filepath) as fp:
    line = fp.readline().replace('\n','')
    cnt = 1
    while line:
        parse_list(line)
        line = fp.readline().replace('\n','')
        cnt += 1
