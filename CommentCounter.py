import re
from bs4 import BeautifulSoup

class CommentCounter:
    def __init__(self, nowDate):
        self.nowDate = nowDate
        self.commentCnt = 0
    def runCounter(self,html):
        self.commentCnt=0
        source = BeautifulSoup(html, "html.parser")
        list = source.find_all("li", class_="update-item")
        for i in range(0,len(list)):
            self.lastestTimeStr = list[i].find_all("li", class_="update-item-desc-and-date")[0].text
            # print("cnt = ",i)
            if (bool(re.search('ago', self.lastestTimeStr))):
                self.counter(self.lastestTimeStr)
            elif(bool(re.search('yesterday', self.lastestTimeStr))):
                self.counter(self.lastestTimeStr)
            else :
                return self.commentCnt
        return self.commentCnt

        # Confluence 최근 업데이트 기록 string splite
    def counter(self, log):
        if (bool(re.search('comment', log))):
            self.commentCnt+=1