import argparse
from reef import scanner
from reef import arpspoof


def main():
    parser = argparse.ArgumentParser(prog="reef")

    parser.add_argument("-sP", help="Scan for open ports in given ip")

    ipargs = parser.add_argument_group("Ip Scan")
    ipargs.add_argument("-sI", help="Scan IP addresses in subnet", action="store_true")

    arpargs = parser.add_argument_group("Arpspoofer")
    arpargs.add_argument("-i", "--spoof", help="Spoofing IP")
    arpargs.add_argument("-t", "--target", help="Target IP")
    arpargs.add_argument("-g", "--gateway", help="Router")

    args = parser.parse_args()

    if args.sP:
        print("Port Scan enabled")
        scanner.PortScanner(args.sP).run()

    if args.sI:
        print("IP Scan enabled")
        scanner.IPScanner().scan()

    if args.spoof:
        arpspoof.ArpSpoofer(args.target, args.spoof, args.gateway).execute()
