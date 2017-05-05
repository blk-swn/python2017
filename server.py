from socket import *
import pickle
from threading import Thread


class serverTcp():

    def __init__(self):
        self.host = ''
        self.port = 5001
        self.soc = None
        self.userList = []
        self.connections = []

    def start(self):
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.soc.bind((self.host, self.port))
        self.soc.listen(10)
        print("socket created...")

        while True:
            print("waiting for a client to connect...")
            con, addr = self.soc.accept()
            t = Thread(target=self.tcpLink, args=(con, addr))
            t.start()
            self.connections.append(t)

    def tcpLink(self, con: socket, addr: tuple):
        auth = False
        count = 0
        user = []

        print("Connection from: %s" % str(addr))
        print("starting chat for the client")
        self.chat(con, addr)

    def chat(self, con: socket, addr: tuple):
        while True:
            msg = self.readMsg(con)
            if msg in ['q', 'exit', 'quit']:
                break
            print(msg)
            self.writeMsg(con, msg)
        print("client %s disconnecting..." % str(addr))
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

    def writeMsg(self, con, msg):
        try:
            print(str(type(msg)))
            msg = str(msg).upper()
            data = pickle.dumps(msg)
            con.send(data)
            print("Sent: '%s'" % msg)
        except Exception as e:
            print("ERROR [writeMsg] %s " % str(e))

    def openFile(self):
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





server = serverTcp()
server.start()