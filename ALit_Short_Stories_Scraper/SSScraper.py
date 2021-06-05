import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup
import re
import textwrap

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Creates SQLite Database
conn = sqlite3.connect('ALit_SS.sqlite')
cur = conn.cursor()

# Creates tables for webpage (going to be https://americanliterature.com/100-great-short-stories) and individual short story pages
cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE,
     error INTEGER, title TEXT, author TEXT, text TEXT, mined INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''')

def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

# Opens base link
cur.execute('SELECT id,url FROM Pages WHERE mined is 0 and error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Starting Crawl")
else:
    starturl = input('Press Enter to start')
    starturl = 'https://americanliterature.com/100-great-short-stories'

    if ( len(web) > 1 ):
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
        cur.execute('INSERT OR IGNORE INTO Pages (url, title, mined) VALUES ( ?, NULL, 0)', ( starturl, ) )
        conn.commit()
        
# Show current web links
cur.execute('''SELECT url FROM Webs''')
webs = list()
for row in cur:
    webs.append(str(row[0]))
print(webs)

# Starts Crawling through pages
many = 0
while True:
    if many < 1:
        sval = input('How many pages:')
        if len(sval) < 1:
            break
        many = int(sval)
    many = many - 1

    cur.execute('SELECT id,url FROM Pages WHERE mined is 0 and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        fromid = row[0]
        url = row[1]
    except:
        print('No unretrieved pages found')
        many = 0
        break

    print(fromid, url, end=' ')
    
    # Retrieves page
    try:
        document = urlopen(url, context=ctx)

        html = document.read()
        if document.getcode() != 200:
            print("Error with page: ",document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )

        if 'text/html' != document.info().get_content_type():
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue

        print('('+str(len(html))+')', end=' ')
        
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string
        print(title)
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user')
        break
    except:
        print("Failure in retrieving/parsing page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue

    cur.execute('INSERT OR IGNORE INTO Pages (url, title) VALUES ( ?, NULL )', ( url, ) )
    cur.execute('UPDATE Pages SET mined=1 WHERE url=?', ( url, ) )
    conn.commit()
    
    # Parsing and committing to database title, author, body text, etc.
    tags = soup('a')
    for tag in tags:
        href = tag.get('href', None)
        if ( href is None ):
            continue
        up = urlparse(href)
        if ( len(up.scheme) < 1 ):
            href = urljoin(url, href)
        ipos = href.find('#')
        if ( ipos > 1 ):
            href = href[:ipos]
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ):
            continue
        if ( href.endswith('/') ):
            href = href[:-1]
        if ( len(href) < 1 ):
            continue

        document = urlopen(href, context=ctx)
        
        p = re.compile('https://americanliterature\.com/author/[^/]+/short-story/')
        if (p.match(href) ) is None:
           continue
        html_1 = document.read()
        soup_1 = BeautifulSoup(html_1, "html.parser")
        if float(soup_1.find(id="new_score").string) < 8:
            continue
        title = soup_1.title.string
        author = soup_1.find(itemprop="author").string
        text = ''
        for paragraph in soup_1.find_all('p'):
            if not paragraph.string is None: 
                text = text + '\n' + indent(paragraph.string, 4)
        
        cur.execute('INSERT OR IGNORE INTO Pages (url, title, author, text, mined) VALUES ( ?, ?, ?, ?, 0 )', ( href, title, author, text, ) )
        conn.commit()