import re
from bs4 import BeautifulSoup

class OverTime:
    def __init__(self, nowDate, workDate):
        self.nowDate = nowDate
        self.workDate = workDate
    def runOverTime(self, html):
        source = BeautifulSoup(html ,"html.parser")
        list = source.find_all("li" ,class_ ="update-item")
        self.lastestTimeStr = list[0].find_all("li", class_="update-item-desc-and-date")[0].text
        if(bool(re.search('ago',self .lastestTimeStr))):
            return self.calOvertime(self.lastestTimeStr)
        return 0
        # Confluence 최근 업데이트 기록 string splite
    def calOvertime(self, log) :
        splitLog = log.split()
        stridx = splitLog.__len__() - 1
        if( bool(re.search('hour',log) )):
            if( splitLog[stridx-2]. isdigit()):
                return self.calTime(3600 * int(splitLog[stridx - 2]))
            else:
                return self.calTime(3600)
        elif(bool (re.search('minute',log)) ):
            if (splitLog[stridx - 2].isdigit()):
                return self.calTime(60 * int(splitLog[stridx - 2]))
            else:
                return self.calTime(60 * 1)
        return self.calTime(60)
        # Overtime 계산
    def calTime(self, lastestTime):
        subDate = self.nowDate - self.workDate
        return subDate.seconds- lastestTime