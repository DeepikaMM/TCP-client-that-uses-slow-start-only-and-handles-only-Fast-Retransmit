# TCP-client-that-uses-slow-start-only-and-handles-only-Fast-Retransmit
TCP client that uses slow start only and handles only Fast Retransmit
Implement TCP client that uses slow start only and handles only Fast Retransmit. Since this client is
using Slow Start, it will start with cwnd of 1, and keep doubling with each RTT cycle. On receiving 3 duplicate
acks, it will reset the cwnd to half of its current value and continue with Slow Start. No ssthreshold is to be
maintained.¬
Use the following command line arguments for TCP client.
. -N : total number of packets to be sent (minimum of 20)
. -s: server IP address, and
. -p: server port number.
. -t : timeout value (in seconds).

The program should output on console the following:
. time (starting from 0 i.e. take current time as 0) and packet contents (Seq num, Ack value, and data) when a
packet is sent, and if it is retransmitted packet.
. time when the ack is received from receiver, along with sequence number, Ack Value and data received.
