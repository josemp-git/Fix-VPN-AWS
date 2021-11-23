import boto3
import urllib3

regionId = 'us-east-1'
ipcheck_url = 'http://checkip.amazonaws.com/'
http = urllib3.PoolManager()

def vpnfix(regionId):
	client = boto3.client('ec2',region_name=regionId)
	response = client.describe_customer_gateways(
		Filters=[
			{
				'Name': 'state',
				'Values': [
					'available',
				]
			},
		],
	)
	response2 = response["CustomerGateways"]
	for s in range(len(response2)):
		cgipaddress = format(response2[s]["IpAddress"])
		currentcgid = format(response2[s]["CustomerGatewayId"])
		bgpasn = int(format(response2[s]["BgpAsn"]))
		#print("Current customer gateway:")
		print("Customer gateway IP address:", cgipaddress)
		#print("Customer gateway id:", currentcgid) 
		#print("BGP ASN:", bgpasn)

	#Get local IP address
	resp = http.request("GET", ipcheck_url)
	localip = str(resp.data)
	localip = localip.replace("b'",'')
	localip = ''.join(localip.split())[:-3]
	print("Local IP address:", localip)
	
	if cgipaddress == localip:
		print("IP addresses match. Nothing to do here.")
		
	else:
		print("Local IP address is different from the customer gateway's IP address. VPN connection is down. Let's fix this!")	
		
		response = client.create_customer_gateway(
    	BgpAsn=bgpasn,
    	PublicIp=localip,
    	Type='ipsec.1',
    	DryRun=False
		)
		response2 = response["CustomerGateway"]
		newcgid=response2.get("CustomerGatewayId")
		print("The new customer gateway has been created with id:", newcgid)
		
		response = client.describe_vpn_connections()
		response2 = response["VpnConnections"]
		for s in range(len(response2)):
			print("The VPN connection id is: {}".format(response2[s]['VpnConnectionId']))
			vpnid=str(format(response2[s]['VpnConnectionId']))
	 		
		response = client.modify_vpn_connection(
		VpnConnectionId=vpnid,
		CustomerGatewayId=newcgid,
		DryRun=False
		)
		print("The new customer gateway has beed added to the VPN connection.")	
		response = client.delete_customer_gateway(
		CustomerGatewayId=currentcgid,
		DryRun=False
		)
		print("The old customer gateway has been deleted")
vpnfix(regionId)