import sqlite3

class Pig:
    # 생성자
    # DB 로드
    def __init__(self):
        self.db = sqlite3.connect("gsdb.sqlite")
        self.cur = self.db.cursor()

    # 야근시간 입력
    # 예) insertOvertime((datetime.datetime(2016,10,30,5,00),"woonghu",datetime.datetime(2016,10,29,21,00),3))
    def insertOvertime(self, d):
        self.cur.execute("insert into OVERTIME values (?,?,?,?)",d)
        self.db.commit()

    # Comment 수 입력
    # 예) insertComment((datetime.datetime(2016,10,30,5,00),"woonghu",2))
    def insertComment(self, d):
        self.cur.execute("insert into COMMENTS values (?,?,?)",d)
        self.db.commit()

    # OVERTIME Table 조회
    def getOvertimes(self):
        self.cur.execute("SELECT * FROM OVERTIME")
        return self.cur.fetchall()

    # COMMENTS Table 조회
    def getComments(self):
        self.cur.execute("SELECT * FROM COMMENTS")
        return self.cur.fetchall()

    # MEMBER Table 조회
    def getMembers(self):
        self.cur.execute("SELECT * FROM MEMBER")
        return self.cur.fetchall()

    # 모든 MEMBER의 confluence ID 조회
    def getConfluenceIDs(self):
        confluenceids = []
        for member in self.getMembers():
            confluenceids.append(member[4])
        return confluenceids

    # 이름으로 Confluence ID 조회
    def getConfluenceID(self, name):
        self.cur.execute("SELECT CONFLUENCE_ID FROM MEMBER WHERE MEMBER.NAME='%s'" % name)
        return self.cur.fetchall()[0][0]

    # start ~ end 기간까지 person의 OVERTIME Table 데이터 조회
    # 예) personalOverTimeList(p.getConfluenceID("한우리"),datetime.datetime(2016,10,25),datetime.datetime(2016,10,29))
    def personalOverTimeList(self,person, start, end):
        self.cur.execute("SELECT * FROM (SELECT * FROM OVERTIME WHERE CONFLUENCE_ID='%s') WHERE DAY between '%s' and '%s'" % (person, start, end))
        return self.cur.fetchall()

    # start ~ end 기간까지 person의 COMMENT Table 데이터 조회
    # 예) personalCommentsList(p.getConfluenceID("한우리"),datetime.datetime(2016,10,25),datetime.datetime(2016,10,29))
    def personalCommentsList(self,person, start, end):
        self.cur.execute("SELECT * FROM (SELECT * FROM COMMENTS WHERE CONFLUENCE_ID='%s') WHERE DAY between '%s' and '%s'" % (person, start, end))
        return self.cur.fetchall()

    def getAllMemberIDs(self):
        self.cur.execute("SELECT CONFLUENCE_ID FROM MEMBER")
        return self.cur.fetchall()

    def getMember(self,person):
        self.cur.execute("SELECT * FROM MEMBER WHERE CONFLUENCE_ID='%s'" % person)
        return self.cur.fetchall()

    def setMemberImage(self, person, image):
        self.cur.execute("UPDATE IMAGE SET IMAGE_PATH = '%s' WHERE CONFLUENCE_ID='%s'" % (image, person))
        return self.cur.fetchall()

    def getMemberImage(self, person):
        self.cur.execute("SELECT IMAGE_PATH FROM IMAGE WHERE CONFLUENCE_ID='%s'" % person)
        return self.cur.fetchall()

    # DB 연결 종료
    def close(self):
        self.db.close()