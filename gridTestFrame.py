#coding = utf-8
'''
Created on 2013年9月24日

@author: hongkangzy
'''
import wx
import wx.lib.buttons as buttons
import wx.grid
import gridTable
import sys
import thread
import urllib2
import httplib
import json
import time
import os

class CGridTestFrame(wx.Frame):
    def __init__(self,parent,filePath):
        wx.Frame.__init__(self,parent,-1,'Test Case',name='TestCase')
        self.SetBackgroundColour(wx.Color(204,232,207))
        self.Maximize()

        self.panel = wx.Panel(self,-1)
        
        #网格表
        self.grid = wx.grid.Grid(self.panel,-1)
        self.grid.SetDefaultColSize(130,True)
        self.grid.SetDefaultRowSize(30,True)
        self.table = gridTable.CGridTable(filePath)
        self.grid.SetTable(self.table,True)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.OnGridDataChanged,self.grid)
        
        self.data = self.table.gridTableDict
        #saveButton
        self.saveButton = buttons.GenButton(self.panel,-1,"Save File")
        self.saveButton.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.saveButton.SetBezelWidth(2)
        self.saveButton.SetBackgroundColour("blue")
        self.saveButton.SetForegroundColour("white")
        self.saveButton.SetToolTipString("Save Test Case")
        self.Bind(wx.EVT_BUTTON,self.OnClickSaveCase,self.saveButton)
        #网格表布局
        gridBox = wx.BoxSizer(wx.VERTICAL)
        gridBox.Add(self.grid,1,wx.EXPAND)
        tempSizer = wx.FlexGridSizer(cols=1,hgap=2,vgap=2)
        tempSizer.Add(self.saveButton)
        gridBox.Add(tempSizer)

        #报告列表
        self.list = wx.ListCtrl(self.panel,-1,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnListRightClick,self.list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnListItemSelected,self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnListItemDeselected,self.list)
        self.LoadListData()
        self.selectedList = dict()
        #startButton
        self.startButton = buttons.GenButton(self.panel,-1,"Run Test")
        self.startButton.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.startButton.SetBezelWidth(2)
        self.startButton.SetBackgroundColour("blue")
        self.startButton.SetForegroundColour("white")
        self.startButton.SetToolTipString("Start Test")
        self.Bind(wx.EVT_BUTTON,self.OnClickStart,self.startButton)
        #报告列表布局
        listBox = wx.BoxSizer(wx.VERTICAL)
        listBox.Add(self.list,1,wx.EXPAND)
        listSizer = wx.FlexGridSizer(cols=1,hgap=2,vgap=2)
        listSizer.Add(self.startButton)
        listBox.Add(listSizer)
        
        self.responseText = wx.TextCtrl(self.panel,-1,"",style = wx.TE_MULTILINE)
        self.responseText.SetInsertionPoint(0)
        
        #saveResponse
        self.saveResponseButton = buttons.GenButton(self.panel,-1,"Save File")
        self.saveResponseButton.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.saveResponseButton.SetBezelWidth(2)
        self.saveResponseButton.SetBackgroundColour("blue")
        self.saveResponseButton.SetForegroundColour("white")
        self.saveResponseButton.SetToolTipString("Save Response")
        self.Bind(wx.EVT_BUTTON,self.OnSaveResponseFile,self.saveResponseButton)

        responseBox = wx.BoxSizer(wx.VERTICAL)
        responseBox.Add(self.responseText,1,wx.EXPAND)
        responseSizer = wx.FlexGridSizer(cols=1,hgap=2,vgap=2)
        responseSizer.Add(self.saveResponseButton)
        responseBox.Add(responseSizer)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(gridBox,3,wx.EXPAND)
        sizer.Add(listBox,2,wx.EXPAND)
        sizer.Add(responseBox,2,wx.EXPAND)
        
        self.panel.SetSizer(sizer)

    def LoadListData(self):
        url_location = self.data[(1,0)] + '://'+ self.data[(1,1)] + self.data[(1,2)]

        paramNameDict = dict()
        paramGroups = 0
        for item in self.data.items():
            if item[0][0] == 2:
                col = item[0][1]
                paramNameDict[col] = item[1]
            if item[0][0] > 2 and item[0][1] == 0:
                paramGroups += 1
        
        paramNums = len(paramNameDict)

        self.requestList = dict()
        for i in range(paramGroups):
            url_params = ''
            for j in range(paramNums):
                url_params += ( '&'+paramNameDict[j]+'='+self.data[(i+3,j)])
            self.requestList[i] = (url_location,url_params[1:])
        
        self.list.ClearAll()
        self.list.InsertColumn(0,'',wx.LIST_FORMAT_CENTER|wx.LIST_AUTOSIZE)
        self.list.InsertColumn(1,'',wx.LIST_FORMAT_CENTER|wx.LIST_AUTOSIZE)
        self.list.InsertColumn(2,'',wx.LIST_FORMAT_CENTER|wx.LIST_AUTOSIZE)
        for i in range(paramGroups):
            index = self.list.InsertStringItem(sys.maxint,'')
            self.list.SetStringItem(index,0,str(i))
            self.list.SetStringItem(index,1,self.requestList[i][0].decode('utf-8'))
            self.list.SetStringItem(index,2,self.requestList[i][1].decode('utf-8'))
        self.list.SetColumnWidth(1,wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2,wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(3,wx.LIST_AUTOSIZE)
            
        
    def OnClickStart(self,event):
        self.LoadListData()
        thread.start_new_thread(self.StartRequest,())
        
    def StartRequest(self):
        #恢复状态
        self.responseText.Clear()
        for key in self.requestList:
            self.list.SetItemBackgroundColour(key,"white")#SetBackgroundColour()不好用才这样循环做的
        #开始运行,第一行是跳过去的
        method = self.data[(1,3)].lower()
        sleepTime = self.data[(1,4)]
        for key in self.requestList:
            self.list.SetItemBackgroundColour(key,"forest green")
            try:
                if method.lower()=='post':
                    f = urllib2.urlopen(self.requestList[key][0],self.requestList[key][1])
                elif method.lower() == 'get':
                    f = urllib2.urlopen(self.requestList[key][0] + '?' + self.requestList[key][1])

                    
                jsonResponse = json.loads(f.read().decode('utf-8','ignore'))
                newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                tempStr = u"测试用例"+str(key)+u":"+self.requestList[key][1].decode('utf-8')+'\n'
                self.responseText.AppendText(tempStr)
                self.responseText.AppendText(newjson)
                self.responseText.AppendText('\n\n')
                f.close()
            except (IOError, httplib.HTTPException):
                continue
            except ValueError:
                tempStr = u"测试用例"+str(key)+u":"+self.requestList[key][1].decode('utf-8')+'\n'
                self.responseText.AppendText(tempStr)
                self.responseText.AppendText(f.read().decode('utf-8','ignore'))
                self.responseText.AppendText('\n\n')
                
            time.sleep(float(sleepTime)/1000.0)

    def OnSaveResponseFile(self,event):
        dlg = wx.FileDialog(self,"Open Test Case...",os.getcwd(),"log.txt",style=wx.SAVE,
                            wildcard="txt(*.txt)|*.txt")
        if dlg.ShowModal()==wx.ID_OK:
            fileHandle = open(dlg.GetPath(),'w')
            fileHandle.write(self.responseText.GetValue().encode('gbk'))
            fileHandle.close()

        dlg.Destroy()

    def OnListItemSelected(self,event):
        self.curIndex = event.GetIndex()
        self.selectedList[self.curIndex] = self.requestList[self.curIndex]
        
    def OnListItemDeselected(self,event):
        self.curIndex = event.GetIndex()
        self.selectedList.pop(self.curIndex)
        
    def OnListRightClick(self,event):
        self.popupmenu = wx.Menu()
        for text in "Run".split():
            item = self.popupmenu.Append(-1,text)
            self.Bind(wx.EVT_MENU,self.OnPopupItemSelected,item)
        pos = self.CaptureMouse()
        self.panel.PopupMenu(self.popupmenu,pos)
        
    def OnPopupItemSelected(self,event):
        item = self.popupmenu.FindItemById(event.GetId())
        if item.GetText()=='Run':
            for key in self.requestList:
                self.list.SetItemBackgroundColour(key,"white")#SetBackgroundColour()不好用才这样循环做的

            method = self.data[(1,3)].lower()
            sleepTime = self.data[(1,4)]
            for key in self.selectedList:
                self.list.SetItemBackgroundColour(key,"gold")
                try:
                    if method.lower()=='post':
                        f = urllib2.urlopen(self.selectedList[key][0],self.selectedList[key][1])
                    elif method.lower() == 'get':
                        f = urllib2.urlopen(self.selectedList[key][0] + '?' + self.selectedList[key][1])
                        
                    jsonResponse =json.loads(f.read().decode('utf-8','ignore'))
                    newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                    tempStr = u"测试用例"+str(key)+u":"+self.selectedList[key][1].decode('utf-8')+'\n'
                    self.responseText.AppendText(tempStr)
                    self.responseText.AppendText(newjson)
                    self.responseText.AppendText('\n\n')
                    f.close()
                except (IOError, httplib.HTTPException):
                    continue
                except ValueError:
                    tempStr = u"测试用例"+str(key)+u":"+self.selectedList[key][1].decode('utf-8')+'\n'
                    self.responseText.AppendText(tempStr)
                    self.responseText.AppendText(f.read().decode('utf-8','ignore'))
                    self.responseText.AppendText('\n\n')
                    
                time.sleep(float(sleepTime)/1000.0)

    def OnGridDataChanged(self,event):
        self.LoadListData()

    def OnClickSaveCase(self,event):
        pass
