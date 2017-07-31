from socket import *
import random,time,sys
import argparse
from array import *



#Parsing the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-N","--packets", default=20 , type=int)	#How many packets(minimum)
parser.add_argument("-t","--timeout", default=2 , type=int)	#Storing the timeout
parser.add_argument("-s","--serverip", default="127.0.0.1")	#Server IP
parser.add_argument("-p","--serverport", default=12345 , type=int)	#Port number 

args = parser.parse_args()

server_IP = args.serverip 
server_Port = args.serverport 
time_out = args.timeout 
Total_no_of_packets = args.packets 

server_Addr=((server_IP,server_Port))


#Creating socket client_sock
try:
	client_sock = socket(AF_INET,SOCK_STREAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()
print 'Socket Created'


#connectinng with the server
'''try:'''
client_sock.connect(server_Addr)
'''except socket.gaierror:
	print 'Error occured while connecting.....
print 'connected to %s port %s' % server_Addr'''

'''

#TCP HANDSHAKING STARTS HERE

SEQ = random.randrange(1,1000)
syn_packet = str(SEQ)+" S" 					# Creating the SYN packet 
time = 0 							# To handle timeout
client_sock.sendto(syn_packet, (server_IP, server_Port)) 	# Sending the SYN packet
client_sock.settimeout(time_out) 				# Setting the timeout
try:
    syn_ack_packet = client_sock.recv(2048) 		# Receiving the SYNACK packet from the server
except time_out: time=1 
if time==1: 
    print "Connection Failed"
    client_sock.close()
    sys.exit(0)         
syn_ack = syn_ack_packet.split(",") 
if syn_ack[2]=="SA": 		# If there is TCP flag named SA in the contents then the connection is established else close and exit
    print "Connection Established"
else:
    print "Connection Failed"
    client_sock.close()
    sys.exit(0)

#TCP HANDSHAKING ENDS HERE
'''



sent = 0
#To keep count of how many packets are sent within that congestion window

cwnd = 1
#Initially congestion window size is 1	

packet_sent = 0	
#To keep count of how many packets have been sent till a particular instant	


last_ACK = 1	
#Initially last ACK is 0 (i.e recently received ACK) 

buffering = []
#To keep track of what packets have been sent till now

seq_num = 1	
#Sequence number of the first packet sent

ack_num = 1	
#ACK number will initially be 1

m = 65	
#To traverse through uppercase alphabets

flag = 0
#To know if the packet being sent is a retransmitted packet

data = ""
message = ""
#Initially there is nothing in the data field of the packet



while (packet_sent<Total_no_of_packets): 
	if(sent < cwnd):
		seq_num = last_ACK
		ack_num = seq_num + 1
		
		start_time = time.time()	#Note the time at which the first packet is sent for the congestion window 
		for i in range(0,cwnd):
			for i in range(5):
				data = data + chr(m)
			message = str(seq_num)+","+str(ack_num)+","+str(data) #Creating the packet
			buffering.insert(seq_num, message) #Adding the packet to the window before it is transmitted to the server

	
			packet_sent_time = time.time()-start_time	#With respect to start time when was the first packet sent
			
			print ("SEQUENCE NUMBER : "+str(seq_num)+" ACK NUMBER : "+str(ack_num)+" DATA : "+str(data)+" and the packet is sent for first time and transmitted at time "+str(packet_sent_time))
			seq_num = seq_num +1 
			if(cwnd!=1):
				ack_num = seq_num + 1
			if(cwnd==1):
				last_ack = seq_num
			client_sock.send(message)

			sent = sent+1
			packet_sent = packet_sent+1
			message = ""
			data = ""
			m = m+1
		
		i = 0
		num_ack = 0	
		# To keep count of number of ACKs received by the client and it should be less than size of congestion window
		dup = 0
		# To keep track of duplicate ACKs

		
		while ((num_ack<cwnd) and (dup<3)):
			received= client_sock.recv(524288)	#Receiving from server
			time_ACK = time.time()
			recd_msg = received.split(",")
			recd_ACK = int(recd_msg[1])

			#CONDITION 1	(ACK received for last packet sent in the congestion window)
			if (recd_ACK == seq_num) :
				sent = 0
				num_ack = cwnd
				cwnd = cwnd*2
				last_ACK = recd_ACK
				print ("SEQUENCE NUMBER : "+recd_msg[0]+" ACK NUMBER : "+recd_msg[1]+" DATA : "+recd_msg[2]+" and the ACK is received at time "+str(time_ACK))
				break



			#CONDITION 2	(ACK received for first packet sent in the congestion window)
			elif (recd_ACK == last_ACK + 1) : 
				last_ACK = recd_ACK
				num_ack = num_ack + 1
				print ("SEQUENCE NUMBER : "+recd_msg[0]+" ACK NUMBER : "+recd_msg[1]+" DATA : "+recd_msg[2]+" and the ACK is received at time "+str(time_ACK))
				if(num_ack == cwnd):
					cwnd = cwnd*2
					sent = 0
					break



			#CONDITION 3	(When the received ACK is same as the previous ACK) To handle retransmission when 3 duplicate ACKs arrive
			elif (recd_ACK == last_ACK):
				dup = dup + 1
				print ("SEQUENCE NUMBER : "+recd_msg[0]+" ACK NUMBER : "+recd_msg[1]+" DATA : "+recd_msg[2]+" and the DUPLICATE ACK is received at time "+str(time_ACK))
				if(dup == 3):
					if(cwnd!=1):
						cwnd = cwnd/2
					sent = 0
					start_dup_time = time.time()
					for i in range(0,cwnd):
						dup_ACK = buffering[recd_ACK-1]
						dup_ACK_message = dup_ACK.split(",")
						client_sock.send(dup_ACK)
						dup_packet_sent_time = time.time()-start_dup_time
						recd_ACK = recd_ACK + 1
						sent  = sent + 1
						packet_sent = packet_sent + 1
						print ("SEQUENCE NUMBER : "+dup_ACK_message[0]+" ACK NUMBER : "+dup_ACK_message[1]+" DATA : "+dup_ACK_message[2]+" and the packet is RETRANSMITTED PACKET and transmitted at time "+str(dup_packet_sent_time))
					dup = 0
					dup_data = dup_ACK_message[2]
					n = dup_data[0]
					m = ord(n)+1
					seq_num = int(dup_ACK_message[0])+1
					ack_num = int(dup_ACK_message[1])
					start_time = start_dup_time
					num_ack = 0
					
			#CONDITION 4	
			else:	
				print ("SEQUENCE NUMBER : "+recd_msg[0]+" ACK NUMBER : "+recd_msg[1]+" DATA : "+recd_msg[2]+" and the ACK is received at time "+str(time_ACK))
				last_ACK = recd_ACK
				num_ack = seq_num-recd_ACK


print ("Total number of packets sent are "+str(packet_sent))
				
				
