"""Программа по подсчету частоты использования слов в новостных файлах."""


import operator

import chardet


class Newsfile(object):
    """Класс - новостной файл."""

    name = None
    encoding = None
    news = None
    words = None

    def __init__(self, filename):
        """Объявление класса и чтение файла в аттрибуты экземпляра класса."""
        with open(filename, 'rb') as f:
            news = f.read()
            attribs_file = chardet.detect(news)

            self.name = filename
            self.encoding = attribs_file['encoding']
            self.news = news.decode(self.encoding)

    def count_top(self, n=6):
        """Подсчет количества слов в файле. Определение рейтинга слов."""
        self.words = {}
        our_list = list(self.news.split())
        for item in our_list:
            if len(item.strip()) >= n:
                if self.words.get(item) is None:
                    self.words[item] = 1
                else:
                    self.words[item] += 1
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


def main():
    """Инициализация программы."""
    n = 0
    while n <= 0:
        n = int(input('Длина слова для анализа (не менее символов):'))

    file_1 = Newsfile('newsafr.txt')
    file_2 = Newsfile('newscy.txt')
    file_3 = Newsfile('newsfr.txt')
    file_4 = Newsfile('newsit.txt')

    file_1.count_top(n)
    file_2.count_top(n)
    file_3.count_top(n)
    file_4.count_top(n)

    file_1.print_top(10)
    file_2.print_top(10)
    file_3.print_top(10)
    file_4.print_top(10)


main()
