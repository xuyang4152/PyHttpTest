#coding=utf-8

'''
Created on 2013年9月16日

@author: hongkangzy
'''
import csv
import copy


class TestFile:
    def __init__(self):
        self.dataList = []
        self.sort = {}
        
    def readFile(self,fileName):
        if fileName == None:
            return False

        requiredParams = {0:'test_index',1:'test_url',2:'test_params',3:'test_protocal',4:'test_host',5:'test_path',6:'test_method',7:"test_sleepTime"}
        
        #默认utf-8编码格式的文件
        reader = csv.DictReader(open(fileName))
        
        #读入第一行
        self.dataList.append(reader.next())
        #增加index 以及 test_url键
        self.dataList[0]['test_index'] = '固定参数'
        self.dataList[0]['test_url'] = ''
        self.dataList[0]['test_params']=''

        #列排序
        self.sort = copy.copy(requiredParams)
        
        index = len(self.sort)
        for key in self.dataList[0]:
            if key not in requiredParams.values():
                self.sort[index] = key
                index += 1
                
        #请求url
        url_location = self.dataList[0]['test_protocal'] + '://'+ self.dataList[0]['test_host'] + self.dataList[0]['test_path']
        
        index = 1
        #从第二行开始遍历
        for item in reader:
            self.dataList.append(item)
            
            url_params =''
            url = ''
                
            for key in item.keys():
                if key not in requiredParams.values() and item[key]!='':
                    url_params += ( '&'+key+'='+item[key] )

            if self.dataList[0]['test_method'].lower() == 'post':
                self.dataList[index]['test_url'] = url_location
                self.dataList[index]['test_params'] = url_params[1:]
                self.dataList[index]['test_index'] = index-1
            elif self.dataList[0]['test_method'].lower() == 'get':
                if url_params != '':
                    self.dataList[index]['test_url'] = ( url_location + '?' + url_params[1:] )
                else:
                    self.dataList[index]['test_url'] = url_location
                self.dataList[index]['test_params'] = ''
                self.dataList[index]['test_index'] = index-1
                
            index += 1

        return True
        



    










        
