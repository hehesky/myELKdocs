import random
import socket
import struct
import sys
import time
from datetime import datetime
#Nginx Log Generator Script
#Using Python 2.7
#Created by 暴力膜的编译器 <zhoukh9468 at gmail dot com> 2017-07-10

#generates "proper" single-line nginx access log entry every second and append to file
methods=["GET","POST"]
stat_list=['100','200','404','418','503','504']
uri_list=['-',"http://183.129.212.250/","http://www.fakesite.com","http://www.testsubjects.io","http://localhost:5601/discover"]
agent_list=["fake agent 2017.07 limited edition","Awesome Broswer Mars Edition (R)"]
def get_randomIP(start=0xa00000,end=0xc0ffffff):
	#generate random ip address and return as string
	#default range from 10.0.0.0 to 192.255.255.255
	ip=socket.inet_ntoa(struct.pack('>I',random.randint(start,end)))
	return str(ip)
	
def get_timestamp():
	#generate a timestamp
	t=datetime.now()
	ret=t.strftime('%d/%b/%Y:%H:%M:%S')+' +0800'
	return ret

def rand_httprequest():
	ret=r'"'+random.choice(methods) +r' /fakefile.sim'+str(random.randint(0,10))+r'"'
	return ret
	
def generate_log():
	MAX_BYTE=1000
	client_ip=get_randomIP()
	timestamp=get_timestamp()
	request=rand_httprequest()
	stat=random.choice(stat_list)
	bytes=str(random.randint(1,MAX_BYTE))
	uri=random.choice(uri_list)
	agent=random.choice(agent_list)
	
	log=client_ip+" - - ["+timestamp+"] "+rand_httprequest()+' '+stat+' '+bytes+r' "'+uri+r'" "'+agent+'"\r\n'
	return log
	
if __name__ =="__main__":
	#print generate_log()
	if len(sys.argv)!=2:
		print "Usage: nginxLogGenerater <file_dir>"
		sys.exit()
	try:
		dir=sys.argv[1]
		fout=open(dir,'a')
		print "start writing to log\r\n"
		while True:
			fout.write(generate_log())
			time.sleep(1)
	
	except KeyboardInterrupt:
		fout.close()
		print "Stopping\n"
		sys.exit(1)
	except:
		print "Error: unable to open file at" +dir
		sys.exit()	
	