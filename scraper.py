#!/usr/bin/env python2
import argparse
import requests
import re
from bs4 import BeautifulSoup


__author__ = 'Jake Johnson'

regex = {
    'phone': r"(?:\D)(\(?\d{1})(\(?\d{3})\D{0,3}(\d{3})\D{0,3}(\d{4})\D",
    'email': r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
    'url': (r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]"
            r"|(?:%[0-9a-fA-F][0-9a-fA-F]))[^\)\"';\s]+")
}


def parse_data_from_src(data):
    """scan html and build a dict of
     regex matches for phone, email, and URLs"""
    data_dict = dict()
    soup = BeautifulSoup(data, 'html.parser')
    html = soup.encode('utf8')

    # find all regex matches in raw html
    for name, pattern in regex.items():
        data_dict[name] = re.findall(pattern, html)

    # get urls from tags with attributes that contain  a url
    hrefs = soup.find_all(href=True)
    srcs = soup.find_all(src=True)
    for tag in hrefs:
        data_dict['url'].append(tag['href'])
    for tag in srcs:
        data_dict['url'].append(tag['src'])

    # format phone numbers
    data_dict['phone'] = ['({}) {}-{}'.format(t[0], t[1], t[2])
                          for t in data_dict['phone']]
    return data_dict


def print_data(data_dict):
    """output formatted data if it exists"""
    for category, values in data_dict.items():
        if values:
            print '{} List: \n{} \n'.format(
                category.title(), (format_data(values)))


def format_data(ls):
    """sort a list, remove its duplicates,
    and create a new string with each item on a new line"""
    return '\n'.join(sorted(list(set(ls))))


def main():
    parser = argparse.ArgumentParser(
        description='Print a list of relevant info from a URL')
    parser.add_argument('url',
                        help='a website URL to scrape data from')
    args = parser.parse_args()

    if args.url:
        req = requests.get(args.url)
        data = parse_data_from_src(req.text)
        print_data(data)


if __name__ == "__main__":
    main()
