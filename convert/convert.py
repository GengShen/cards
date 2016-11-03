# coding=utf-8
from collections import defaultdict
import csv
import sys
import sqlite3
#import ast


class convert:

    def __init__(self, file_name, type_data = 'general'):
        self.contents = []
        self.file_name = file_name
        #self.type_dict = ast.literal_eval(open('').read().replace('\n',''))
        self.type_dict = {
            'general': 0,
            'english': 1,
            'math': 2,
            'computer': 3,
            'code': 4,
        }
        self.type_int = self.type_dict.get(type_data)
        if not self.type_int:
            self.type_int = 0

    def csv_lst2d(self):
        with open(self.file_name) as csvfile:
            middle = csv.reader(csvfile)
            for i in middle:
                i = [ii for ii in i if ii <> '']
                self.contents.append(i)
        return 1

    def markdown_lst2d(self):  # 待测试
        # '---' as start pattern
        with open(self.file_name) as file:
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
                            '--'.join(self.contents[row-1][:col])].append(
                                self.contents[row-1][col])
                    else:
                        cards[
                            '--'.join(self.contents[row-1][:col])].append(
                                self.contents[row-1][col])
        for i in cards:
            elem = []
            for ii in cards[i]:
                if ii not in elem:
                    elem.append(ii)
                cards[i] = ' \n '.join(elem)
        self.cards = cards
        return 1

    def csv_cards(self):
        if self.csv_lst2d():
            self.lst2d_cards()

    def markdown_cards(self):
        if self.markdown_lst2d():
            self.lst2d_cards()

    def convert_file(self):
        file_postfix = self.file_name.split('.')[1]
        if file_postfix == 'md' or file_postfix == 'txt':
            self.markdown_cards()
        elif file_postfix == 'csv':
            self.csv_cards()
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

    def exp_database(self):
        conn = sqlite3.connect("../cards.db")  # 注意修改
        sql_statement_raw = \
            'insert into cards(type,front,back) values (%i,%s,%s)'
        n = 0
        for i in self.cards:
            sql_statement = sql_statement_raw % (
                self.type_int, '\''+i.replace('\'', '‘')+'\'', '\'' +
                self.cards[i].replace('\'', '‘') + '\'')
            conn.execute(sql_statement)
            n += 1
        conn.commit()
        print str(n)+' Done'

    def convert_to_database(self):

        self.convert_file()
        self.exp_database()


def test():
    file_name = '/Users/shen/Desktop/cards/convert/tstfile/' + sys.argv[-2]
    type_d = sys.argv[-1]
    t = convert(file_name, type_d)
    t.convert_to_database()


if __name__ == '__main__':
    test()
