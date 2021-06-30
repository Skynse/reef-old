import argparse
from reef import scanner, arpspoof, p_sniff
from rich import print


def main():
    parser = argparse.ArgumentParser(prog="reef")

    parser.add_argument("-sP", help="Scan for open ports in given ip")

    ipargs = parser.add_argument_group("Ip Scan")
    ipargs.add_argument("-sI", help="Scan IP addresses in subnet", action="store_true")

    sniffargs = parser.add_argument_group("HTTP Sniffer")
    sniffargs.add_argument("--sniff", action="store_true")
    sniffargs.add_argument("--iface", required=False, default=None)

    arpargs = parser.add_argument_group("Arpspoofer")
    arpargs.add_argument("-i", "--spoof", help="Spoofing IP")
    arpargs.add_argument("-t", "--target", help="Target IP")
    arpargs.add_argument("-g", "--gateway", help="Gateway mac address")

    args = parser.parse_args()

    if args.sP:
        print("Port Scan enabled")
        scanner.PortScanner(args.sP).run()

    if args.sI:
        print("[red]IP Scan enabled[/red]")
        scanner.IPScanner().scan()

    if args.spoof:
        arpspoof.ArpSpoofer(args.target, args.spoof, args.gateway).execute()

    if args.sniff:
        p_sniff.Sniffer(args.iface).sniff_packets()
