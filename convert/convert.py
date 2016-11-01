# coding=utf-8
from collections import defaultdict
import csv
import sys


class convert:

    def __init__(self):
        self.contents = []

    def csv_lst2d(self, file_name):
        with open(file_name) as csvfile:
            middle = csv.reader(csvfile)
            for i in middle:
                i = [ii for ii in i if ii <> '']
                self.contents.append(i)
        return 1

    def markdown_lst2d(self, file_name):  # 待测试
        # '---' as start pattern
        with open(file_name) as file:
            lines = [i.rstrip() for i in file.readlines()]
            lines = [i for i in lines if i <> '']
            if '---' in lines:
                lines = lines[lines.index('---')+1:]
            lst = []
            for i in lines:
                num_spaces = self.count_spaces(i)
                if len(lst) == num_spaces/4:
                    lst.append(i.strip())
                elif len(lst) > num_spaces/4:
                    self.contents.append(lst)
                    lst = []
                    for n in range(num_spaces/4):
                        lst.append(self.contents[-1][n])
                    lst.append(i.strip())
                elif len(lst) < num_spaces/4:
                    lst.append(i.strip())
            self.contents.append(lst)
        return 1

    def lst2d_cards(self):  # key-front，value-back
        cols = 0
        for i in self.contents:
            if len(i) > cols:
                cols = len(i)
        rows = len(self.contents)
        cards = {}
        for col in range(1, cols+1):
            for row in range(1, rows+1):
                if len(self.contents[row-1]) >= (col+1):
                    if '--'.join(self.contents[row-1][:col]) not in cards:
                        cards['--'.join(self.contents[row-1][:col])] = []
                        cards[
                            '--'.join(self.contents[row-1][:col])] .append(self.contents[row-1][col])
                    else:
                        cards[
                            '--'.join(self.contents[row-1][:col])].append(self.contents[row-1][col])
        for i in cards:
            elem = []
            for ii in cards[i]:
                if ii not in elem:
                    elem.append(ii)
                cards[i] = ' \n '.join(elem)
        self.cards = cards
        return 1

    def csv_cards(self, file_name):
        if self.csv_lst2d(file_name):
            self.lst2d_cards()

    def markdown_cards(self, file_name):
        if self.markdown_lst2d(file_name):
            self.lst2d_cards()

    def convert_file(self, file_name):
        file_postfix = file_name.split('.')[1]
        if file_postfix == 'md' or file_postfix == 'txt':
            self.markdown_cards(file_name)
        elif file_postfix == 'csv':
            self.csv_cards(file_name)
        else:
            print 'not a convertable file type'

    def count_spaces(self, txt_line):
        n = 0
        for i in txt_line:
            if i == ' ':
                n += 1
            else:
                break
        return n

    def test(self):
        file_name = '/Users/shen/Desktop/cards/convert/tstfile/' + sys.argv[-1]
        self.convert_file(file_name)
        print '-'*20
        print 'cards_report:'
        for i in sorted(self.cards.keys()):
            print 'Q:'+i + ' :\n' + self.cards[i]
        #print self.cards


if __name__ == '__main__':
    t = convert()
    # t.csv_lst2d('/Users/shen/desktop/sqlite.csv')
    # t.lst2d_cards()
    # t.markdown_lst2d("/Users/shen/Desktop/g.md")
    t.test()
