import random
import socket
import struct
from IPy import IP as IPy

class IP:
    @staticmethod
    def generate_random():
        while True:
            ip = IPy(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))
            if ip.iptype() == 'PUBLIC':
                return str(ip)
