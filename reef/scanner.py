import sys
import socket
import platform
import typing as t
import threading
import re
import scapy.all as scapy
from queue import Queue
from reef.table import make_table
from reef.utils import get_mac, get_gateway

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


def get_platform() -> str:
    """For platform specific functions"""
    return platform.system()


class IPScanner:
    """
    Base class for IP scanner

    """

    def __init__(self):
        self.q = Queue()

    def scan(self) -> None:
        ip_list = []
        ip = get_gateway() + "/24"
        arp_req_frame = scapy.ARP(pdst=ip)
        broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = scapy.srp(
            broadcast_ether_arp_req_frame, timeout=1, verbose=False
        )[0]
        result = []
        for i in range(0, len(answered_list)):
            client_dict = {
                "ip": answered_list[i][1].psrc,
                "mac": answered_list[i][1].hwsrc,
            }
            result.append(client_dict)

        for i in result:
            try:
                hostname = socket.gethostbyaddr(i.get("ip"))[0]
            except:
                hostname = "None"
            ip_list.append([i.get("ip") + " ", hostname, i.get("mac")])
        print(
            make_table(
                rows=ip_list,
                labels=["ip", "hostname", "mac"],
                centered=True,
            )
        )


class PortScanner:
    def __init__(self, target: t.AnyStr) -> None:
        self.target = target
        self.q = Queue()

    def scan(self, port) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r = sock.connect_ex((self.target, port))

        if r == 0:
            print("[OPEN]:", port)
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
