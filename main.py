# -*- coding: utf-8 -*-   
from PyQt4 import QtGui  
from PyQt4 import QtCore
from login import autoWeb
import sys
import math
import random
import time
from convert import xpmicon
def U( str_):
    return QtCore.QString(str_.decode('utf8'))
class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()
       
        self.setWindowTitle( QtCore.QString(U("登录助手") ))
        self.setSizeGripEnabled(False)
        self.resize( 500, 300 )
        
        self.construct()
        self.createUserconfig()
        self.createRuntime()
        self.createTime()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.userconfig)
        mainLayout.addWidget(self.timeedit)
        mainLayout.addWidget(self.runtime)
        self.texterea = QtGui.QTextEdit()
        #self.texterea.setReadonly ( True )
        mainLayout.addWidget(self.texterea )
        self.texterea.setReadOnly(True)
        self.setLayout(mainLayout)
         
        
        self.createActions()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()
        
        self.sButton.clicked.connect(self.startbutton)
        self.tButton.clicked.connect(self.stop)
        self.cButton.clicked.connect(self.clearScreen)
        if self.autoLogin.hasConfig() :
            self.autoLogin.getconf()
            self.setDefault()

    def setDefault(self) :
        self.name.setText(self.autoLogin.username)
        self.pwd.setText(self.autoLogin.password)
        login = self.autoLogin.logintime.split('-')
        in_start = login[0].split(':')
        in_end = login[1].split(':')
        logout = self.autoLogin.logouttime.split('-')
        out_start = logout[0].split(':')
        out_end = logout[1].split(':')

        
        self.in_start.setTime( QtCore.QTime(int(in_start[0] ) ,int(in_start[1] ) ))
        self.in_end.setTime( QtCore.QTime(int(in_end[0] ) ,int(in_end[1] ) ) )

        self.out_start.setTime( QtCore.QTime(int(out_start[0] ) ,int(out_start[1] ) ))
        self.out_end.setTime( QtCore.QTime(int(out_end[0] ) ,int(out_end[1] ) ) )
        

    def stop(self):
        self.timer.stop()
        self.display(False)
        self.showInfo('服务停止')
    def startbutton(self):
        self.display(True)
        self.showInfo('服务启动')
        self.start()

    def display( self, param):
        '''
        self.name.setReadOnly( param )
        self.pwd.setReadOnly(param )
        self.in_start.setReadOnly(param )
        self.in_end.setReadOnly(param )
        self.out_start.setReadOnly(param )
        self.out_end.setReadOnly(param )
        '''
        self.sButton.setEnabled(not param)
        self.tButton.setEnabled(param)
        self.userconfig.setEnabled(not param)
        self.timeedit.setEnabled(not param)

    def clearScreen(self):
        self.texterea.setText('')
    def getUserinfo(self):
        in_start = self.in_start.time().toString('HH:mm')
        in_end = self.in_end.time().toString('HH:mm')
        out_start = self.out_start.time().toString('HH:mm')
        out_end = self.out_end.time().toString('HH:mm')
        self.autoLogin.logintime = str(in_start + '-' + in_end)
        self.autoLogin.logouttime =str( out_start + '-' + out_end)
        self.autoLogin.username = str(self.name.text() )
        self.autoLogin.password = str(self.pwd.text())
        #str_ = "username : " + self.autoLogin.username + "\r\n" +"pwd :" + self.autoLogin.password + "\r\n"+'logintime :' +self.autoLogin.logintime + "\r\n" +'logouttime :'+  self.autoLogin.logouttime + "\r\n"
        #self.showInfo(str_)
        
       
        
    def createTrayIcon(self):
        
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
       
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    def createActions(self):
        self.minimizeAction = QtGui.QAction(U("最小化"), self,
                triggered=self.hide)

        self.restoreAction = QtGui.QAction(U("还原"), self,
                triggered=self.showNormal)

        self.quitAction = QtGui.QAction(U("退出"), self,
                triggered=QtGui.qApp.quit)

    def createTime(self):
        self.timeedit = QtGui.QGroupBox("")
        gridlayout = QtGui.QGridLayout()

        
        
        label = QtGui.QLabel( U('签入时间范围') )         
        self.in_start = QtGui.QTimeEdit()
        self.in_start.setDisplayFormat( 'HH:mm')
        self.in_start.width = 10
       
        gridlayout.addWidget( label, 0, 0 )
        gridlayout.addWidget( self.in_start, 0, 1 )
        gridlayout.addWidget( QtGui.QLabel('-'), 0, 2 )
        
        self.in_end =  QtGui.QTimeEdit()
        self.in_end.setDisplayFormat( 'HH:mm')
       
        gridlayout.addWidget( self.in_end , 0 , 3)

        label = QtGui.QLabel(  U('签出时间范围') )         
        self.out_start = QtGui.QTimeEdit()
        self.out_start.setDisplayFormat( 'HH:mm')
        gridlayout.addWidget( label, 0, 4 )
        gridlayout.addWidget(  self.out_start, 0, 5 )
        gridlayout.addWidget( QtGui.QLabel('-'), 0, 6 )
        
        self.out_end =  QtGui.QTimeEdit()
        self.out_end.setDisplayFormat( 'HH:mm')
        gridlayout.addWidget(  self.out_end , 0 , 7)

        
        
        self.timeedit.setLayout(gridlayout)
         
        
    def setIcon(self):
        icon = QtGui.QIcon(QtGui.QPixmap(xpmicon ))
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
    def createUserconfig(self):
        self.userconfig = QtGui.QGroupBox("")
        gridlayout = QtGui.QGridLayout()
         
        
        label = QtGui.QLabel( U('用户名') )
        label.setAlignment( QtCore.Qt.AlignCenter )
         
        self.name = QtGui.QLineEdit()
        gridlayout.addWidget( label, 0, 0 )
        gridlayout.addWidget( self.name , 0 , 1)
         
        self.pwd = QtGui.QLineEdit()
        self.pwd.setEchoMode( QtGui.QLineEdit.Password )
        gridlayout.addWidget( self.pwd ,0 ,3)

        labelpwd = QtGui.QLabel(U('密码'))
        labelpwd.setAlignment( QtCore.Qt.AlignCenter )
        gridlayout.addWidget( labelpwd ,0 ,2)
        self.userconfig.setLayout(gridlayout)
        
    def createRuntime(self):
        self.runtime = QtGui.QGroupBox("")
        boxlayout = QtGui.QHBoxLayout()
        self.sButton = QtGui.QPushButton( U('开始'))
        self.tButton = QtGui.QPushButton(U('停止'))
        self.cButton = QtGui.QPushButton(U('清屏'))
        self.tButton.setEnabled(False)
        boxlayout.addWidget( self.sButton   )
        boxlayout.addWidget( self.tButton   )
        boxlayout.addWidget( self.cButton )

        
        self.runtime .setLayout(boxlayout)
        
    
        
    def construct(self) :
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"),self.autoRun)
        self.info = []
        self.autoLogin = autoWeb()
        self.done = ''
        
        #self.start()

    def showInfo(self , info):
        formate = '%Y-%m-%d %H:%M:%S'
        nowtime = str(time.strftime(formate))
        self.info.append(nowtime +':<b> ' + U(info) + '</b><br />')
        while len(self.info) > 8 :
            self.info.remove(self.info[0])

        #str_ = ''.join(str(item) for item in self.info)
        self.texterea.setText('')
        for item in self.info:
            self.texterea.insertHtml(item)

        #self.texterea.scrollToAnchor(nowtime)


    def start(self):
       
        self.getUserinfo()
        if not self.autoLogin.username or not self.autoLogin.password:
            self.showInfo('请输入用户名和密码')
            self.display(False)
            return
        self.autoLogin.saveconf()
        
         
        self.date = str(time.strftime( '%Y-%m-%d' ,time.localtime() ))
        
        #签入时间戳
        self.signin = self.getexectime(self.autoLogin.logintime)
        #签出时间戳
        self.signout = self.getexectime(self.autoLogin.logouttime)

        
        if time.time() <= self.signin and self.done != 'in':
            self.diff = self.signin - time.time()
            self.action = 'in'
            self.nextDay = False
            
        elif  time.time() <= self.signout and self.done !='out':
            self.diff =  self.signout - time.time()
            self.action = 'out'
            self.nextDay = False

        elif time.time() > self.signout :#等第二天签到
            self.diff = self.signin + 86400 - time.time()
            self.action = 'in'
            self.nextDay = True
        
        wday =  time.localtime().tm_wday;
        
        if  self.nextDay == True and wday  == 4 or wday  == 5 or wday  == 6:
          
           self.diff = (7 - wday )* 86400 + time.time()
           
           self.diff = self.diff - self.diff%86400 -time.time()
           self.action = ''

        self.diff = int(math.ceil(self.diff))
        
        if self.diff > 0 :
            formate = '%Y-%m-%d %H:%M:%S'
            s = time.strftime(formate , time.localtime(time.time() + self.diff))
            if self.action :
                s = s + '  将签' + (self.action == 'in' and '入' or '出')
               
            else :
                s = '周末系统暂停,周一将继续为你服务'
                self.action = ''
            self.showInfo(s)
                    
            
        #调用循环方法
        
        self.timer.start( 1000)

    def autoRun(self ):

        exectime = time.strftime('%H:%M:%S')
        #self.showInfo(exectime)
        ac = self.action
        
        if self.diff  <= 0:
            if ac == '':
                self.showInfo('服务启动')
                self.start()
                return False

            for i in range(5) :
                r,uid = self.autoLogin.login()
                if r :
                    self.showInfo('第 %d 次登录 ,成功'%(i+1))
                else :
                    self.showInfo('第 %d 次登录,失败'%(i+1))

                if r :
                    break

                elif i>=4 and not r :
                    self.showInfo('无法登陆')
                    return False
            
            
            if ac == 'in':
                res = self.autoLogin.checkin(exectime)
                self.done  = 'in'
            elif ac == 'out' :
                res = self.autoLogin.checkout(exectime)
                self.done = 'out'
            done = (self.done =='in' and '签入' or '签出')+ ( res and '成功' or '失败')
            self.showInfo( done )
            
            self.start()
        else :
            self.diff = self.diff  -1
                
            


        
    def randtime(self,mintime,maxtime):
        #print mintime , maxtime
        mintime = self.date + ' ' + mintime
        min_ = time.mktime( time.strptime(mintime ,  '%Y-%m-%d %H:%M'))
        if min_ < time.time() :
            min_ = time.time()
        if maxtime == '' :
            max_ = min_+60
        else :
            maxtime = self.date + ' ' + maxtime
       
            max_ = time.mktime( time.strptime(maxtime ,  '%Y-%m-%d %H:%M'))
        min_ = int(min_)
        max_ = int( max_ )
        return max_>min_ and random.randint(min_,max_) or random.randint(max_,min_)

    #返回本次签入/签出的时间戳
    def getexectime(self,_time):

        index = _time.find('-')
        if index < 0:
            
            return self.randtime(_time , '')
        else:
            timelist = _time.split('-')
            return self.randtime(timelist[0] , timelist[1])
            
    def closeEvent(self, event):
       
        if self.trayIcon.isVisible():
            QtGui.QMessageBox.information(self, U("提示"),
                    U("系统将会在后台继续运行"))
            self.hide()
            event.ignore()
   
            
app = QtGui.QApplication( sys.argv )
'''
if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
    QtGui.QMessageBox.critical(None, "Systray",
                    "I couldn't detect any system tray on this system.")
    sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    '''
window = Window()
window.show()

app.exec_()
