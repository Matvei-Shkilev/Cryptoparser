import requests
import csv
from bs4 import BeautifulSoup


def write_to_csv(data: dict):
    with open('coingencko.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['ticker'], data['price'], data['link'], data['graph']))


def get_html(url: str):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def get_data(html: str):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        spans = tds[2].find_all('span')
        name = spans[0].text.strip()
        ticker = spans[1].text.strip()
        link = 'https://www.coingecko.com' + tds[2].find('a').get('href')
        price = tds[3].find('span').text
        graph = tds[11].find('img').get('src')
        data = {
            'name': name,
            'ticker': ticker,
            'link': link,
            'price': price,
            'graph': graph
        }
        write_to_csv(data)


def main():
    for page in range(1, 128):
        url = 'https://www.coingecko.com/'
        get_data(get_html(url))


if __name__ == '__main__':
    main()

