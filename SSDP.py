import socket
import sys
from httplib import HTTPResponse
from StringIO import StringIO

# SSDP discovery
# based on https://gist.github.com/2428250 by schlamar (https://github.com/schlamar)

MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1900

DISCOVERY_MSG = "M-SEARCH * HTTP/1.1\r\n" + \
                "HOST: 239.255.255.250:1900\r\n" + \
                "MAN: ssdp:discover\r\n" + \
                "MX: 10\r\n" + \
                "ST: ssdp:all\r\n\r\n"

class Response(HTTPResponse):
    def __init__(self, response_text):
        self.fp = StringIO(response_text)
        self.debuglevel = 0
        self.strict = 0
        self.msg = None
        self._method = None
        self.begin()

def discover(timeout=1, retries=5):
    socket.setdefaulttimeout(timeout)
    
    response_list = {}
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.bind(("", 0))

    for _ in xrange(2):
        # sending it more than once will
        # decrease the probability of a timeout
        sock.sendto(DISCOVERY_MSG, (MCAST_GRP, MCAST_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            r = Response(data)
            if not addr in response_list.keys():
                response_list[addr] = r
    except socket.timeout:
        pass       
        
    return response_list


if __name__ == '__main__':
    resp = discover()
    for r in resp:
        print resp[r].getheader('')