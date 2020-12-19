import os
import sys
import socket
import platform
import typing as t
import threading
import re
import struct
import subprocess
from queue import Queue

HOST_IP = socket.gethostbyname(socket.gethostname())

types = {
    "pscan": lambda i: f"Scanning ports in IP: {i}",
    "presult": lambda r: "\n".join([f"[OPEN]: {i}" for i in r]),
}

def debug(_type: str, obj: t.Union[int, str]) -> str:
    """easy debugging function"""
    print(types[_type](obj))


def validate(target: str) -> None:
    """validate the ip address before use"""
    if bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", target)):
        pass
    else:
        sys.exit("Aborted: Invalid IPV4 address")


def getplatform() -> str:
    """For platform specific functions"""
    return platform.system()


def get_default_gateway_linux() -> str:
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != "00000000" or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
                    
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


class IPScanner:
    """
    Base class for IP scanner

    """

    def __init__(self):
        self.q = Queue()

    def scan(self, end: int) -> None:
        if platform.system() == "Windows":
            com = "ping -n 1 "
        else:
            com = "ping -c 1 "
        try:
            addr = ".".join(get_default_gateway_linux().split(".")[:3]) + "." + str(end)
            process = com + addr
            resp = subprocess.call(process.split(), stderr=subprocess.DEVNULL, stdout=open(os.devnull, "w"))
            if not resp:
                print(f"FOUND {addr}@{socket.gethostbyaddr(addr)[0]}")

        except KeyboardInterrupt:
            sys.exit("Aborted")
        except:
            pass

    def threader(self) -> None:
        while True:
            worker = self.q.get()
            self.scan(worker)
            self.q.task_done()

    def run(self) -> None:
        for _ in range(100):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for worker in range(0, 256):
            self.q.put(worker)

        self.q.join()


class PortScanner:
    def __init__(self, target: t.AnyStr) -> None:
        self.target = target
        self.q = Queue()

    def scan(self, port) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r = sock.connect_ex((self.target, port))

        if r == 0:
            print("[OPEN]:",port)
            sock.close()

    def threader(self) -> None:
        while True:
            worker = self.q.get()
            self.scan(worker)
            self.q.task_done()

    def run(self) -> None:
        validate(self.target)
        debug("pscan", self.target)
        for _ in range(100):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        try:
            for worker in range(0, 65535):
                self.q.put(worker)
            self.q.join()
        except KeyboardInterrupt:
            sys.exit("Aborted!")
        except:
            pass
