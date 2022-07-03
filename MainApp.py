



import sys
import socket
from _thread import *





class ConnectionConfiguration :
    def __init__(ConnectionConfiguration,IPADDRESS,PORT,PROTOCOL,SERVERCLIENT):
        ConnectionConfiguration.IPADDRESS=IPADDRESS
        ConnectionConfiguration.PORT=PORT
        ConnectionConfiguration.PROTOCOL=PROTOCOL
        ConnectionConfiguration.SERVERCLIENT=SERVERCLIENT

ipv4 = socket.AF_INET
tcp =  socket.SOCK_STREAM
udp =  socket.SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def encodingMessages(text):
    return str.encode(text)

arg_help = "MainApp.py <ip address> <port> <Server -s \ Client -c>  <tcp -t \ udp -u> "

def Configuration ():
    ConnectionConfiguration.IPADDRESS=str(sys.argv[1])
    ConnectionConfiguration.PORT=int(sys.argv[2])
    ConnectionConfiguration.PROTOCOL=sys.argv[4]
    ConnectionConfiguration.SERVERCLIENT=sys.argv[3]
      
def multiConnections(connection:socket):
    connection.send(str.encode('This is a TCP Server'))
    while True:
        try :
            received = connection.recvfrom(1024)
            replay = 'Message form the Server: ' + received[0].decode('utf-8')
            if not received :
                break
            connection.sendall(str.encode(replay))
    
        except socket.error as ERR :
              connection.close()
              break
              
    connection.close()

def startserver(_type,_protocol):
      
     server = socket.socket(_type,_protocol)
     server_address = (ConnectionConfiguration.IPADDRESS, ConnectionConfiguration.PORT)
     server.bind((server_address))
     return server

def startListen(server):
     ClientsNum = 0     
     server.listen()
     printServerDetails()
     while True:
      try :
       clientsocket, client_address =  server.accept()
       print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
       start_new_thread(multiConnections, (clientsocket, ))
       ClientsNum += 1
       print('Clients Number: ' + str(ClientsNum))
      except socket.error as ERR :
        print(ERR)
        startListen()




def userchoose():
    print(f"Server Or Client")
    x=input()
    return x

def printServerDetails():
        print(f"Server type = " , ConnectionConfiguration.PROTOCOL)
        print(f"Server starting on... " , ConnectionConfiguration.IPADDRESS)
        print("Server listening on..." , ConnectionConfiguration.PORT)



#try : 
Configuration()
match ConnectionConfiguration.SERVERCLIENT :
    case '-s':
       
        
        match ConnectionConfiguration.PROTOCOL:
                        case '-t':
                                    startListen(startserver(ipv4,tcp))
                                    
                        case '-u':   
                            if startserver(ipv4,udp):
                                printServerDetails()
                                print(f'UDP SERVER IS UP AND LISTENING')
                                while True:
                                    receiveddata = server.recvfrom(1024)
                                    message = receiveddata[0]
                                    address = receiveddata[1]
                                    clientMsg = "Message from Client: " + message.decode('utf-8')
                                    clientIP  = "Client IP Address: "+ address.decode('utf-8')
                                    server.sendto(encodingMessages('this is UDP server'),address)
                                    print(clientMsg)
                                    print(clientIP)
    case '-c':
         match ConnectionConfiguration.PROTOCOL:
            case '-t':
                     client = socket.socket(ipv4, tcp)
                     server_address = (ConnectionConfiguration.IPADDRESS, ConnectionConfiguration.PORT)
                     try :
                         client.connect(server_address)
                         print(f"Connected")
                         client.send(('this is TCP client').encode('utf-8'))
                         MsgFromServer = client.recvfrom(1024)
                         msg = 'Message from Server :'+ MsgFromServer[0].decode('utf-8')
                         print(msg)
                     except socket.error as ERR:
                            print('Cant connect to :'+ server_address[0].decode('utf-8'))
                            print(str(ERR)) 
                            client.close()
                            userchoose()   
                     finally:
                             client.close()
                     

            case '-u':
                    client = socket.socket(ipv4, udp)
                    server_address = (ConnectionConfiguration.IPADDRESS, ConnectionConfiguration.PORT)
                    print(f"Connecting... ")
                    try :
                        client.settimeout(2)
                        client.sendto(encodingMessages('this is UDP client'),server_address)                
                        MsgFromServer = client.recvfrom(1024)
                        msg = "Message from Server :" + MsgFromServer[0].decode('utf-8')
                        print(msg)
                    except socket.error as ERR:
                     print('Cant connect to :' + server_address[0].decode('utf-8'))
                     print(str(ERR)) 
                     client.close()
                     userchoose()   
                    finally:
                        client.close()
#except:
 #       print(arg_help)
  #      sys.exit(2)        


     
  