from pig import Pig
import datetime
import operator


class Computer:
    # 생성자
    # Pig 모듈 생
    def __init__(self):
        self.p = Pig()

    # start ~ end 기간동안 person의 야근 시간 조회
    def getPersonalOvertime(self, person, start, end):

        list = self.p.personalOverTimeList(self.p.getConfluenceID(person), start, end)
        overtime = 0
        for item in list:
            overtime += item[3]
        return self.p.getMember(self.p.getConfluenceID(person)), overtime

    # start ~ end 기간동안 person의 Comment 수 조회
    def getPersonalComments(self, person, start, end):
        list = self.p.personalCommentsList(self.p.getConfluenceID(person), start, end)
        comments = 0
        for item in list:
            comments += item[2]
        return self.p.getMember(self.p.getConfluenceID(person)), comments

    # start ~ end 기간동안 모든 member의 야근 시간 조회
    def getOvetimes(self, start, end):
        list = self.p.getMembers()
        overtimes = []
        for member in list:
            overtimes.append(self.getPersonalOvertime(member[1], start, end))
        return sorted(overtimes, key=operator.itemgetter(1), reverse=True)

    # start ~ end 기간동안 모든 member의 Comment 수 조회
    def getComments(self, start, end):
        list = self.p.getMembers()
        comments = []
        for member in list:
            comments.append(self.getPersonalComments(member[1], start, end))
        return sorted(comments, key=operator.itemgetter(1), reverse=True)

    # String 포맷 -> datetime 포맷 변환
    # 예) StrToDatetime("2016/10/30/17/47")
    def StrToDatetime(self, str):
        splitted = str.split('/')
        intdata = list(map(lambda a: int(a), splitted))
        return datetime.datetime(intdata[0], intdata[1], intdata[2], intdata[3], intdata[4])
