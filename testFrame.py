#coding=utf-8
'''
Created on 2013年9月18日

@author: hongkangzy
'''
import wx
import wx.lib.buttons as buttons
import testFile
import sys
import urllib2
import httplib
import time
import thread
import json
import os
import copy

class TestFrame(wx.Frame):
    def __init__(self,parent,file):
        
        self.selectedItems = []
        self.sort = {}
        self.dataList = []
        
        #读取测试用例文件
        curTestFile = testFile.TestFile()
        if curTestFile.readFile(file)==False:
            return
        self.dataList = curTestFile.dataList
        self.sort = curTestFile.sort

        
        wx.Frame.__init__(self,parent,-1,'Test Run',name='TestFrame')
        self.SetBackgroundColour(wx.Color(204,232,207))
        self.Maximize()

        self.panel = wx.Panel(self,-1)
        
        ####################################################################################################
        #ListCtrl
        self.list = wx.ListCtrl(self.panel,-1,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.LoadListData()
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnListRightClick,self.list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnListItemSelected,self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnListItemDeselected,self.list)
        #self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,self.OnBeginLabelEdit,self.list)
        #self.Bind(wx.EVT_LIST_END_LABEL_EDIT,self.OnEndLabelEdit,self.list)
        #saveButton
        self.saveButton = buttons.GenButton(self.panel,-1,"Save")
        self.saveButton.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.saveButton.SetBezelWidth(2)
        self.saveButton.SetBackgroundColour("blue")
        self.saveButton.SetForegroundColour("white")
        self.saveButton.SetToolTipString("Save Test Case")
        #self.Bind(wx.EVT_BUTTON,self.OnClick,self.saveButton)
        
        #startButton
        self.startButton = buttons.GenButton(self.panel,-1,"Start")
        self.startButton.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD,False))
        self.startButton.SetBezelWidth(2)
        self.startButton.SetBackgroundColour("blue")
        self.startButton.SetForegroundColour("white")
        self.startButton.SetToolTipString("Start Test")
        self.Bind(wx.EVT_BUTTON,self.OnClickStart,self.startButton)
        
        listBox = wx.BoxSizer(wx.VERTICAL)
        listBox.Add(self.list,1,wx.EXPAND)
        tempSizer = wx.FlexGridSizer(cols=2,hgap=2,vgap=2)
        tempSizer.Add(self.saveButton)
        tempSizer.Add(self.startButton)
        listBox.Add(tempSizer)

        ######################################################################################################
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
        responseBox.Add(self.saveResponseButton)
        
        sizer = wx.FlexGridSizer(cols=2,hgap=2,vgap=2)
        sizer.Add(listBox,1,wx.EXPAND)
        sizer.Add(responseBox,1,wx.EXPAND)
        sizer.AddGrowableCol(0,1)
        sizer.AddGrowableCol(1,1)
        sizer.AddGrowableRow(0,1)
        self.panel.SetSizer(sizer)

        #状态栏
        starusBar = self.CreateStatusBar()

    def LoadListData(self):
        self.list.ClearAll() 
        for key in self.sort:
            self.list.InsertColumn(key,self.sort[key],wx.LIST_FORMAT_CENTER|wx.LIST_AUTOSIZE)

        for i in range(len(self.dataList)):
            index = self.list.InsertStringItem(sys.maxint,'')
            for key in self.sort:
                data = self.dataList[i][self.sort[key]]
                self.list.SetStringItem(index,key,str(data).decode('utf-8'))
                
        self.list.SetColumnWidth(1,wx.LIST_AUTOSIZE)
        self.list.SetItemBackgroundColour(0,"coral")#SetBackgroundColour()不好用才这样循环做的
        
    def StartRequest(self):
        #恢复状态
        self.responseText.Clear()
        for i in range(1,len(self.dataList)):
            self.list.SetItemBackgroundColour(i,"white")#SetBackgroundColour()不好用才这样循环做的
        #开始运行,第一行是跳过去的
        for i in range(1,len(self.dataList)):
            self.list.SetItemBackgroundColour(i,"forest green")

            try:
                if self.dataList[0]['test_method'].lower()=='post' and self.dataList[i]['test_url']!='':
                    f = urllib2.urlopen(self.dataList[i]['test_url'],self.dataList[i]['test_params'])
                    jsonResponse = json.loads(f.read().decode('utf-8','ignore'))
                    newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                    tempStr = u"第"+str(i-1)+u"个测试用例:"+self.dataList[i]['test_url'].decode('utf-8')+'\n'
                    self.responseText.AppendText(tempStr)
                    self.responseText.AppendText(newjson)
                    self.responseText.AppendText('\n\n')
                    f.close()
                elif self.dataList[0]['test_method'].lower()=='get'and self.dataList[i]['test_url']!='':
                    f = urllib2.urlopen(self.dataList[i]['test_url'])
                    jsonResponse = json.loads(f.read().decode('utf-8','ignore'))
                    newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                    tempStr = u"第"+str(i-1)+u"个测试用例:"+self.dataList[i]['test_url'].decode('utf-8')+'\n'
                    self.responseText.AppendText(tempStr)
                    self.responseText.AppendText(newjson)
                    self.responseText.AppendText('\n\n')
                    f.close()
               
            except (IOError, httplib.HTTPException):
                continue
            
            #延时
            time.sleep(float(self.dataList[0]['test_sleepTime'])/1000.0)

    def OnClickStart(self,event):
        thread.start_new_thread(self.StartRequest,())

        
    def OnSaveResponseFile(self,event):
        dlg = wx.FileDialog(self,"Open Test Case...",os.getcwd(),"log.txt",style=wx.SAVE,
                            wildcard="txt(*.txt)|*.txt")
        if dlg.ShowModal()==wx.ID_OK:
            fileHandle = open(dlg.GetPath(),'w')
            fileHandle.write(self.responseText.GetValue().encode('gbk'))
            fileHandle.close()

        dlg.Destroy()

    def OnListItemSelected(self,event):
        #确保第一行无法被选进
        self.curIndex = event.GetIndex()
        if self.curIndex == 0:
            return
        #加入选择列表
        self.selectedItems.append(self.dataList[self.curIndex])
        
    def OnListItemDeselected(self,event):
        #确保第一行无法被选进
        self.curIndex = event.GetIndex()
        if self.curIndex == 0:
            return
        #从选择列表中删除
        self.selectedItems.remove(self.dataList[self.curIndex])
            
    def OnListRightClick(self,event):
        self.popupmenu = wx.Menu()
        for text in "Run Delete".split():
            item = self.popupmenu.Append(-1,text)
            self.Bind(wx.EVT_MENU,self.OnPopupItemSelected,item)
        pos = event.GetPoint()
        self.panel.PopupMenu(self.popupmenu,pos)
        
    def OnPopupItemSelected(self,event):
        item = self.popupmenu.FindItemById(event.GetId())
        if item.GetText()=='Run':
            for item  in self.dataList[1:]:
                self.list.SetItemBackgroundColour(item['test_index']+1,"white")#SetBackgroundColour()不好用才这样循环做的
            #开始运行,第一行是跳过去的
            for item in self.selectedItems:
                self.list.SetItemBackgroundColour(item['test_index']+1,"gold")
                
                try:
                    if self.dataList[0]['test_method'].lower()=='post' and item['test_url']!='':
                        f = urllib2.urlopen(item['test_url'],item['test_params'])
                        jsonResponse = json.loads(f.read().decode('utf-8','ignore'))
                        newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                        tempStr = u"第"+str(item['test_index'])+u"个测试用例:"+item['test_url'].decode('utf-8')+'\n'
                        self.responseText.AppendText(tempStr)
                        self.responseText.AppendText(newjson)
                        self.responseText.AppendText('\n\n')
                        f.close()
                    elif self.dataList[0]['test_method'].lower()=='get' and item['test_url']!='':
                        f = urllib2.urlopen(item['test_url'])
                        jsonResponse = json.loads(f.read().decode('utf-8','ignore'))
                        newjson = json.dumps(jsonResponse, ensure_ascii=False)
                    
                        tempStr = u"第"+str(item['test_index'])+u"个测试用例:"+item['test_url'].decode('utf-8')+'\n'
                        self.responseText.AppendText(tempStr)
                        self.responseText.AppendText(newjson)
                        self.responseText.AppendText('\n\n')
                        f.close()
               
                except (IOError, httplib.HTTPException):
                    continue
            
                #延时
                time.sleep(float(self.dataList[0]['test_sleepTime'])/1000.0)

        elif item.GetText()=='Delete':
            #根据已选择项删除列表
            for item in self.selectedItems:
                self.dataList.remove(item)
            #清除已选择项
            del self.selectedItems[:]
            #重新排列测试用例ID
            index = 0 
            for item in self.dataList[1:]:
                item['test_index'] = index
                index+=1
            
            self.LoadListData()

        elif item.GetText() =='Insert':
            newData = copy.copy(self.dataList[self.curIndex])
            for key in newData.keys():
                newData[key] = ''
            self.dataList.insert(self.curIndex+1,newData)
            #清除已选择项
            del self.selectedItems[:]
            #重新排列测试用例ID
            index = 0 
            for item in self.dataList[1:]:
                item['test_index'] = index
                index+=1
            self.LoadListData()







        
       
