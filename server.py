from socket import *
import pickle
from threading import Thread
'''
    This is the server class it handles everything on the server side.
'''


class serverTcp():

    def __init__(self):
        '''
            This is the initializer '__init__' method. When i create an instance of the class
            at the bottom of the file, this method is automatically called and it just initializes
            some variables so we can access them throughout the class. the variables with self. in-front
            of them are like global variables accessible from anywhere in the serverTcp class.
        '''
        self.host = ''
        self.port = 5001
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.userList = []
        self.connections = []

    def start(self):
        '''
            This method opens the socket and accepts client connections.
            When a client connects inside the while True: block, a new thread
            is created and the clients connection is passed on to the main client
            function tcpLink() which will handle authorising the user and so on.
        '''
        self.soc.bind((self.host, self.port))
        self.soc.listen(10)
        print("socket created...")

        while True:
            print("\nwaiting for a client to connect...\n")
            con, addr = self.soc.accept()
            t = Thread(target=self.tcpLink, args=(con, addr))
            t.start()
            self.connections.append(t)

    def tcpLink(self, con: socket, address: tuple):
        auth = False
        count = 0
        user = []

        print("Connection from: %s" % str(address))

        for i in range(3):
            attempt = self.authenticate(con)
            if attempt:
                auth = True
                self.writeMsg(con, "ok")
                break
            else:
                self.writeMsg(con, "no")

        if auth:
            self.chat(con, address)

    def authenticate(self, con: socket):
        attempt = self.readMsg(con)
        auth = self.validate(attempt)
        if auth:
            return True
        else:
            return False


    def validate(self, attempt: list):
        switch = False
        authList = self.openFile()

        if attempt in authList:
            switch = True

        return switch

    def chat(self, con: socket, address: tuple):
        while True:
            msg = self.readMsg(con)
            if msg in ['q', 'exit', 'quit']:
                break
            print("Received: %s" % msg)
            self.writeMsg(con, msg)
        print("client %s disconnecting..." % str(address))
        self.openFile()
        con.close()


    def readMsg(self, con: socket):
        try:
            data = con.recv(4096)
        except Exception as e:
            print("ERROR [readMsg]: %s" % str(e))
        else:
            try:
                msg = pickle.loads(data)
            except Exception as e:
                print("Error [readMsg.pickle]: %s" % str(e))
                return False
            else:
                return msg

    def writeMsg(self, con: socket, msg: object):
        try:

            msg = str(msg).upper()
            data = pickle.dumps(msg)
            con.send(data)
            print("Sent: '%s'" % msg)
        except Exception as e:
            print("ERROR [writeMsg] %s " % str(e))

    def openFile(self):
        '''
            This function opens the file, creates a list out of the contents
            and returns the list to the caller
        '''
        try:
            f = open('auth.dat', 'r')
            try:
                raw = f.readlines()
                lines = list(map(str.split, raw))
                print(lines)
            finally:
                f.close()
                return lines
        except IOError:
            print("Cannot find/read the file.")

'''
    The end of the serverTcp() class. 
'''

server = serverTcp()    # Create an instance of the serverTcp() class
server.start()          # Run the start method.
