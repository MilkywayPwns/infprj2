import socket
import client
import commands
import threading
import packets
from packet import Packet

class Server:
    def __init__(self, host, port):
        # open the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind our server to a port
        self.sock.bind(("", 61022))

        # start listening to incoming requests
        self.sock.listen(10)
  
        # Set active to true
        self.isActive = True

        # This will hold an array of connected clients
        self.clients = []

        # Server name
        self.name = ""

        # Current turn
        self.current_player = 0
        self.has_started = False

        # packets that should be emulated for new clients
        self.emulateablepackets = []

    # client related shit
    def cli_max_index(self):
        max = 0
        for x in self.clients:
            if x.index > max:
                max = x.index

        return max
    def cli_min_index(self):
        min = self.cli_max_index()
        for x in self.clients:
            if x.index < min:
                min = x.index

        return min

    # sends a message to all clients
    def send_all(self, command):
        for cli in self.clients:
            if not cli.sock._closed and not cli.isDisconnecting:
                cli.send(command)

        # for the newbies that are connecting at a later point
        self.emulateablepackets.append(command) 

    def clientcount(self):
        idx = 0

        for x in self.clients:
            idx += 1
        return idx

    def add_client(self, clnt):
        clnt.set_index(self.clientcount())
        self.clients.append(clnt)
        
        print("[INFO]: Client {} connected to the server!".format(clnt.index))

    def start_match(self):
        # Don't attempt to start a match if its already started
        if self.has_started:
            return

        # set started to true
        self.has_started = True

        print("[INFO]: Match started.")

        # let the clients know that the match has been started.
        self.send_all(Packet("startmatch").get())
        
        # choose a start position for each client
        idx = 1
        for x in self.clients:
            self.send_all(Packet("clientstart:{}:{}:0:0".format(x.index, idx)).get())
            idx += 1

        # tell the clients who's about to start.
        self.current_player = self.clients[0].index
        self.send_all(Packet("setplayerindex:{}".format(self.current_player)).get())

        pass

    def stop_match(self):
        self.has_started = False
        
        for x in self.clients:
            x.disconnect()

        self.clients.clear()
        self.emulateablepackets.clear()
        self.current_player = 0

        print("[INFO]: Match stopped.")

    def connection_loop(self):
        while self.isActive:
            conn, addr = self.accept()
            clientthread = threading.Thread(target = client.thread, args = (self,conn))
            clientthread.setDaemon(True)
            clientthread.start()
    def accept(self):
        return self.sock.accept()
    def shutdown(self):
        self.isActive = False

# main function of the dedicated server
def init():
    print("[INFO]: Starting up opseilen dedicated server...")

    # init the sock var
    srv = None

    # create the socket for the server
    try:
        # open the socket
        srv = Server("localhost", 61022)

    except socket.error as err:
        srv.sock.close()
        print("[ERROR]: Dedicated server init failed, socket could not be created. Errorcode is {}.".format(err))
        quit()

    # add commands to command array
    commands.init()
    packets.init()

    # info
    print("[INFO]: Dedicated server initialization complete.");

    # Ask for a lobby name
    srv.name = input("Please enter the name of the lobby: ")

    # start command thread
    commandthread = threading.Thread(target = commands.cmdthread, args = (srv,))
    commandthread.setDaemon(True)
    commandthread.start()

    # wait for clients to connect...
    srv.connection_loop()

    # close socket
    srv.sock.close()

# Start the dedicated server
init()