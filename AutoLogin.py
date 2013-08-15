# coding:gbk
from PIL import Image
import os, sys

import IMAGEDIR

x = 30
y = 30  
n_x = (128, 128, 255)  # 干扰线颜色
n_y1 = (128, 191, 255)  # 网格颜色
n_y2 = (227, 218, 237)  # 背景色
    
t_b = (255, 255, 255)  # 白色底
t_w = (0, 0, 0)  # 黑色字

class Myimage():
    
    def init(self, img):
        # 去除底色和网格
        self.img = img
        self.img = self.img.convert("RGB")
        self.pixdata = self.img.load()
        self.imgX = self.img.size[0]
        self.imgY = self.img.size[1]
        self.a = [(["-"] * self.imgX) for o in range(self.imgY)]

        for y in xrange(self.imgY):
            for x in xrange(self.imgX):
                if self.pixdata[x, y] == n_y1 or self.pixdata[x, y] == n_y2:
                    self.pixdata[x, y] = t_w
                elif self.pixdata[x, y] == n_x:
                    self.a[y][x] = 0
                else:
                    self.a[y][x] = "@"
                    
    def allX(self, tempi):
        if tempi == 1 or tempi == 2:  # 左右
            for yy in xrange(self.imgY):
                isContinue = False  # 是否左连续
                for xx in xrange(self.imgX):
                    if tempi == 1:  
                        x = xx
                        y = yy
                        if self.pixdata[x, y] == n_x:
                            if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                if self.pixdata[x - 1, y ] not in(n_x, t_w) or isContinue == True:  # 从左往右
                                    isContinue = True
                                    self.a[y][x] += 1
                                    pass                      
                                else:
                                    isContinue = False
                    elif tempi == 2: 
                        x = self.imgX - xx - 1
                        y = self.imgY - yy - 1
                        pass
                        if self.pixdata[x, y] == n_x:
                            if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                if self.pixdata[x + 1, y ] not in(n_x, t_w) or isContinue == True:  # 从右往左
                                    isContinue = True
                                    self.a[y][x] += 1
                                    pass                      
                                else:
                                    isContinue = False
                                    
        elif tempi == 3 or tempi == 4:  # 上下
            for xx in xrange(self.imgX): 
                isContinue = False  # 是否连续
                for yy in xrange(self.imgY):
                    if tempi == 3:  
                        x = self.imgX - xx - 1
                        y = yy   
                        if self.pixdata[x, y] == n_x: 
                            if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                if self.pixdata[x , y - 1 ] not in(n_x, t_w) or isContinue == True:  # 从上往下
                                    isContinue = True
                                    self.a[y][x] += 1
                                    pass                      
                                else:
                                    isContinue = False
                    if tempi == 4: 
                        x = xx
                        y = self.imgY - yy - 1            
                        if self.pixdata[x, y] == n_x: 
                            if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                if self.pixdata[x , y - 1 ] not in(n_x, t_w) or isContinue == True:  # 从下往上
                                    isContinue = True
                                    self.a[y][x] += 1
                                    pass                      
                                else:
                                    isContinue = False
                                    
        elif tempi == 5 or tempi == 6:  # 反斜
            for ii in range(self.imgX + self.imgY - 1):
                isContinue = False
                for jj in range(self.imgY):   
                    if tempi == 5:  
                        xx = ii
                        yy = jj
                        if ((xx - yy) >= 0)and (((xx - yy) < self.imgX)): 
                            x = xx - yy
                            y = yy
                            if self.pixdata[x, y] == n_x: 
                                if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                    if self.pixdata[x + 1 , y - 1 ] not in(n_x, t_w) or isContinue == True:  # #从右上到左下
                                        isContinue = True
                                        self.a[y][x] += 1
                                        pass                      
                                    else:
                                        isContinue = False
                    if tempi == 6: 
                        xx = ii
                        yy = self.imgY - 1 - jj
                        if ((xx - yy) >= 0)and (((xx - yy) < self.imgX)): 
                            x = xx - yy
                            y = yy
                            if self.pixdata[x, y] == n_x: 
                                if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                    if self.pixdata[x - 1 , y + 1 ] not in(n_x, t_w) or isContinue == True:  # #从左下到右上
                                        isContinue = True
                                        self.a[y][x] += 1
                                        pass                      
                                    else:
                                        isContinue = False
                                        
        elif tempi == 7 or tempi == 8:  # 正斜
            for ii in range(self.imgX + self.imgY - 1):
                isContinue = False
                for jj in range(self.imgY):   
                    if tempi == 7:  
                        xx = ii - self.imgY + 1
                        yy = jj
                        if ((xx + yy) >= 0)and (((xx + yy) < self.imgX)): 
                            x = xx + yy
                            y = yy
                            if self.pixdata[x, y] == n_x: 
                                if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                    if self.pixdata[x - 1 , y - 1 ] not in(n_x, t_w) or isContinue == True:  # #从左上到右下
                                        isContinue = True
                                        self.a[y][x] += 1
                                        pass                      
                                    else:
                                        isContinue = False
                    if tempi == 8: 
                        xx = ii - self.imgY + 1
                        yy = self.imgY - 1 - jj
                        if ((xx + yy) >= 0)and (((xx + yy) < self.imgX)): 
                            x = xx + yy
                            y = yy
                            if self.pixdata[x, y] == n_x: 
                                if x != 0 and x != self.imgX - 1 and y != 0 and y != self.imgY - 1:
                                    if self.pixdata[x + 1 , y + 1 ] not in(n_x, t_w) or isContinue == True:  # #从右下到左上
                                        isContinue = True
                                        self.a[y][x] += 1
                                        pass                      
                                    else:
                                        isContinue = False
    
    def fix(self):  # 设为黑白
        for y in xrange(self.imgY):
            for x in xrange(self.imgX):
                if self.a[y][x] >= 4 and self.a[y][x] != "!" and self.a[y][x] != "-" :
                    self.pixdata[x, y] = t_b
                elif self.a[y][x] < 4 :
                    self.pixdata[x, y] = t_w

    def getIResultImgs(self):
        self.resultImage = []
        for i in range(8):
            self.allX(i)
        self.fix()
        #self.img.save("temp.png")
        totle = 0
        biginX = 0
        isOK = False
        for x in range(self.imgX):
            for y in range(self.imgY):
                if self.pixdata[x, y] == t_b:
                    isOK = True
                    break
            else:
                if isOK == True:
                    box = (biginX, 0, x + 1, self.imgY)
                    xim = self.img.crop(box)
                    #if not os.path.exists("Temp"):
                    #    os.makedirs("Temp")
                    #xim.save("Temp\\"+str(totle)+".png")
                    self.resultImage.append(xim)
                    totle += 1
                    biginX = x + 1
                    isOK = False
         
    def drawRectangle(self, image):
        '''
        image为白色字体,其他为黑色
        画一个矩形，返回面积
        '''
        imgX = image.size[0]
        imgY = image.size[1]
        self.lii = []
        self.liy = []
        pixData = image.load()
        for i in range(imgX):
            for j in range(imgY):
                if pixData[i, j] == (255, 255, 255):
                    self.lii.append(i)
                    self.liy.append(j)  
        if(len(self.lii)==0):
            return 999  
        return (max(self.lii) - min(self.lii)) * (max(self.liy) - min(self.liy))
    
    def putRight(self):
        '''
        摆正图片，缩放为30*30
        '''
        for index in range(len(self.resultImage)):
            image = self.resultImage[index]
            size = self.drawRectangle(image)
            angle = 0
            for i in range (-30, 30, 1):
                imageinit = image.rotate(i)
                if self.drawRectangle(imageinit) <= size:
                    size = self.drawRectangle(imageinit)
                    angle = i  
                    self.finSize = (min(self.lii), min(self.liy), max(self.lii), max(self.liy))
                    
            #print "xxxxxxxxx=", angle
            image = image.rotate(angle)
            image2 = image.crop(self.finSize)
            #image2.save("abc.png")
            self.resultImage[index] = image2.resize((x, y))#调整为30*30
    
    def compare(self):
        resultList = []
        for index in range(len(self.resultImage)):
            maxsum = 0
            maxfilename = ""
            timg = self.resultImage[index]
            #for dirname, dirs, filenames in os.walk("a"):
            for abc in IMAGEDIR.IMAGEDIR:
                #标准图片库
                    list1 = self.imageto1_0(timg)
                    list2 = IMAGEDIR.IMAGEDIR[abc]
                    sum = 0
                    for i in range(len(list1)):
                        if list1[i]==list2[i]:
                            sum+=1
                    #timg.close()
                    #image2.close()
                    if sum > maxsum:
                        maxsum = sum
                        maxfilename = abc
            resultList.append(maxfilename[0])
        return resultList
    
    def imageto1_0(self,image):
        list=[]
        pix=image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if pix[i,j] ==(255,255,255):
                    list.append(1)
                else : list.append(0)
        return list
    
    def domain(self):
        self.getIResultImgs()
        self.putRight()
        return self.compare()