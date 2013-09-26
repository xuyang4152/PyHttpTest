#coding=utf-8
'''
Created on 2013年9月16日

@author: hongkangzy
'''

import wx
import wx.lib.buttons as buttons

import os
from testFrame import TestFrame

from gridTestFrame import CGridTestFrame


class TopFrame(wx.Frame):
    def __init__(self):
        #顶层框架
        wx.Frame.__init__(self,None,-1,'Http Api Test',size=(1600,900),
                          style=wx.DEFAULT_FRAME_STYLE,name='TopFrame')
        self.SetBackgroundColour(wx.Color(204,232,207))
        self.Maximize(True)

        #菜单栏
        menu =wx.Menu()
        item = menu.Append(-1, u"创建测试用例")
        self.Bind(wx.EVT_MENU,self.OnNewTestCase,item)
        item = menu.Append(-1, u"打开测试用例")
        self.Bind(wx.EVT_MENU,self.OnOpenTestCase,item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_EXIT, u"关闭")
        self.Bind(wx.EVT_MENU,self.OnExit, item)
        
        mbar =wx.MenuBar()
        mbar.Append(menu, u"文件")
        self.SetMenuBar(mbar)
        
    def OnNewTestCase(self,event):
        dlg = wx.FileDialog(self,"Open Test Case...",os.getcwd(),style=wx.OPEN,
                            wildcard="csv(*.csv)|*.csv")
        if dlg.ShowModal()==wx.ID_OK:
            testCaseFrame = CGridTestFrame(self,dlg.GetPath())
            testCaseFrame.Show()
        dlg.Destroy()
        

        
    def OnOpenTestCase(self,event):
        dlg = wx.FileDialog(self,"Open Test Case...",os.getcwd(),style=wx.OPEN,
                            wildcard="csv(*.csv)|*.csv")
        if dlg.ShowModal()==wx.ID_OK:
            curTestFrame = TestFrame(self,dlg.GetPath())
            curTestFrame.Show()
        dlg.Destroy()
        
    def OnExit(self,event):
        self.Close()


class App(wx.App):
    def __init__(self,redirect=True,filename=None):
        wx.App.__init__(self,redirect,filename)
    def OnInit(self):
        self.frame = TopFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == '__main__':
    app = App(redirect=True)
    app.MainLoop()
    pass
