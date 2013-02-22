#!/bin/python

import logthis

def LoadConfigFile():
	patterns=[]
	con_handle=open('rules.conf','r')
	one_line=con_handle.readline()
	while one_line:
		if one_line.split(';')[-2].strip()=="string":
			patterns.append(str(one_line.split(';')[-1].encode('hex')))
		elif one_line.split(';')[-2].strip()=="hex":
			patterns.append(str(one_line.split(';')[-1].strip()))
		else:
			logthis.log("LOAD MISUSE","Config "+str(one_line)+" not loaded")
		one_line=con_handle.readline()
	return patterns
	con_handle.close()

if __name__=="__main__":
	main()