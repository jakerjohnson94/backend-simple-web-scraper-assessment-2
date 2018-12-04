#!/usr/bin/env python2
import argparse
import requests
import re
from bs4 import BeautifulSoup


__author__ = 'Jake Johnson'

regex = {
    'phone': r"(?:\D)(\(?\d{3})\D{0,3}(\d{3})\D{0,3}(\d{4})\D",
    'email': r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
    'url': (r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]"
            r"|(?:%[0-9a-fA-F][0-9a-fA-F]))[^\)\"';\s]+")
}


def parse_html_from_src(data):
    data_dict = dict()
    soup = BeautifulSoup(data, 'html.parser')
    raw_html = soup.encode('utf8')

    # find all regex matches in raw html
    for name, pattern in regex.items():
        data_dict[name] = re.findall(pattern, raw_html)

    # get urls from tags with attributes that contain  a url
    hrefs = soup.find_all(href=True)
    srcs = soup.find_all(src=True)
    for tag in hrefs:
        data_dict['url'].append(tag['href'])
    for tag in srcs:
        data_dict['url'].append(tag['src'])

    # format phone numbers
    data_dict['phone'] = ['({}) {}-{}'.format(t[0].strip(), t[1], t[2].strip())
                          for t in data_dict['phone']]
    return data_dict


def print_data(dic):
    for category, values in dic.items():
        if values:
            print '{} List: \n {} \n'.format(
                category.title(), '\n'.join(format_list(values)))


def format_list(ls):
    # sort list and remove duplicates
    return sorted(list(set(ls)))


def scrape_html(url):
    html_req = requests.get(url)
    data = parse_html_from_src(html_req.text)
    print_data(data)


def main():
    parser = argparse.ArgumentParser(
        description='Print a list of relevant info from a URL')
    parser.add_argument('url',
                        help='a website URL to scrape data from')
    args = parser.parse_args()

    if args.url:
        scrape_html(args.url)


if __name__ == "__main__":
    main()
