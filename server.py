from socket import *
import pickle
from threading import Thread
import statistics
'''
    This is the server class it handles everything on the server side.
'''

#print("imran")
#name = input("What is your name? ")
#print(name)

#def getName():
#    name = input("What is your name? ")
#    print(name)

#getName()



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

        self.usersLoggedOn = []
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

    '''
        Don't get confused with the arguments, i am simply telling the compiler what
        type of object to expect.
    '''
    def tcpLink(self, con, address):
        auth = False
        user = []

        print("Connection from: %s" % str(address))

        '''
            This is the main client function. When a client connects, 
            the server will immediately attempt to authorise the user.    
        '''
        for i in range(3):
            result = ""

            attempt = self.readMsg(con)

            authUser = self.check_credentials(attempt)

            if authUser:
                result += "1OK"
                if attempt not in self.usersLoggedOn:
                    auth = True
                    result += ":2OK"
                    user = attempt
                    self.usersLoggedOn.append(user)
                else:
                    result += ":2NO"
            else:
                result += "1NO"

            self.writeMsg(con, result)

            if auth:
                break

        if auth:
            print("\n%s authenticated.\n" % str(user))
            #self.chat(con, address, user)
            while True:
                msg = self.readMsg(con)

                if msg in ['q', 'quit', 'exit', '5']:
                    self.quitProgram(user, con)
                    break

                elif msg == '1':
                    self.getServerNameIp(con)

                elif msg == '2':
                    self.getStatistics(con)

                elif msg == '3':
                    self.addNewOrganisation(con)

                elif msg == '4':
                    self.removeOrganisation(con)

                else:
                    print("bad user...")
                    break

        print("The End")

    def getServerNameIp(self, con: socket):
        self.writeMsg(con, "1OK")

        request = self.readMsg(con)

        serverFile = self.get_server_list()

        organisations = [item[0] for item in serverFile]

        if request in organisations:
            self.writeMsg(con, "Organisation Found...")

        else:
            print("not ok")
            self.writeMsg(con, "server not ok")

    def getStatistics(self, con: socket):
        self.writeMsg(con, "2OK")

        serverFile = self.get_server_list()
        uptimeStr = [item[3] for item in serverFile]
        uptimes = list(map(int, uptimeStr))
        '''
            We need to sort the list of uptimes into an ascending order
            to calculate the median. There are alot of ways to do this 
            in Python. In this case I am using List Comprehensions to 
            iterate and sort the list.
        '''
        #times = sorted(uptimes)
        print("Pre-sort: %s" % str(uptimes))
        uptimes.sort(key=lambda x: x)
        print("Post-sort: %s" % str(uptimes))
        # Calculate the average
        #score = 0
        #for element in uptimes:
        #    score += element
        #average = score / len(uptimes)

        # Calculate the average
        average = statistics.mean(uptimes)

        # Calculate the median
        ''' 
            If the no. of elements in the list is a even one
            there is no "middle". Instead a "mean" is calculated
            from the upper middle and lower middle elements.
        '''
        if len(uptimes) % 2 == 0:
            idx1 = (len(uptimes) / 2) - 1
            idx2 = (len(uptimes) / 2)
            num1 = uptimes[int(idx1)]
            num2 = uptimes[int(idx2)]
            median = (num1 + num2) / 2
        else:
            idx = ((len(uptimes) + 1) / 2) - 1
            median = uptimes[int(idx)]

        # Max
        maximum = max(uptimes)

        # Min
        minimum = min(uptimes)

        #statsList = [
        #    ["Mean", str(average)],
        #    ["Median", str(median)],
        #    ["Minimum", str(minimum)],
        #    ["Maximum", str(maximum)]
        #]

        #statsReport = "Mean: %s\n" % str(average)
        #statsReport += "Median: %s\n" % str(median)
        #statsReport += "Minimum %s\n" % str(minimum)
        #statsReport += "Maximum %s\n" % str(maximum)


        rep = '{:*^36}\n'.format('')
        rep += '{:^36}\n'.format('Uptime Statistics Report')
        rep += '{:*^36}\n'.format('')
        rep += '{:18}'.format('Mean:')
        rep += '{:>18}\n'.format(str(round(average, 2)))
        rep += '{:18}'.format("Median:")
        rep += '{:>18}\n'.format(str(median))
        rep += '{:18}'.format("Minimum:")
        rep += '{:>18}\n'.format(str(minimum))
        rep += '{:18}'.format("Maximum:")
        rep += '{:>18}\n'.format(str(maximum))

        self.writeMsg(con, rep)

    def addNewOrganisation(self, con: socket):
        self.writeMsg(con, "Add a new org...")

    def removeOrganisation(self, con: socket):
        self.writeMsg(con, "Remove org...")

    def quitProgram(self, user, con: socket):
        self.usersLoggedOn.remove(user)
        con.close()
        #self.soc.close()

    def create_report(self, ave, med, mini, maxi):
        rep = '{:*^36}\n'.format('')
        rep += '{:^36}\n'.format('Uptime Statistics Report')
        rep += '{:*^36}\n'.format('')
        rep += '{:18}'.format('Mean:')
        rep += '{:>18}\n'.format(str(round(ave, 2)))
        rep += '{:18}'.format("Median:")
        rep += '{:>18}\n'.format(str(med))
        rep += '{:18}'.format("Minimum:")
        rep += '{:>18}\n'.format(str(mini))
        rep += '{:18}'.format("Maximum:")
        rep += '{:>18}\n'.format(str(maxi))

        return rep

    def check_credentials(self, attempt):
        '''
            This function will use the get_auth_list function
            to return a list of valid users. The attempt is passed
            through as an argument and compared against the "database"
        '''

        authList = self.get_auth_list()

        if attempt in authList:
            return True
        else:
            return False


    def chat(self, con: socket, address: tuple, user):
        while True:
            msg = self.readMsg(con)
            if msg in ['q', 'exit', 'quit']:
                self.usersLoggedOn.remove(user)
                break
            print("Received: %s" % msg)
            self.writeMsg(con, msg)
        print("client %s disconnecting..." % str(address))

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

            #msg = str(msg).upper()

            data = pickle.dumps(msg)

            con.send(data)

            print("Sent: '%s'" % msg)
        except Exception as e:
            print("ERROR [writeMsg] %s " % str(e))

    def get_server_uptimes(self):
        serverList = self.get_server_list()

        uptimeList = [item[0] for item in serverList]

        #for values in serverList:
        #    output.append(values[3])

        return uptimeList

    def get_server_list(self):
        try:
            f = open("organisations.dat", 'r')
        except IOError as e:
            print("File could not be found...")
        else:
            raw = f.readlines()
            f.close()
            lines = list(map(str.split, raw))
            return lines

    def get_auth_list(self):
        '''
            This function opens the file, creates a list out of the contents
            and returns the list to the caller
        '''
        try:
            f = open('auth.dat', 'r')
            try:
                raw = f.readlines()

                lines = list(map(str.split, raw))

                #print(lines)
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
