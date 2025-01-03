from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from fake_useragent import UserAgent
import pandas

USER_PAGE_URL = "https://www.ukclimbing.com/logbook/showlog.php?id=<userid>&nresults=100&pg=<page>"
USER_AGENT = UserAgent()

class LogbookError(Exception): 
    def __init__(self, message): 
        super().__init__(message)

def ukc_page_url(userid, page):
    page_url = USER_PAGE_URL[:]
    page_url = page_url.replace("<userid>", str(userid))
    page_url = page_url.replace("<page>", str(page))
    return page_url

def get_page(username, page):
    header = {'User-Agent':str(USER_AGENT.chrome)}
    response = requests.get(ukc_page_url(username, page), header)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'lxml')
    elif reponse.status_code == 409:
        raise Exception(HTTPError, f"HTTP error, status code {response.status_code},response reason '{response.reason}'")

    else:
        raise Exception(HTTPError, f"HTTP error, status code {response.status_code},response reason '{response.reason}'")

def extract_table(soup):
    data = []
    table = soup.find('div', attrs={'id':'myLogbookTable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [item.text.strip() for item in cols]
        data.append(cols)
    return pandas.DataFrame(data)

def get_user_table(userid):
    page = 1
    page_exists = True
    
    soup = get_page(userid, 1)
    no_climbs = get_no_climbs(soup)
    if no_climbs == 0:
        return
    no_pages = int(no_climbs / 100) + (no_climbs % 100 > 0)
    dfs = [extract_table(soup)]
    for i in range(2, no_pages + 1):
        soup = get_page(userid, i)
        dfs.append(extract_table(soup))
    table = pandas.concat(dfs)
    if len(table) != no_climbs:
        raise LogbookError(f"User has {no_climbs} climbs but {len(table)} climbs found.")
    return pandas.concat(dfs)

if __name__ == '__main__':
    page = get_page(297086, 1)
    table = extract_table(page)
    print(table)