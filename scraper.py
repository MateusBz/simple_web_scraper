import requests

import csv

from bs4 import BeautifulSoup


class Connection:
    def __init__(self, url):
        self.url = url

    def connection_to(self):
        connection = requests.get(self.url)
        return connection


class ParserHtml:
    def __init__(self, connection):
        self.connection = connection

    def find_links(self):
        soup = BeautifulSoup(self.connection.text, 'lxml')
        articles = soup.main
        links = articles('a', {'rel': 'bookmark'})
        return links


def write_new_links(file, links):
    with open(file, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for new_link in links:
            writer.writerow([new_link.text, new_link.get('href')])


def check_files(file, links):
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for link in links:
            saved = set()
            for row in csv_reader:
                if row[1] not in link['href']:
                    saved.add(link)
        write_new_links(file, saved)


if __name__ == '__main__':

    categories = ['python', 'blockchain', 'narzedzia', 'web-scraping']
    for category in categories:
        url = 'http://kamil.kwapisz.pl/category/' + category + '/'
        conn = Connection(url)
        links_of_site = ParserHtml(conn.connection_to()).find_links()
        file_name = category + '.csv'
        try:
            scrap = check_files(file_name, links_of_site)

        except FileNotFoundError:
            scrap = write_new_links(file_name, links_of_site)
