
ABORT = '[aborted]'
SUCCESS = '[successs]'

class network:
    
    # messages pertaining to Scanning for a valid node
    SCANNING = f'''searching for nodes'''
    SCANNING_SEARCHING_FROM = lambda dns_server : f'''[{dns_server}]: finding nodes in dns seed server'''
    SCANNING_RETRIVED_NODES_FROM =  lambda dns_server, nodes : f'''[{dns_server}]: found the following nodes: {nodes}''' 
    SCANNING_RETRIVED_NODE_FROM = NotImplemented
    
    # messages pertaining to checking the status of the node
    CHECK_NODE = lambda node : f'''[{node}]: checking node...'''
    CHECK_APPROVED = '''all checks passed'''
    CHECK_DENIED = NotImplemented
    
    ## messages pertaining to checking the port  
    CHECK_PORT_DENIED = lambda node : f'''[{node}]: port is not OPEN {ABORT}'''
    CHECK_PORT_APPROVED = lambda node : f'''[{node}]: port is OPEN {SUCCESS}'''
    
    ## messages pertaining to checking the latency

    CHECK_LATENCY_DENIED = lambda node, latency, max_latency: f'''[{node}]: latency of {latency} is more then max latency of {max_latency}'''
    CHECK_LATENCY_APPROVED = lambda node, latency, max_latency :f'''[{node}]: latency of {latency} is less then max latency of {max_latency}'''
        
    LATENCY_QUERY = lambda node: f'''[{node}]: querying latency...'''
    CHECK_LATENCY_STAUTS_NONE = lambda node: f'''[{node}]: no connection estblished to check latency'''
    CHECK_LATENCY_STATUS_DELAY = lambda node, latency: f'''[{node}]: latency measured at {int(round(latency*1000, 0))} ms'''
    
    PORT_QUERY =  lambda node: f'''[{node}]: querying if port is open...'''
    CHECK_PORT_STAUTS_OPEN = lambda node, port : f'''[{node}]: port {port} is OPEN {SUCCESS}'''
    CHECK_PORT_STAUTS_CLOSED = lambda node, port : f'''[{node}]: port {port} is CLOSED {ABORT}'''
    
    
class client:
    
    #messages pertaining to client
    CLI_INTIALIZED = f'''starting a new client'''
    
    #messages pertaining to connection status
    CONN_ESTABLISHING = lambda node : f'''[{node}]: Connecting to node...'''
    CONN_ESTABLISHED = lambda node : f'''[{node}]: Connection established'''
    CONN_DISCONNECTING = NotImplemented
    CONN_DISCONNECTED = NotImplemented
    
    #Messages pertaining to sending / Reciving messages
    MSG_SENDING = lambda command, node : f'''[{node}]:[{command}]: Sending request..'''
    MSG_SENT = NotImplemented
    MSG_RECIVING = NotImplemented
    MSG_RECIVED = lambda response, command, node : f'''[{node}]:[{command}]: retrived response {response} {SUCCESS}'''
