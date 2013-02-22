#!/usr/bin/python

import logthis
import packet_cap
import process_pcap
import thread
import threading
import sys, os
import datetime
import random

USAGE="""
Oops! You got it wrong. Read below
Usage: python ids.py <INTERFACE_TO_MONITOR>
Try again now
"""

IPC_DOMAIN_SOCKET="/tmp/ids_domain_socket"

def main():

	#RANDOM_PORT=random.randint(1024,65534)
	try:
		if os.path.exists(IPC_DOMAIN_SOCKET): # Deleting the previous instance - equivalent to flush for domain sockets
			os.unlink(IPC_DOMAIN_SOCKET)
			
		logthis.begin_log()

		print "Welcome to the customizable IDS.\nUsing %s for Inter-thread Communication " % IPC_DOMAIN_SOCKET
		
		INTERFACE_TO_MONITOR=sys.argv[1]  # Initialize the interface 
		#CONFIG=sys.argv[2] TODO
		print 'Opening %s' % INTERFACE_TO_MONITOR

		print "\nRunning\nPress Ctrl+c to exit\n"

		#print "Break point 1"
		'''Setting up the local server'''
		server_thread=threading.Thread(target=packet_cap.make_server,args=(IPC_DOMAIN_SOCKET,))
		server_thread.daemon=True # Make it run in the background
		server_thread.start()

		#print "Break point 2"
		'''Setting up the local client'''
		client_thread=threading.Thread(target=process_pcap.be_client,args=(IPC_DOMAIN_SOCKET,))
		client_thread.daemon=True
		client_thread.start()
		print dir(client_thread)

		#print "Break point 3"
		'''Setting up the packet capture deamon'''
		pcap_thread=threading.Thread(target=packet_cap.do_capture,args=(INTERFACE_TO_MONITOR,))	
		pcap_thread.daemon=True
		pcap_thread.start()

		#print "Break point 4"
		'''Setting up the procesing deamon'''
		process_thread=threading.Thread(target=process_pcap.do_processing())
		process_thread.daemon=True
		process_thread.start()

	except KeyboardInterrupt:
		print "\nPerforming Cleanup"
		os.unlink(IPC_DOMAIN_SOCKET)
		sys.exit(1)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		sys.exit(1)


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print USAGE
		sys.exit(1)
	main()