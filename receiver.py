from socket import *
from time import sleep
from util import *

'''
  Ryan Barth
  CPSC 5510
  Project 2: RDT 3.0
  May 12, 2022


  This file is the receiver side of the RDT 3.0 FSM. It receives a packet via
  socket transmission and then verifies the data of the packet. On a packet 
  that is divisible by 3, it requests the packet to be resent for either a
  timeout or bit corruption reason.
'''

class Receiver:
    def __init__(self, socket) -> None:
        self.s = socket
        self.seqNum = 0
        self.packNum = 1


    def get_String_Of_Data(self, packet):
        '''
            Takes in a packet and returns the data of the packet in string form

            args:
                packet: the data packet that has been received by the socket

            returns:
                A string representation of the data payload of the packet
        '''

        if len(packet) < 13:
            return None
        data = packet[12:]
        return str(data, 'UTF-8')



    def sendACK(self, num):
        '''
            Sends a packet with an ACK flag as well as a sequence number of num.
            Has a payload of ""

            args:
                num: the sequence number (1 or 0) to be attached to the packet
        '''
        packet = make_packet("resp",1,num)
        self.packNum += 1
        self.s.send(packet)




    def normalPacketACK(self, packet):
        '''
            Method called for sending a regular ACK packet back to the sender. Will
            send a packet with the expected seq # attached

            args:
                packet: the packet received by the socket, used to get the string
                payload from the data for printing to console 
        '''

        print("Packet is expected, message string delivered: ", self.get_String_Of_Data(packet))
        self.sendACK(self.seqNum)
        self.seqNum = 0 if self.seqNum == 1 else 1
        print("packet is delivered, now creating and sending the ACK packet...")



    def sameSEQ(self, packet):
        '''
            Checks if a packet has the same sequence number as the expected one
        
            args:
                packet: The packet received by the socket (has sequence num inside)

            returns:
                Boolean value of True if the sequence num is the same as the
                expected, False otherwise
        '''
        return self.seqNum == check_seq_num(packet)



    def resendPacket(self):
        '''
            Method that handles timeout production and spoofing of bit corruption
            If timing out, will sleep for 5.1 seconds, spoofing will just resend an
            ACK packet with the previous packet Seq # attached
        '''


        #sender timeout is 2 seconds so just sleep until it times out
        if self.packNum % 6 == 0:
            print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
            sleep(2.1)
            self.packNum += 1
        else:
            print("Simulating packet bit errors/corrupted: ACK the previous packet!")
            #Send a packet with the previous ack num
            self.sendACK(1 if self.seqNum == 0 else 0)


if __name__ == "__main__":
    myPort = 10101 + (2186951 % 200) + 1
    localHost = "127.0.0.1"

    
    has_rerequested = False

    metaSocket = socket(AF_INET, SOCK_STREAM)
    metaSocket.bind(("", myPort))
    metaSocket.listen(1)
    s, addr = metaSocket.accept()
    r = Receiver(s)
    while True:
        
        packet = s.recv(4096)

        #connection is closed
        if len(packet) == 0:
            s.close()
            break

        print("Packet num.", r.packNum, " received: ", packet)
        isSameCheckSum = verify_checksum(packet)

        normal_data_bool = isSameCheckSum and r.packNum % 3 != 0 and r.sameSEQ(packet)

        #checks if the packet has normal data or has already been resent
        if normal_data_bool or has_rerequested:
            has_rerequested = False
            r.normalPacketACK(packet)

        elif has_rerequested == False:
            r.resendPacket()
            has_rerequested = True
        

        print("all done for this packet!\r\n\r\n")

    
        
        
        
        
        
        
        





