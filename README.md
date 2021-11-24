# Fix-VPN-AWS

This tool automates the creation of a new customer gateway in case the local IP address changes. It also modifies the current
site-to-site VPN connection by adding the newly created customer gateway and deletes the old one.

This tool is ideal if you don't have an static IP address, and your dynamic IP address changes often, which brings your VPN
connection down if . You can schedule the execution of this script, so that it constantly verifies that everything is up
and  running.
