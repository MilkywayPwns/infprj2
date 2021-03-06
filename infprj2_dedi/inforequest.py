import socket
from packet import Packet

def Packet_GetInfo(srv,client,args):
    # debug print
    print("[INFO]: Server info request received, sending back lobby data.")

    # tell the client about our server                                        - 1 to filter out the current client
    client.send(bytes("inforesponse:{}:{}".format(srv.name, srv.clientcount() - 1), 'utf-8'))

    # server info packet, we want to disconnect those clients.
    return False