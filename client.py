import pickle
from socket import *

'''
    This is the client side. Everything the client does is inside this class named clientTcp().
    Its pretty easy to understand once you break it up. I have split most of the program up into functions.
    def readMsg() is a function for reading messages from the server and writeMsg() is a similar function that 
    handles writing messages to the server. 
'''
class clientTcp():
    def __init__(self):
        self.host = ''
        self.port = 5001
        self.soc = socket(family=AF_INET, type=SOCK_STREAM)

        self.authorised = False
        self.credentials = []

    def start(self):

        try:
            self.soc.connect((self.host, self.port))
            print("client connected to the server...")
        except error as e:  # socket.error has been raised. Is the server running?
            print("Error connecting to the server: %s" % str(e))

        else:
            print("starting for loop to authorise the user")

            for i in range(3):

                username = input("Username: ")
                password = input("Password: ")

                attempt = [username, password]  # Store the username and password pair in a list.
                print(attempt)
                self.writeMsg(attempt)
                print("wrote credentials")
                #username = input("Username: ")

                msg = self.readMsg()

                if msg == 2:
                    print("Welcome!")
                    self.authorised = True
                    break

                elif msg == 1:
                    print("user already logged on, you have {} attempts remaining".format(2 - i))

                elif msg == 0:
                    print("incorrect username or password, you have {} attempts remaining".format(2 - i))

            if self.authorised:
                while True:
                    self.menu()
                    selection = input("Enter your choice: ")

                    if selection == '1':
                        self.getServerNameIp()

                    elif selection == '2':
                        self.getStatistics()

                    elif selection == '3':
                        self.addNewOrganisation()

                    elif selection == '4':
                        self.removeOrganisation()

                    elif selection == '5':
                        self.quitProgram()
                        break
                    else:
                        print("bad user...")

                    option = input("Play again? (y/n): ")

                    if option == 'n':
                        self.quitProgram()
                        break

        self.soc.close()
        print("Have a lovely day!")

    def getServerNameIp(self):
        print("Get the server name and IP...")
        self.writeMsg("1")
        msg = self.readMsg()
        if msg == '1OK':

            request = input("Enter the organisations name: ")
            self.writeMsg(request)

            reply = self.readMsg()
            print(type(reply))
            print(reply)

    def getStatistics(self):
        self.writeMsg("2")
        msg = self.readMsg()

        if msg == "2OK":
            result = self.readMsg()
            print(type(result))
            print(result)

    def addNewOrganisation(self):
        self.writeMsg("3")
        orgName = None
        orgURL = None
        orgIP = None
        orgUptime = None
        newOrganisation = []

        msg = self.readMsg()

        if msg == "3OK":
            orgName = input("What is the organisations name? ")
            orgURL = input("What is the organisations URL? ")
            orgIP = input("What is the organisations IP address? ")
            orgUptime = input("What is the organisation's server up-time? ")

            newOrganisation = [orgName, orgURL, orgIP, orgUptime]

            self.writeMsg(newOrganisation)

            msg = self.readMsg()
            print(msg)



    def removeOrganisation(self):
        self.writeMsg("4")
        msg = self.readMsg()
        print(msg)

    def quitProgram(self):
        self.writeMsg("5")
        self.soc.close()

    def authenticate(self):
        ''' 
            A small functions that asks the user to enter a username
            and password. They are inserted into a list object and 
            sent to the server. 
        '''
        username = input("Username: ")
        password = input("Password: ")

        attempt = [username, password]  # Store the username and password pair in a list.

        self.writeMsg(attempt)  # Send the attempt over the network to the server.

    def readMsg(self):
        ''' 
        This function looks confusing because of the exceptions 
        Without the exceptions it looks like this:
        
            data = self.soc.recv(1024)
            msg = pickle.loads(data)
            return msg
        
        pickle comes with the standard library. It is used to 
        serialize objects so they can be sent over the network.
        Similar to how we encoded an decoded the text to utf-8,
        we now serialize and deserialize the object.
        '''
        try:
            data = self.soc.recv(1024)
            try:
                msg = pickle.loads(data)
            except:
                print("error pickling data")
            else:
                return msg
        except error as e:
            print("ERROR: %s" % str(e))

    def writeMsg(self, msg: object):
        try:
            data = pickle.dumps(msg)
            try:
                self.soc.send(data)
            except error: # socket.error raised
                print("error sending data")
        except pickle.PicklingError:
            print("error serializing the object...")
        except:
            print("unknown error serializing...")

    def menu(self):
        menu = '{:*^54}\n'.format('')
        menu += '{:^54}\n'.format('Menu')
        menu += '{:*^54}\n'.format('')
        menu += '(1) {:20}\n'.format('Get Server Name and IP Address')
        menu += '(2) {:20}\n'.format('Get Server Stats (mean, median, minimum, maximum)')
        menu += '(3) {:20}\n'.format('Add a new organisation')
        menu += '(4) {:20}\n'.format('Remove an organisation')
        menu += '(5) {:20}\n'.format('Quit program')
        print(menu)

client = clientTcp()
client.start()
