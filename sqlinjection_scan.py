#!/usr/bin/env python

# -*- coding: utf-8 -*-

import requests
import time
import json
import re
import codecs
import sys
from multiprocessing.dummy import Pool as TP
import threading
import chardet
class Injection_Scan:
    def __init__(self,url):
        print '+' + '-' * 50 + '+'
        print '\t   SQLscan by naihebian'
        print '\t\t Blog:http://www.9null.com'
        print '+' + '-' * 50 + '+'

        self.server='http://127.0.0.1:8775/'
        self.taskid=''
        self.engineid=''
        self.status=''
        self.data =''
        self.url=url
        self.start_time=time.time()

        
    def task_new(self):
        try:
            self.taskid = (requests.get('http://127.0.0.1:8775/task/new').json())['taskid']
            print '\t[*]The task is created!... taskid: ',self.taskid

        except :
            print '\t[*]ERROR!!!\tPlease run sqlmapapi.py -s !'
            exit()


    def task_delete(self):
        if requests.get(self.server + 'task/' + self.taskid + '/delete').json()['success']:
            print 'Deleted task: [%s] '% (self.taskid)


    def scan_start(self):

        if 'http' not in self.url:
            self.url='http://'+self.url
        self.url=self.url.replace('\n','')
        headers={'Content-Type':'application/json'}
        payload={'url':self.url}
        target=self.server+'scan/'+self.taskid+'/start'
        t=requests.post(target,data=json.dumps(payload),headers=headers)

        self.engineid=t.json()['engineid'] 
        if len(str(self.engineid))>0:
            print '[*]Start scanning task! [engineid:%s]' % self.engineid
        else:
            return False


    def scan_status(self):
        self.status=requests.get(self.server+'scan/'+self.taskid+'/status').json()['status']
        if self.status =='running':
            print  '\t[*]Scan! Please wait for...'
        elif self.status == 'terminated':
            print  'terminated!'
        else:
            print  'error!'


    def scan_data(self):
        self.data=requests.get(self.server+'scan/'+self.taskid+'/data').json()['data']

        if len(self.data) ==0:
            print 'not injection:\t %s' % self.url
        else:
            print 'this is a injection:\t'+self.url
            file1=open('injection.txt','a+')
            file1.write(self.url+'\n')
            file1.close()


    def scan_stop(self):
        requests.get(self.server+'scan/'+self.taskid + '/stop')


    def scan_kill(self):
        requests.get(self.server+'scan/'+self.taskid+'/kill')

    def run(self):
		

        self.task_new()
        if self.scan_start():
            print '\tError!'

        while True:
            self.scan_status()
            if self.status == 'running':
                time.sleep(10)
            elif self.status =='terminated':
                print '\t[*]The scan is complete! Available:',(time.time()-self.start_time)
                break
            else:
                break

            if time.time() - self.start_time > 360:
                error=True
                self.scan_stop()
                self.scan_kill()

        self.scan_data()

        self.task_delete()
        print '\t[*]Elapsed time:',time.time() - self.start_time
		

def getsql(url):
	Injection_Scan(url).run()

file1=codecs.open(sys.argv[1],'r').readlines()
try:
	pool=TP(int(sys.argv[2]))
	res=pool.map(getsql,file1)
	pool.close()
	pool.join()
except :
	pass


