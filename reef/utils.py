import scapy.all as scapy


def get_gateway() -> str:
    """Read the default gateway directly from /proc."""
    return scapy.get_if_addr(scapy.conf.iface)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False)[0]
    return answered_list[0][1].hwsrc
