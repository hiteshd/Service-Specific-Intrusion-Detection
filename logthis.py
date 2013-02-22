#!/bin/python

import datetime

def detected(pattern,msg):
	foo=open("DETECTIONS.LOG","a")
	logthis=str(datetime.datetime.today())+" | "+str(pattern)+" | "+str(msg)+"\n"
	foo.write(logthis)
	foo.close()

def log(coming_from,msg):
	foo=open("LOG_IDS_TOTAL.LOG","a")
	logthis=str(datetime.datetime.today())+" | "+str(coming_from)+" | "+str(msg)+"\n"
	foo.write(logthis)
	foo.close()

def begin_log():
	foo=open("LOG_IDS_TOTAL.LOG","a")
	logthis="-----------------------------------------------\nSTARTING CAPTURE ON "+str(datetime.datetime.today())+"\n-----------------------------------------------\n"
	foo.write(logthis)
	foo.close()

def create_pcap(addthis):
	foo=open("PCAP.LOG","a")
	logthis=str(datetime.datetime.today())+" | "+str(addthis)+"\n"
	foo.write(logthis)	
	foo.close()
