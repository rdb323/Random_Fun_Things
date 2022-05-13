from socket import *
from util import *

myPort = 10101 + (2186951 % 200)
localHost = "127.0.0.1"

class Sender:

  def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """

        self.mySock = socket(AF_INET, SOCK_STREAM)
        self.mySock.bind(("", myPort))
        self.mySock.settimeout(2)

        self.seqNum = 0
        self.packNum = 1
        self.connected = False


  def rdt_send(self, app_msg_str):
      """realiably send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """

      print("original message string: ", app_msg_str)
      packet = make_packet(app_msg_str,0, self.seqNum)
      print("packet created: ", packet)
      
      if not self.connected:
        self.mySock.connect((localHost, myPort+1))
        self.connected = True

      self.mySock.send(packet)
      print("packet num.", self.packNum, " is successfully sent to the receiver.") 
      self.packNum += 1
      self.getResponse(packet, app_msg_str)
      self.seqNum = 1 if self.seqNum == 0 else 0
      

     



  def resendPacket(self, packet, timeout_bool, payload):
    '''
    Method called to resend a packet, either because of timeout or spoofed bit corruption
    Increases packet number by 1

    args:
      packet: the entire packet to be resent to the receiver
      timeout_bool: boolean to tell if this is supposed to be a "timeout"
        resend (True means it is)
      payload: The non-encoded data payload in string form that will be sent to the receiver
    '''

    if timeout_bool:
      print("socket timeout! Resend!\r\n\r\n")
      print("[timeout retransmission]: ", payload)
    else:
      print("receiver acked the previous pkt, resend!\r\n\r\n")
      print("[ACK-Previous retransmission]: ", payload)
    
    self.mySock.send(packet)
    print("packet num.", self.packNum, " is successfully sent to the receiver.")
    self.packNum += 1
    self.getResponse(packet, payload)



  def getResponse(self, packet, payload):
    '''
      Tries to receive a response for the sent packet from the receiver. If 2
      or more seconds pass, then a timeout for the message happens. Either timeout
      or bit corruption will cause a call for resending the packet

      args:
        packet: previous packet sent to the receiver
        payload: data that was sent in the previous packet  
    '''
    try:
      response = self.mySock.recv(4096)
      ackNum = check_seq_num(response)

      if verify_checksum(response) and self.seqNum == ackNum:
        print("packet is received correctly: seq. num ", self.seqNum, \
          " = ACK num ", ackNum, ". all done!\r\n\r\n" )
      else:
        self.resendPacket(packet, False, payload)
          
    except timeout:
      self.resendPacket(packet, True, payload)
  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT Change the function name.                    #######                    
  ####### You can have other functions as needed.                             #######   