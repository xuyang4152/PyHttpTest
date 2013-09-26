#coding=utf-8
'''
Created on 2013年9月23日

@author: hongkangzy
'''
import wx
import wx.grid
import csv

class CGridTable(wx.grid.PyGridTableBase):
    def __init__(self,filePath):
        wx.grid.PyGridTableBase.__init__(self)

        self.gridTableDict = dict()
        self.gridTableDict[(0,0)] = 'test_protocal'
        self.gridTableDict[(0,1)] = 'test_host'
        self.gridTableDict[(0,2)] = 'test_path'
        self.gridTableDict[(0,3)] = 'test_method'
        self.gridTableDict[(0,4)] = 'test_sleepTime'
        self.gridTableDict[(0,5)] = 'test_login'
        self.gridTableDict[(0,6)] = 'test_user'
        self.gridTableDict[(0,7)] = 'test_password'

        self.cols = 8
        self.rows = int()
        
        #读取csv文件
        with open(filePath) as csvfile:
            urlInfo = dict()
            #头部信息
            keywordList = csvfile.next()[:-1].split(',')#关键字 [:-1]是为了去掉换行符'\n'
            valueList = csvfile.next()[:-1].split(',')#值 [:-1]是为了去掉换行符'\n'
            for i in range(len(keywordList)):
                urlInfo[keywordList[i]] = valueList[i]
            for i in range(8):
                if urlInfo.has_key(self.gridTableDict[(0,i)]):
                    self.gridTableDict[(1,i)] = urlInfo[self.gridTableDict[(0,i)]]

            paramsInfo = list()
            #参数信息
            dictFileObj = csv.DictReader(csvfile)
            for line in dictFileObj:
                paramsInfo.append(line)

            #构建网格表
            #第三行
            col = 0
            for key in paramsInfo[0].keys():
                if key == '':
                    paramsInfo[0].pop(key)
                    continue
                self.gridTableDict[(2,col)] = key
                col += 1
            if self.cols < col:
                self.cols = col
            #剩余行
            row = 3
            for item in paramsInfo:
                for col in range(len(paramsInfo[0])):
                    key = self.gridTableDict[(2,col)]
                    self.gridTableDict[(row,col)] = item[key]
                row += 1
            self.rows = row
            
    def GetColLabelValue(self,col):
        return ''
    def GetRowLabelValue(self,row):
        if row == 0:
            return 'Control'
        elif row == 1:
            return 'Value'
        elif row == 2:
            return 'Params'
        else:
            return row-3
    def GetNumberRows(self):
        return self.rows
    def GetNumberCols(self):
        return self.cols
    

    def IsEmptyCell(self,row,col):
        return self.gridTableDict.get(row,col) is not None

    def GetValue(self,row,col):
        value = self.gridTableDict.get((row,col))
        if value is not None:
            return value
        else:
            return ''

    def SetValue(self,row,col,value):
        self.gridTableDict[(row,col)] = value.encode('utf-8')

    def GetAttr(self,row,col,kind):
        if row == 0 or row == 2:
            attr = wx.grid.GridCellAttr()
            attr.SetTextColour("navyblue")
            attr.SetBackgroundColour("gold")
            attr.SetFont(wx.Font(12,wx.SWISS,wx.NORMAL,wx.BOLD))
            return attr
        elif row > 2:
            attr = wx.grid.GridCellAttr()
            attr.SetTextColour("navyblue")
            attr.SetBackgroundColour("forest green")
            attr.SetFont(wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL))
            return attr
        elif row == 1:
            attr = wx.grid.GridCellAttr()
            attr.SetTextColour("navyblue")
            attr.SetBackgroundColour("forest green")
            attr.SetFont(wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL))
            return attr
        
        










        
