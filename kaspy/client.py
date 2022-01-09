from threading import Event, Lock, Thread
from collections import defaultdict
from typing import Iterable, Iterator, Union
import time

import grpc
import json
from google.protobuf import json_format
from logging import INFO, getLogger, basicConfig

from .network.node import Node, node_acquirer
from .protos.messages_pb2 import KaspadMessage, _KASPADMESSAGE
from .protos.messages_pb2_grpc import RPCStub
from .defines import LATEST_KASPAD_VERSION, MAINNET
from .log_handler.log_messages import client as cli_lm
from .utils.version_control import version as ver
from .excepts.exceptions import RPCResponseException

from queue import SimpleQueue

basicConfig(level=INFO)
LOG = getLogger('[KASPA_CLI]')

CONNECTED = 'connected'
DISCONNECTED = 'disconnected' #waits for all queued data to be sent
CLOSED = 'closed'

STATES = (CONNECTED,DISCONNECTED,CLOSED) 


class server_health_checker: 
    '''
    Register and handle changes in server status
    Reference:  https://github.com/grpc/grpc/blob/master/doc/health-checking.md
    --> "A client can declare the server as unhealthy if the rpc is not finished after some amount of time. 
    The client should be able to handle the case where server does not have the Health service." 
    Note: No Health Checking protocol seems to be implemented on server side.
    
    '''

    def __init__(self) -> None:
        raise NotImplementedError

class client_health_checker:
    '''
    register and handle changes in client status
    '''

    def __init__(self) -> None:
        raise NotImplementedError

 
class kaspa_client:
    
    def __init__(self) -> None:
        self._RPCstub = RPCStub
        self._P2Pstub = NotImplemented
        self._chan = None
        self.node = Node
        self._is_connected = lambda : True if self._chan else False
        self.server_status = NotImplemented #hold server status from grpc.RpcErrors
        self.client_status = NotImplemented
        self.subscriptions = defaultdict(dict) #hold subscription streams
        
        #for threading
        self._requests = SimpleQueue() # `_requests` holds all messages queued to be sent
        self._responses = SimpleQueue() # responses pertain to reqeust messages
        self._subscitptions = NotImplemented
        self._notifications = NotImplemented 
        self._lock = Lock()
        self._activate_stream = Event()
        self._streamer = Thread(target=self._stream, daemon=True)
    
    def disconnect(self) -> None:
        self.client_status = DISCONNECTED
        self._activate_stream.clear()
        self._requests.put(DISCONNECTED) #finish getting all requests until DISCONENCT is injected into the request_iterator 
    
    def close(self) -> None:
        self.client_status = CLOSED
        self._requests._queue.appendleft(CLOSED) #skip the queue
        self._chan.close()
    
    def subscribe(self, command : str, payload: Union[dict, str, None] = None) -> None:
        raise NotImplementedError
    
    def unsubscribe(self) -> None:
        raise NotImplementedError
    
    def is_notification_response(self, serialized_resp : Union[dict, str]) -> bool: 
        raise NotImplementedError     
    
    def _cancel(self) -> None:
        raise NotImplementedError

    def _serialize_response_to_json(self, response : KaspadMessage) -> str:
        raise NotImplementedError

    def _serialize_request(self, command : str, payload : Union[dict, str]) -> KaspadMessage:
        assert command == _KASPADMESSAGE.fields_by_name[command].name #this is important so we don't execute arbitary python code in this function
        kaspa_msg = KaspadMessage()
        app_msg = eval(f'kaspa_msg.{command}') #should not use eval - but seems like the easiest way for now.
        if payload:
            if isinstance(payload, dict):
                json_format.ParseDict(payload, app_msg)
            if isinstance(payload, str):
                json_format.Parse(payload, app_msg)
        app_msg.SetInParent()
        return kaspa_msg
    
    def _serialize_response_to_dict(self, response: KaspadMessage) -> dict:
        return json_format.MessageToDict(response)
    
    def _stream(self) -> None:
        self._activate_stream.wait()
        try:
            
            for resp in self._RPCstub.MessageStream(req for req in self._requests_iterator()):
                self._responses.put(resp)              
        
        except grpc.RpcError as e: 
            
            # in our case a _MultiThreadedRendezvous raises itself, which requires further parsing
            # for details on this behaviour, see issue: https://github.com/grpc/grpc/issues/25334
            # for help parsing, see source code: https://github.com/grpc/grpc/blob/master/src/python/grpcio/grpc/_channel.py?functions.php#L652
            # explainations of the indivdual codes, see documentation = https://grpc.github.io/grpc/core/md_doc_statuscodes.html
            
            if self.server_status == CLOSED: #closing the channel will raise an RpcError
                pass # let thread return None and finish 
            
            #handle errors:
            code = e.code()
            details = e.details()
            raise RPCResponseException(code, details) # for now raise until we have proper error handling to deal with some cases. 
                
                    
    def _requests_iterator(self) -> Iterator[Union[KaspadMessage, None]]:
        while True:
            req = self._requests.get()
            if req == DISCONNECTED: 
                self._activate_stream.set() # in set the thread to wait
                self._stream() #send to wait in self.stream and halt thread
            elif req == CLOSED:
                pass #kill thread
            else:
                yield req
    
    def send(self, command : str, payload : Union[dict, str, None] = None) -> None:
        if self.server_status == CONNECTED:
            LOG.info(cli_lm.MSG_SENDING(command, self.node))
            self._requests.put(self._serialize_request(command, payload))
        elif self.server_status in set(DISCONNECTED, CLOSED):
            raise Exception
            
    
    def recv(self) -> Iterator[Union[dict, str]]:
        return self._serialize_response_to_dict(self._responses.get())
    
    def request(self, command : str, payload: Union[dict, str, None] = None) -> Union[dict, str]:
        self.send(command, payload)
        resp = self.recv()
        LOG.info(cli_lm.MSG_RECIVED(
            next(iter(resp.keys())),
            command,
            self.node
                    ))
        return resp
    
    def reconnect(self):
        self._activate_stream.set()

    def connect(self, host: str, port: Union[int, str], service = NotImplemented) -> None:
        self.node = Node(host, rpc_port=port)
        LOG.info(cli_lm.CONN_ESTABLISHING(self.node))
        self._chan = grpc.insecure_channel(self.node.rpc_addr, compression=grpc.Compression.Gzip)
        self._RPCstub = RPCStub(self._chan)
        self._streamer.start() if not self._streamer.is_alive() else None
        LOG.info(cli_lm.CONN_ESTABLISHED(self.node))
    
    def auto_connect(self, min_version: Union[ver, str] = LATEST_KASPAD_VERSION, subnetworks: Union[str, Iterable] = MAINNET, 
                     service = NotImplemented, timeout: float = 5, max_latency: float =  5) -> None:
        '''
        Connect to a node, broadcasted by the dns seed servers with the specified kwargs 
        '''
        for node in node_acquirer.yield_open_nodes(max_latency=max_latency, timeout=timeout):
            self.connect(node.ip, node.rpc_port)
            kaspad_ver = self.request('getInfoRequest')
            kaspad_ver = ver.parse_from_string(kaspad_ver['getInfoResponse']['serverVersion'])
            if kaspad_ver < min_version:
                continue
            kaspad_network = self.request('getCurrentNetworkRequest')['getCurrentNetworkResponse']['currentNetwork'].lower()
            if kaspad_network not in subnetworks:
                continue
            break
