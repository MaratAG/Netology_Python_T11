"""Программа по подсчету частоты использования слов в новостных файлах."""


import json
import operator

import chardet


class Newsfile(object):
    """Класс - новостной файл."""

    name = None
    encoding = None
    news = ''
    words = None

    def __init__(self, filename, file_format, code_file=None):
        """Объявление класса и чтение файла в аттрибуты экземпляра класса."""
        if file_format == 'txt':
            self.news = self.open_file_txt(filename).decode(self.encoding)
        elif file_format == 'json':
            self.news = self.open_file_json(filename, code_file)
        self.name = filename

    def open_file_txt(self, filename):
        """Открытие файла формата txt."""
        with open(filename, 'rb') as f:
            news = f.read()
            attribs_file = chardet.detect(news)
            self.encoding = attribs_file['encoding']
            return news

    def open_file_json(self, filename, code_file):
        """Открытие файла формата json."""
        with open(filename, encoding=code_file) as f:
            news = json.load(f)
            self.encoding = 'json, ' + code_file
            return news

    def countword(self, count_text, n):
        """Подсчет количества слов в тексте."""
        our_list = list(count_text.split())
        for item in our_list:
            if len(item.strip()) >= n:
                if self.words.get(item) is None:
                    self.words[item] = 1
                else:
                    self.words[item] += 1

    def count_top(self, n=6):
        """Подсчет количества слов в файле. Определение рейтинга слов."""
        self.words = {}
        if self.encoding.find('json') != -1:
            news = self.news['rss']['channel']['items']
            for piece_of_news in news:
                self.countword(piece_of_news['title'], n)
                self.countword(piece_of_news['description'], n)
        else:
            self.countword(self.news, n)

        self.words = sorted(self.words.items(),
                            key=operator.itemgetter(1), reverse=True)

    def print_top(self, top):
        """Вывод топ-рейтинга слов."""
        print('Файл {}, кодировка {}'.format(self.name, self.encoding))
        count = 0
        for key, value in self.words:
            print('Слово: "{}", частота использования: {}'.format(key, value))
            count += 1
            if count == top:
                break
        print('----------')


def work_with_file(files, type_of_file, n, top, code_page):
    """Выполнение операций над файлами."""
    file_1 = Newsfile('' + files[0] + '.'
                      + type_of_file, type_of_file, code_page[0])
    file_2 = Newsfile(files[1] + '.'
                      + type_of_file, type_of_file, code_page[1])
    file_3 = Newsfile(files[2] + '.'
                      + type_of_file, type_of_file, code_page[2])
    file_4 = Newsfile(files[3] + '.'
                      + type_of_file, type_of_file, code_page[3])

    file_1.count_top(n)
    file_2.count_top(n)
    file_3.count_top(n)
    file_4.count_top(n)

    file_1.print_top(top)
    file_2.print_top(top)
    file_3.print_top(top)
    file_4.print_top(top)


def main():
    """Инициализация программы."""
    files = ['newsafr', 'newscy', 'newsfr', 'newsit']
    top = 10

    n = 0
    while n <= 0:
        n = int(input('Длина слова для анализа (не менее символов):'))

    # Файлы формата txt.
    work_with_file(files, 'txt', n, top, [None, None, None, None])

    # Файлы формата json.
    work_with_file(files, 'json', n, top,
                   ['utf-8', 'KOI8-R', 'ISO-8859-5', 'windows-1251'])


main()
