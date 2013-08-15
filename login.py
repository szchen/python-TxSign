#coding=utf-8

from AutoLogin import Myimage
from BeautifulSoup import BeautifulSoup
from PIL import Image
import StringIO
import cookielib
import httplib2
import os
import sys
import re
import types
import time
import urllib
import urllib2


class autoWeb():
    def __init__(self):
        
        self.configFile = r'D:\AutoLoginConfig.ini'

        self.homeurl = r"http://rd.tencent.com/top/ptlogin/ptlogins/login?site=TAPD&ref=http%3A%2F%2Frd.tencent.com%2Foutsourcing%2F"

        self.mi =  Myimage()
        headers = { 
        "Accept":"image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/6.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0)",
        "Host":"rd.tencent.com",
        "Connection": "Keep-Alive"
        }
        cj = cookielib.CookieJar()  
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.opener.addheaders = [(k, v) for k, v in headers.iteritems()] 




    def hasConfig(self):
        return os.path.exists(self.configFile)


    def getconf(self):
        cf=open(self.configFile,'r')
        self.username=cf.readline().split("username=")[-1].strip()
        self.password=cf.readline().split("password=")[-1].strip()
        self.logintime = cf.readline().split("=")[-1].strip()
        self.logouttime = cf.readline().split("=")[-1].strip()

    def saveconf(self) :
        cf=open(self.configFile,'w')
        cf.write("username="+self.username+"\n")
        cf.write("password="+self.password+"\n")
        cf.write("logintime="+self.logintime+"\n")
        cf.write("logouttime="+self.logouttime)
        cf.close()

    def getToken(self):
        imageurl = r"http://rd.tencent.com/top/ptlogin/ptlogins/securimage?sid=&#39"
        #content = self.opener.open(imageurl, "").read()
        content = self.opener.open(imageurl ).read()
        stream = StringIO.StringIO(content)
        image = Image.open(stream)
        #image.save("securimage.png")
        return image

    def login(self):
        self.mi.init(self.getToken())
        token = self.mi.domain()
        loginurl = r"http://rd.tencent.com/top/ptlogin/ptlogins/login?ref=http%3A%2F%2Frd.tencent.com%2Foutsourcing"
        idurl = "http://rd.tencent.com/outsourcing/"
        key=""
        for i in range(len(token)):
            key=key+token[i].strip()
       
        params = { 
            "data[Login][ref]":"http://rd.tencent.com/",
            "data[Login][site]":"TAPD",
            #"data[Login][via]":"encrypt_password",
            "data[Login][name]":self.username,
            "data[Login][password]":self.password,
            "data[Login][code]":key,
            "data[Login][login]":"login"
            }
        data = [(k, v) for k, v in params.iteritems()]  
        content = self.opener.open(loginurl, data=urllib.urlencode(data)).read()
        #print content
        content = self.opener.open(idurl, "").read()
        soup = BeautifulSoup(''.join(content))

        user_infor = soup.findAll(id="user_infor")
        if len(user_infor) == 1:
            os.system("color 1E")
            #print u"-----------------------        登录成功！        ------------------------"
            #print ""
            attendance_id = soup.findAll(id="attendance_id")
            if len(attendance_id) == 1:
                self.uid = (str(attendance_id[0]).split("value=\""))[-1][:6]
                #print "UID==", self.uid,u",可以签出~"
            else:
                self.uid=0
                #print u"没有UID，可以签入~"
            return True,self.uid
        else:
            os.system("color 4E")
            #print u"XXXXXXXXXX    登录失败！    XXXXXXXXXX"
            #print "--------------------------------------------------------------------------"
            return False,0


    def checkout(self,time_):
        params_out = {
        "_method":"POST",
        "data[Attendance][check_out]":time_,
        "data[Attendance][check_out_remark]":"",
        "data[Attendance][id]":self.uid
        }
        checkouturl = r"http://rd.tencent.com/outsourcing/attendances/edit/" + self.uid + "/TAPD"
        data = [(k, v) for k, v in params_out.iteritems()]
        content = self.opener.open(checkouturl, data=urllib.urlencode(data)).read()
        soup = BeautifulSoup(''.join(content))
        flashMessage = soup.findAll(id="flashMessage")     
        if len(flashMessage)==1 and "Check out successfully" in str(flashMessage[0]):
            #check_out_success_tip = soup.findAll(id="check_out_success_tip")
            #print "check_out_success_tip====",str(check_out_success_tip).decode("utf8")
            print u"-----------------------        签出成功！        ------------------------"
            print ""
            return True
        else:
            os.system("color 4E")
            print u"XXXXXXXXXX    签出失败！    XXXXXXXXXX"
            return False
    

    def checkin(self,time_):
        checkinurl="http://rd.tencent.com/outsourcing/attendances/add?from=TAPD"
        params_in = {
            "_method":"POST",
            "data[Attendance][check_in]":time_,
            "data[Attendance][check_in_remark]" : "",
            "data[Attendance][city_id]":"1",
            "data[Attendance][office_building_id]":"4",
            "data[Attendance][floor]":"16",
            "data[Attendance][is_check_first]":""
        }
        data = [(k, v) for k, v in params_in.iteritems()]
        content = self.opener.open(checkinurl, data=urllib.urlencode(data)).read()
        #print content
        soup = BeautifulSoup(''.join(content)) 
        flashMessage = soup.findAll(id="flashMessage")
        #print buycount
        if len(flashMessage)==1 and "Check in successfully" in str(flashMessage[0]): 
            return u"-----------------------        签入成功！        ------------------------"
           
        else:
            os.system("color 4E")
            return u"XXXXXXXXXX    签出失败！    XXXXXXXXXX"
            



        
