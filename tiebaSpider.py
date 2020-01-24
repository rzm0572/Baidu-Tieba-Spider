# -*- coding: utf-8 -*-
# Author: rzm
# Create time: 2020/01/24 11:01

import requests as r
import re
from bs4 import BeautifulSoup


class TiebaSpider(object):
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/55.0.2883.87 Safari/537.36'}
    total_page = -1
    page_title = ""
    lz = ""
    contents = ""

    def __init__(self, number, path, add_info=False, only_lz=True):
        self.get_page_info(number, only_lz)
        self.get_contents(number, path, add_info, only_lz)

    def get_page_info(self, number, only_lz=True):
        url = "https://tieba.baidu.com/p/%s?see_lz=%d" % (str(number), only_lz)

        try:
            first_page = r.get(url, headers=self.HEADER)
        except r.ConnectionError or r.HTTPError:
            raise Exception("Connection error!")
        first_page_html = first_page.text
        first_page_soup = BeautifulSoup(first_page_html, 'lxml')
        total_page_div = first_page_soup.find('ul', class_='l_posts_num')
        self.page_title = first_page_soup.find('h3', class_='core_title_txt pull-left text-overflow').string
        self.lz = first_page_soup.find('a', class_=re.compile('p_author_name')).contents[0].string
        total_page_string = total_page_div.contents[3].contents[2].string
        if total_page_string.isdigit():
            self.total_page = int(total_page_string)
        else:
            self.total_page = -1
        return [self.total_page, self.page_title, self.lz]

    def get_contents(self, number, path, add_info=False, only_lz=True):
        if self.total_page == -1:
            self.contents = ""
            raise Exception("Page not found.")
        url = "https://tieba.baidu.com/p/%s?see_lz=%d&pn=" % (str(number), only_lz)

        file = open(path, 'w+', encoding='utf-8')
        self.contents += self.page_title + ' by ' + self.lz + '\n\n\n'
        file.write(self.contents)
        self.contents = ""

        for page_number in range(1, self.total_page + 1):
            try:
                page = r.get(url + str(page_number), headers=self.HEADER)
            except r.ConnectionError or r.HTTPError:
                raise Exception("Connection error!")
            print("Connection OK!")
            page_html = page.text
            page_soup = BeautifulSoup(page_html, 'lxml')
            posts = page_soup.find_all('div', class_='d_post_content j_d_post_content')
            info = []
            cz = []
            if add_info:
                info = page_soup.find_all('div', class_='post-tail-wrap')
                if not only_lz:
                    cz = page_soup.find_all('a', class_=re.compile('p_author_name'))

            for post in posts:
                if add_info:
                    idx = posts.index(post)
                    self.contents += info[idx].find('span', string=re.compile('[1-9][0-9]*楼')).string + ' ' + \
                                     info[idx].find('span', string=re.compile('(19|20)[0-9]{2}-(0?[0-9]|1[0-2])-'
                                                                              '(0?[1-9]|[12][0-9]|3[01]) ([01][0-9]'
                                                                              '|2[0-3]):([0-5][0-9])')).string
                    if not only_lz:
                        self.contents += ' by ' + cz[idx].contents[0].string
                    self.contents += '\n'
                self.contents += post.get_text('\n', 'br/') + '\n\n'
                self.render(file)
            print("Download page %d OK!" % page_number)

    def render(self, file):
        if self.total_page == -1:
            raise Exception("Page not found.")

        try:
            file.write(self.contents)
        except FileExistsError or FileNotFoundError:
            raise Exception("File error!")
        finally:
            self.contents = ""


if __name__ == "__main__":
    pass
    # test = TiebaSpider("6457834799", add_info=True)
    # test.print_to_screen()
    # test.render(r"D:\RZM\project\tieba_spider\test\test.txt")
