from twisted.internet import protocol, reactor
from smspdu import *
import binascii

class SMsock(protocol.Protocol):

  def __init__(self):
    self.pdu = ""

  def dataReceived(self, data):
    data_hex = binascii.b2a_hex(data)
    print 'Data received:',data_hex
    data_received = data_hex.strip()
    print 'Data received:',data_received
    try:
      p = SMS_SUBMIT.fromPDU(data_received,'unknown')
      print p.toPDU(1)
      print p.dump()
      print p.user_data
      rpdu = "07911326040000F0040B911346610089F60000208062917314080CC8F71D14969741F977FD07"
      rpdu_bin = binascii.a2b_hex(rpdu)
      self.transport.write(rpdu_bin)
    except:
      print 'error'

class SMsockFactory(protocol.ClientFactory):
  def buildProtocol(self, addr):
    print 'Connected.'
    return SMsock()
    
  def startedConnecting(self, connector):
    print 'Started to connect'

  def clientConnectionFailed(self,connector,reason):
    print 'Lost connection. reason: ', reason

  def clientConnectionFailed(self,connector,reason):
    print 'Connection failed. reason: ', reason


reactor.connectUNIX("/tmp/bsc_sms", SMsockFactory())
reactor.run()
