from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from fake_useragent import UserAgent
import pandas

USER_PAGE_URL = "https://www.ukclimbing.com/logbook/showlog.php?id=<userid>&nresults=100&pg=<page>"
USER_AGENT = UserAgent()

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

if __name__ == '__main__':
    page = get_page(297086, 1)
    extract_table(page)