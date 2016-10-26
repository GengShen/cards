from collections import defaultdict
import csv






class convert:
    def __init__(self):
        self.contents = []

    def csv_lst2d(self,file_name):
        with open(file_name) as csvfile:
            middle = csv.reader(csvfile)
            for i in middle:
                self.contents.append(i)
        return 1
    def lst2d_cards(self):#返回cards字典,key-front，value-back
        cols = 0
        for i in self.contents:
            if len(i) > cols:
                cols = len(i)
        rows = len(self.contents)
        cards = {}
        for col in range(1,cols+1):
            for row in range(1,rows+1):
                if len(self.contents[row-1]) >= (col+1):
                    if self.contents[row-1][col-1] not in cards:
                        cards[self.contents[row-1][col-1]] = []
                        cards[self.contents[row-1][col-1]] .append(self.contents[row-1][col])
                    else:
                        cards[self.contents[row-1][col-1]].append(self.contents[row-1][col])
        for i in cards:
            elem = []
            for ii in cards[i]:
                if ii not in elem:
                    elem.append(ii)
                cards[i] = ' \n '.join(elem)
        return cards



    
   



if __name__ == '__main__':
    t = convert()
    t.csv_lst2d('/Users/shen/desktop/sqlite.csv')
    t.lst2d_cards()
    