#!/usr/bin/env python3

import subprocess		#Module to run system commands
import optparse			#Module to parse options from terminal
import re 				#Module for regex operations

def get_arguments():
	
	parser = optparse.OptionParser()
	
	parser.add_option("-i", "--interface", dest = "interface", help = "Interface to change its MAC address")
	parser.add_option("-m", "--mac", dest = "new_mac", help = "New MAC address")
	
	(options, arguments) = parser.parse_args() 

	if (not options.interface) & (not options.new_mac):
		parser.error("Please specify an interface and a new MAC address, use --help for more info.")

	elif not options.interface:
		parser.error("Please specify an interface, use --help for more info.")

	elif not options.new_mac:
		parser.error("Please specify a new MAC address, use --help for more info.")
	
	else:
		return options

def change_mac(interface, new_mac):
	
	print("[+] Changing MAC address for " + interface + " to " + new_mac)
	
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):

	ifconfig_result = subprocess.check_output(["ifconfig", interface])

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

	if mac_address_search_result:
		return mac_address_search_result.group(0)

	else:
		print("Sorry no mac address")

options = get_arguments()

interface = options.interface
new_mac = options.new_mac

current_mac = get_current_mac(interface)
print("[+] Current MAC " + str(current_mac))

change_mac(interface, new_mac)

current_mac = get_current_mac(interface)

if current_mac == new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)

else:
	print("[-] Operation failed...")
