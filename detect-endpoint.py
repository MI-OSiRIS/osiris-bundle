#!/usr/bin/env python

import socket
import sys
import argparse

http = 'https://'
domain = 'osris.org'

# default list of regions to try connecting to
# all = RR DNS record using all 3 regions
regions = ['all','um','msu','wsu','vai']

rs = ' '.join(regions)

serverlist = dict()
serverlist['all'] = 'rgw'
serverlist['um'] = 'rgw-um'
serverlist['msu'] = 'rgw-msu'
serverlist['wsu'] = 'rgw-wsu'
serverlist['vai'] = 'rgw-vai-int'

class RegionArgAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # catch comma separated list
        rlist = values[0].split(',')
        if len(rlist) == 1:
            rlist = values
        if set(rlist).issubset(regions):
            setattr(namespace, self.dest, rlist)
        else:
            parser.error("Region arguments do not match any available region from: {0}\n".format(rs))

parser = argparse.ArgumentParser(description='Determine reachable OSiRIS S3 region from this host. Default is to use all regions if reachable.')
parser.add_argument("regions", metavar='REGION', nargs='*', default=regions,
    help="Optional list of region(s) to check in order listed.  Available regions:  {0}".format(rs),
    action=RegionArgAction)
args = parser.parse_args()

def construct_fqdn(hostname):
    return '{0}.{1}'.format(hostname, domain)

# cycle through list of servers, break on the first one we find with all IP reachable

for region in args.regions:
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


