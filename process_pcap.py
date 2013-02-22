#!/bin/python

import datetime
import sys
import socket
import logthis
import load_misuse

def be_client(IPC_DOMIAN_SOCKET):
	global s
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	logthis.log("PROCESS_PCAP","CONNECTING TO PCAP SERVER")
	s.connect(IPC_DOMIAN_SOCKET)

def do_processing():
	dirty_patterns=load_misuse.LoadConfigFile()
	while 1:
		the_packet=s.recv(256)
		print the_packet
		for one in dirty_patterns:
			if one in the_packet:
				logthis.detected(one,"Possible Intrusion")
		logthis.create_pcap(the_packet)


def check_packet(data):
	dirty_patterns=load_misuse.LoadConfigFile(CON_FILE)
	for one in dirty_patterns:
		if one in data:
			logthis.detected(one,"Possible Intrusion")
	logthis.create_pcap(the_packet)