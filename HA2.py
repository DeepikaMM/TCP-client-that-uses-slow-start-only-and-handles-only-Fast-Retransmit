from socket import *
import struct
import sys
import time


#Default values
Server_IP = 'localhost'
Server_PORT = 8888
Timeout = 0.1
Total_no_of_packets = 20
cwnd=1
#arg = str(sys.argv[i])  #aruments from command line
#print arg
Server_Addr=((Server_IP,Server_PORT))
bytes = 1024
time_out=time.time() + Timeout
sent=0
tot=0


#creating socket client_sock
try:
	client_sock =socket(AF_INET,SOCK_STREAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()
print 'Socket Created'


#connectinng with the server
try:
	client_sock.connect(Server_Addr)
except socket.gaierror:
	print 'Error occured while connecting.....'
print 'connected to %s port %s' % Server_Addr

#send data to server
message="Sample message"
try:
	print "hi"
	#while True:
	while tot<Total_no_of_packets:
		if ((time.time() > time_out)and(sent<cwnd)):
			print 'Timeout occured'
			cwnd=cwnd/2
			sent=0
			#break
		else:
			if(sent<cwnd):
				client_sock.send(message)
				print message
				print 'Message sent successfully'
				print sent
				sent=sent+1
				tot=tot+1
			else:
				cwnd=cwnd*2
				sent =0


finally:
	print 'Packets sent successfully'
	print >>sys.stderr,'closing socket'
	client_sock.close()

