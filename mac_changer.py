#! /usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info')
    elif not options.mac_address:
        parser.error('[-] Please specify a new MAC address, use --help for more info')
    return options


def change_mac(interface, mac_address):
    print("[+] Changing MAC address for " + interface + " to " + mac_address)
    subprocess.call(["ip", "l", "set", interface, "down"])
    subprocess.call(["ip", "l", "set", interface, "a", mac_address])
    subprocess.call(["ip", "l", "set", interface, "up"])


def get_current_mac(interface):
    ip_show_result = subprocess.check_output(["ip", "l", "show", interface])
    ip_show_result = ip_show_result.decode('utf-8')

    mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)+? (?=brd)", ip_show_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("\nCurrent MAC = " + str(current_mac))

change_mac(options.interface, options.mac_address)
current_mac = get_current_mac(options.interface)
if current_mac == options.mac_address:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] Current MAC = " + str(current_mac))
