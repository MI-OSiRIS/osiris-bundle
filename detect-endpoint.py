#!/usr/bin/env python

import socket
import sys

http = 'https://'
domain = 'osris.org'

serverlist = dict()

# generally all needs to be first, the rest not as important
checkorder = ['all','um','msu','wsu','vai']

serverlist['all'] = 'rgw'
serverlist['um'] = 'rgw-um'
serverlist['msu'] = 'rgw-msu'
serverlist['wsu'] = 'rgw-wsu'
serverlist['vai'] = 'rgw-vai-int'

def construct_fqdn(hostname):
	return '{0}.{1}'.format(hostname, domain)

# cycle through list of servers, break on the first one we find with all IP reachable

for region in checkorder:
	# print "Checking {0}".format(construct_fqdn(serverlist[region]))
	serverips = socket.gethostbyname_ex(construct_fqdn(serverlist[region]))
	
	# only interested in 3rd tuple value
	for ipaddr in serverips[2]:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2)
		result = sock.connect_ex((ipaddr, 443))
		sock.close()
		if result == 0:
			# print "reached {0}".format(ipaddr)
			use_region = True
		else:
			# print "no reach {0}".format(ipaddr)
			use_region = False
			break
	if use_region:
		use_region = region
		# print 'set use_region'
		break

if use_region == False:
	print('No reachable rgw endpoint was found')
	sys.exit(1)
		
print('{0}{1}'.format(http,construct_fqdn(serverlist[use_region])))


