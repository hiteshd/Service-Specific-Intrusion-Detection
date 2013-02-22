#!/usr/bin/python

import dpkt
import datetime
import pcapy
import sys
import socket
import logthis
from dpkt.ip import IP, IP_PROTO_UDP
from dpkt.udp import UDP

INTERFACE_TO_MONITOR=None

def make_server(IPC_DOMAIN_SOCKET):
  global ss 
  ss = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  ss.bind(IPC_DOMAIN_SOCKET)
  
  ss.listen(1)

def do_capture(INTERFACE_TO_MONITOR):
  '''
   Arguments here are:
     open_live(INTERFACE_TO_MONITOR,(maximum number of bytes to capture _per_packet_),promiscious mode (1 for true),
        timeout (in milliseconds)
  '''
  cap = pcapy.open_live(INTERFACE_TO_MONITOR, 65536, 1, 0)
  logthis.log("PACKET-CAP","Starting to Capture")
  logthis.log("PACKET-CAP","Waiting for PCAP-PROCESSING MODULE")
  
  c, addr = ss.accept()
  
  logthis.log("PACKET-CAP","CONNECTION ACCEPTED - LOCAL SOCKET ESTABLISHED")


  # Read packets -- header contains information about the data from pcap,
  # payload is the actual packet as a string
  while 1:
    (header,payload)=cap.next()
    the_packet= (header,payload)
  
    eth = dpkt.ethernet.Ethernet(payload)
  
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
          continue
    ip = eth.data
    if ip.p!=dpkt.ip.IP_PROTO_TCP: #Check for TCP packets
          continue
    tcp = ip.data
  
    c.send((str(tcp.data).encode("hex")))

    if tcp.dport == 80 and len(tcp.data) > 0:
        http = dpkt.http.Request(tcp.data)
        c.send(str(http))
  
def main(argv):
  if len(sys.argv)<2:
    print "Usage: ./packet-cap <INTERFACE_TO_MONITOR>"
    sys.exit(1)

  INTERFACE_TO_MONITOR=argv[1]  
  print 'Opening %s' % INTERFACE_TO_MONITOR

if __name__ == "__main__":
  main(sys.argv)