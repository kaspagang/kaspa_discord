from logging import getLogger, basicConfig, INFO
from typing import Set, Union, Iterator
import socket
import time
from ..log_handler.log_messages import network as net_lm
from ..defines import P2P_DEF_PORT, RPC_DEF_PORT

basicConfig(level=INFO)
LOG = getLogger('[KASPA_NOD]')


class query_node:
    '''some socket things to navigate and check connectivity'''
    
    @classmethod
    def port_open(cls, ip : str, port: Union[int, str], timeout : float) -> bool:
        LOG.info(net_lm.PORT_QUERY(f'{ip}:{port}'))
        sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            if sock.connect_ex((ip, int(port))) == 0:
                LOG.info(net_lm.CHECK_PORT_STAUTS_OPEN(f'{ip}:{port}', port))
                port_open = True
            else:
                LOG.info(net_lm.CHECK_PORT_STAUTS_CLOSED(f'{ip}:{port}', port))
                port_open = False
        except Exception as e:
            LOG.debug(e)
            LOG.info(net_lm.CHECK_PORT_STAUTS_CLOSED(f'{ip}:{port}', port))
            port_open = False
        finally: sock.close()
        return port_open
    
    @classmethod
    def latency(cls, ip : str, port : Union[int, str], timeout: float) -> Union[float, None]:
        LOG.info(net_lm.LATENCY_QUERY(f'{ip}:{port}'))
        sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            start = time.perf_counter()
            sock.connect((ip, int(port)))
            latency = time.perf_counter() - start
            LOG.info(net_lm.CHECK_LATENCY_STATUS_DELAY(f'{ip}:{port}', latency))
        except Exception as e:
            LOG.debug(e)
            LOG.info(net_lm.CHECK_LATENCY_STAUTS_NONE(f'{ip}:{port}'))
            latency= None
        finally: sock.close()
        return latency            
    
    @classmethod
    def connected_peers(cls, ip : str, port : Union[str, int]) -> Union[Set[str], None]:
        try:
            return set([f'{addr[-1][0]}:{port}' for addr in socket.getaddrinfo(host=ip, port=int(port))])
        except Exception as e:
            LOG.debug(e)
            return None

class Node:
    
    def __init__(self, ip: str, rpc_port = RPC_DEF_PORT, p2p_port = P2P_DEF_PORT) -> None:
        self.ip = ip 
        self.rpc_port = RPC_DEF_PORT
        self.p2p_port = P2P_DEF_PORT
    
    @property
    def rpc_addr(self) -> str:
        return f'{self.ip}:{self.rpc_port}'
    @property
    def p2p_addr(self) -> str:
        return f'{self.ip}:{self.p2p_port}'
    
    def rp2_port_open(self, timeout : Union[int, float]) -> None:
        return query_node.port_open(self.ip, self.rpc_port, timeout)
    
    def p2p_port_open(self, timeout : Union[int, float]) -> bool:
        return query_node.port_open(self.ip, self.rpc_port, timeout)
    
    def port_open(self, timeout : str, service : str = NotImplemented) -> bool:
        return query_node.port_open(self.ip, self.rpc_port, timeout)
    
    def latency(self, timeout : str, service : str = NotImplemented) -> bool:
        return query_node.latency(self.ip, self.rpc_port, timeout)
    
    def __str__(self) -> str:
        return f'{self.ip}:{self.rpc_port}' #keep for comaptibility with client class until dual RPC and P2P connections are dealt with
    
class node_acquirer:
    
    dns_seed_servers = [
        f"mainnet-dnsseed.daglabs-dev.com",
        f"mainnet-dnsseed-1.kaspanet.org",
        f"mainnet-dnsseed-2.kaspanet.org",
        f"dnsseed.cbytensky.org",
        f"seeder1.kaspad.net",
        f"seeder2.kaspad.net",
        f"seeder3.kaspad.net",
        f"seeder4.kaspad.net",
        f"kaspadns.kaspacalc.net"
    ]
    
    @classmethod
    def yield_open_nodes(cls, max_latency : float, timeout : float, service = NotImplemented) -> Iterator[Node]:
        LOG.info(net_lm.SCANNING)
        while True:
            scanned = set()
            for dns_server in cls.dns_seed_servers:
                addresses = query_node.connected_peers(ip=dns_server, port=RPC_DEF_PORT) - scanned
                LOG.info(net_lm.SCANNING_RETRIVED_NODES_FROM(dns_server, addresses))
                if not addresses: continue
                for addr in addresses:
                    node = Node(addr.rsplit(':', 1)[0])
                    LOG.info(net_lm.CHECK_NODE(node))
                    scanned.add(node.rpc_addr)
                    latency, port_open = node.latency(timeout), node.port_open(timeout)
                    if not isinstance(latency, type(None)) and latency <= max_latency:
                        LOG.info(net_lm.CHECK_LATENCY_APPROVED(node.rpc_addr, latency, max_latency))
                    else:
                        LOG.info(net_lm.CHECK_LATENCY_DENIED(node.rpc_addr, latency, max_latency))
                        continue
                    if port_open:
                        #LOG.info(net_lm.CHECK_PORT_APPROVED(node.rpc_addr))
                        yield node
                    else: continue
                        #LOG.info(net_lm.CHECK_PORT_DENIED(node.rpc_addr))