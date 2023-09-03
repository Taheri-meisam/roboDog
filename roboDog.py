#Import everything in the control module, 
#including functions, classes, variables, and more.

from Control import *
import socket
import sys
from Led import * 

if len(sys.argv) > 1:
    server_ip = sys.argv[1]
else:
    server_ip = '127.0.0.1'  # server ip
server_port = 50005      # port number

# Create a UDP socket and bind
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((server_ip, server_port))
recivedData = "Null"
control=Control()
led = Led()
print(f"UDP server listening on {server_ip}:{server_port}")

def MoveForward(): 
    control.forWard()
    led.colorWipe(led.strip,Color(0,0,255))

def MoveBackward():
    control.backWard()

def controlData(data,clientAddress):
    recievedData = data.decode('utf-8')
    print(recievedData)
    print(f" data recieved : {recievedData} from {clientAddress}")
    if (recievedData[0] == '1'):
        MoveForward()
        control.stop()
    if(recivedData[1] == '2'):
        MoveBackward()
        control.stop()


while True:
    try:
        data,clientAddress = udp_socket.recvfrom(1024)
        controlData(data,clientAddress)
    except KeyboardInterrupt:
        print("Server Stopped")
        control.relax()
        led.colorWipe(led.strip,Color(0,0,0))
        break
udp_socket.close()

control.stop()
