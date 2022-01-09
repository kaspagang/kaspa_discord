from os import times
from random import seed
from socket import socket
from kaspy.client import kaspa_client
import time

#kaspa_network.run()
#kaspa_network.scanner.cancel()

get_peers = 'getPeerAddressesRequest'

vulnerable_hosts = set()
scanned_hosts = set()
seeds = set([
        f"mainnet-dnsseed.daglabs-dev.com",
        f"mainnet-dnsseed-1.kaspanet.org",
        f"mainnet-dnsseed-2.kaspanet.org",
        f"dnsseed.cbytensky.org",
        f"seeder1.kaspad.net",
        f"seeder2.kaspad.net",
        f"seeder3.kaspad.net",
        f"seeder4.kaspad.net",
        f"kaspadns.kaspacalc.net"
    ])

start = time.time()

def hosts_from_get_peers(peers):
    peers = peers['getPeerAddressesResponse']['addresses']
    if peers:
        return set([peer['Addr'].rsplit(':', 1)[0] for peer in peers])
    
def yield_hosts():
    new_hosts = seeds
    while True:
        hosts = new_hosts
        new_hosts = set()
        for host in hosts:
            print()
            if kaspa_network.is_port_open(host, DEFAULT_PORT, 0.5):
                try:
                    client = kaspa_client()
                    client.connect(host, DEFAULT_PORT)
                    new_addrses = hosts_from_get_peers(client.request(get_peers))
                    if new_addrses:
                        new_hosts.update(new_addrses)
                    vulnerable_hosts.add(host)
                    yield host
                except Exception as e:
                    print(e)
                scanned_hosts.add(host)
                print(f'scanned : {len(scanned_hosts)}, vulnerable :{len(vulnerable_hosts)} time : {time.time()-start}')
            new_hosts = new_hosts - scanned_hosts
                

[x for x in yield_hosts()]