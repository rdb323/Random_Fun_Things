from struct import pack

'''
  Ryan Barth
  CPSC 5510
  Project 2: RDT 3.0
  May 12, 2022


  This file is a collection of common utility functions for the 2nd project
  including creating packets, checksum creation and validation, and checking
  the sequence number of a packet
'''



def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except 
      for checksum field)

    Returns:
      the checksum in bytes

    """

    runningSum = getSum(packet_wo_checksum)

    comp = complement(runningSum)
    return comp.to_bytes(2, 'big')


def check_seq_num(packet):
  '''
    takes in a packet and returns which sequence number it has 1 or 0 in int form

    args:
      packet, the packet of data that is being looked through

    returns:
      an int representation of 1 or 0
  '''
  length = format(packet[11], "08b")
  return int(length[7])


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """

    givenChecksum = packet[8:10]

    rest_of_packet = packet[:8]
    rest_of_packet += packet[10:]

   
    runningSum = getSum(rest_of_packet)

    derivedChecksum = complement(runningSum)
    derivedChecksum = derivedChecksum.to_bytes(2,'big')

    return True if givenChecksum == derivedChecksum else False


    

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """

    data_str_encoded = data_str.encode()
    lengthBytes = lengthMaker(data_str_encoded, ack_num, seq_num)
    classStr = "COMPNETW".encode()

    byteArrays = classStr + lengthBytes + data_str_encoded
    checksum = create_checksum(byteArrays)

    return classStr + checksum + lengthBytes + data_str_encoded

    # make sure your packet follows the required format!




def lengthMaker(encoded_data, ack, seq):
  '''
    Creates the length bytes of the packet by taking in the length of the data in
    bytes, adding in 12 for the entire header and then adding at most 3 for the 
    ack and seq # bits that are appended to the 14 length bits

    Args:
    encoded_data: The data payload for the packet encoded into bytes
    ack: int of 0 or 1 to show that this packet is meant to be an ACK message
    seq: int of 0 or 1 for the seq # of the packet

    Returns: a byte array of size 2 for the entirety of the length and ack + seq 
    byte sequence, with the most sig byte on the right
  '''

  size = len(encoded_data) + 12
  size = format(size, "014b")
  size += format(ack*2 + seq, "02b")
  size = int(size, 2)
  return size.to_bytes(2, 'big')




def sumBin(a, b):
  '''
      Takes in 2 binary numbers with size of 16 each, and adds them. Any
      overflow past the 16 bits will wrap around. The final 16 bit number will
      be returned

      Args:
      a: the first 16 bit binary number (must be a string of only 1s and 0s)
      b: the second 16 bit binary number (must be a string of only 1s and 0s)

      Returns: a 16 bit binary number represented as a string
      (wraparound handled)
  '''

  binSum = bin(int(a,2) + int(b,2))
  binSum = binSum[2:] # get rid of the leading "0b" from the string

  #String size is greater than 16 bits, have to wrap around to 16 bits again
  if len(binSum) > 16:
      #Need to do a wraparound
      wraparound = 1
      binStr = binSum[1:]
      wrapStr = ""
      count = 0

      while count < 16 and wraparound == 1:
          if binStr[15 - count] == "1":
              wrapStr = "0" + wrapStr
          else:
              wrapStr = "1" + wrapStr
              wraparound = 0
          count += 1
      
      if count < 16:
          wrapStr = binStr[:(16 - count)] + wrapStr
      return wrapStr

  #If the size of the string is less than 17 bits, just return the string itself
  return binSum




def complement(sum):
  '''
    Takes in a 16 bit binary number in the form of a string and gives the complement
    of it

    Args:
      sum: 16 bit binary in string form

    Returns:
      An integer representation of the binary complement to sum
  '''
  if len(sum) < 16:
    num = int(sum, 2)
    sum = format(num, "016b")
  
  comp = ""

  for ind in range(len(sum)):
    if sum[ind] == "1":
      comp += "0"
    else:
      comp += "1"

  return int(comp, 2)



def getSum(byteArr):
  '''
    Small method to get the running sum for an array of byte data

    Arg:
      byteArr: an array of byte data

    returns:
      A string representation of a 16 bit binary integer
  '''

  a = format(byteArr[0], "016b")
  b = format(byteArr[1], "016b")

  runningSum = sumBin(a, b)

  for ind in range(2, len(byteArr)):
    nextByte = format(byteArr[ind], "016b")
    runningSum = sumBin(runningSum, nextByte)

  return runningSum
###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should not make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
