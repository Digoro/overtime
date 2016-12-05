import base64
import datetime
import http.cookiejar
import urllib
from datetime import timedelta
from urllib.request import urlopen

from bs4 import BeautifulSoup

from CommentCounter import CommentCounter
from Overtime import OverTime
from pig import Pig


##########################################################################################
# OverTime 수집 Class
class Thief:
    login_url = "http://sigma:9091/dologin.action"

    # 생성자
    # ID = thief Login ID
    # ID = thief Login pwd
    def __init__(self, id, pwd):
        self.payload = {
            "os_username": base64.b64decode(id).decode('utf-8'),
            "os_password": base64.b64decode(pwd).decode('utf-8')
        }
        self.cj = http.cookiejar.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)
        self.thiefHour = 5
        self.setDate()
        self.pig = Pig()
        self.overtime = OverTime(self.thiefDate, self.workDate)
        self.commentCnter = CommentCounter(self.thiefDate)

    def setDate(self):
        self.now = datetime.datetime.now()
        self.thiefDate = datetime.datetime(self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute)
        print(self.thiefDate)
        self.workDate = self.thiefDate - timedelta(hours=11)

    # Confluence Login
    def logIn(self):
        params = urllib.parse.urlencode(self.payload)
        params = params.encode('utf-8')
        req = urllib.request.Request(self.login_url, params)
        self.opener.open(req)

    def getUserImage(self, userID):
        url = "http://sigma:9091/display/~" + str(userID)
        html = self.opener.open(url).read()
        source = BeautifulSoup(html, "html.parser")
        usrImage = "http://sigma:9091"
        if (userID == "wurihan"):
            usrImage += source.find('img', class_="userLogo logo defaultLogo").get('src')  # user image
        else:
            usrImage += source.find('img', class_="userLogo logo").get('src')  # user image
        img = urlopen(usrImage)
        file = open(str(userID) + '.png', 'wb')
        file.write(img.read())
        file.close()

    # Thief 실행
    def run(self, userIDList):
        self.logIn()
        for i in range(0, len(userIDList)):
            # self.getHtml(userIDList[i])
            url = "http://sigma:9091/plugins/recently-updated/changes.action?theme=sidebar&pageSize=9999999&startIndex=0&authors=" + \
                  str(userIDList[
                          i]) + "&spaceKeys=*&contentType=-mail,page,comment,blogpost,attachment,userinfo,spacedesc,personalspacedesc,space,draft,custom"
            html = self.opener.open(url).read()
            # self.getUserImage(userIDList[i])
            self.overtime_ = self.overtime.runOverTime(html)
            self.comment = self.commentCnter.runCounter(html)
            print(userIDList[i], "overtime =", self.overtime_ / 3600, "comment = ", self.comment)
            self.endWorkTime = self.workDate + timedelta(seconds=self.overtime_)
            self.pig.insertOvertime((self.thiefDate,userIDList[i],self.endWorkTime,(self.overtime_ / 3600)))
            self.pig.insertComment((self.thiefDate,userIDList[i],self.comment))
