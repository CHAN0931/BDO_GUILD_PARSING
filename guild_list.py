from bs4 import BeautifulSoup
import requests
import sqlite3

MEMBER_LIMIT = 30
max_page = None

req = requests.get(f'https://www.kr.playblackdesert.com/Adventure/Guild?searchText=&Page=1')
soup = BeautifulSoup(req.text, 'html.parser')
pagination = soup.select('#paging > a')
con = sqlite3.connect('List.db')
cur = con.cursor()
cur.execute('CREATE TABLE GUILD_LIST (NAME text, MEMBER int)')
try:
    max_page = int(pagination[-2].text.strip())
except:
    pass


if max_page is not None:
    n = 0
    while n < max_page:
        n += 1
        print(f'Parsing guild page {n}...')
        req = requests.get(f'https://www.kr.playblackdesert.com/Adventure/Guild?searchText=&Page={n}')
        soup = BeautifulSoup(req.text, 'html.parser')
        guilds = soup.select('.adventure_list_table > li')

        count = 0
        for guild in guilds:
            count += 1
            try:
                guildname = guild.select('.guild_title > .text > a')[0].text.strip()
                member = guild.select('.guild_info > .user_info')[0]
                temp = member.select('.guild_member')[0].text.strip()
                num_of_members = int(temp.replace('길드원 : ', '').replace(' 명', ''))
                if num_of_members > MEMBER_LIMIT :
                    cur.execute('INSERT INTO GUILD_LIST VALUES(?, ?);', ((guildname), (num_of_members)))
                    con.commit()
                    print(guildname, num_of_members)
            except Exception as ex:
                # print(f'WARNING! Unable to parse guild {count}: {ex}')
                pass
else:
    print('ERROR! Unable to select max page')