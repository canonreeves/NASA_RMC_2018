import socket
from decimal import Decimal
import json
import PyCmdMessenger

UDP_IP = "192.168.1.252"
#UDP_IP = "192.168.1.254"
LAPTOP_IP = "192.168.1.253"
UDP_PORT = 1113

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=9600)
commands = [["shoulder","i"],
            ["elbow","i"],
            ["left_F","i"],
            ["left_B","i"],
            ["right_F","i"],
            ["right_B","i"],
            ["drum","i"]
                        ]
c = PyCmdMessenger.CmdMessenger(arduino,commands)



#initalize variables
shoulder_value = 0.0
elbow_value = 0.0 
left_F_value = 0.0
left_B_value = 0.0
right_F_value = 0.0
right_B_value = 0.0
drum_value = 0.0

count = 0;
while True:
    count = count + 1
    print(count)
    if(count > 600):
        print("Count is too high, exit now")
    data, address = sock.recvfrom(UDP_PORT)
    #print('received {} bytes from {}'.format(
        #len(data), address))
    #print(data)
    json_data = data.decode(encoding = "utf-8")
    json_obj = json.loads(json_data, parse_float = Decimal)
    #print("Printing Drum value: ")
    #print (json_obj['drum'])

    shoulder_value = json_obj['shoulder_value']
    elbow_value = json_obj['elbow_value']
    left_F_value = json_obj['left_F_value']
    left_B_value = json_obj['left_B_value']
    right_F_value = json_obj['right_F_value']
    right_B_value = json_obj['right_B_value']
    drum_value = json_obj['drum_value']
    #pan_value = json_obj['pan_value']
    #tilt_value = json_obj['tilt_value']
    
    """print("left front: " + str(int(left_F_value)))
    print("left back: " + str(int(left_B_value)))
    print("right front: " + str(int(right_F_value)))
    print("right back: " + str(int(right_B_value)))
    print("shoulder: " + str(int(shoulder_value)))
    print("elbow: " + str(int(elbow_value)))
    print("drum: " + str(int(drum_value)))"""

    c.send("left_F",int(-left_F_value)) #-----FIXME-----#
    c.send("left_B",int(left_B_value))
    c.send("right_F",int(-right_F_value)) #Note: front values are negative to filp polatity
    c.send("right_B",int(right_B_value))
    c.send("shoulder",int(shoulder_value))
    c.send("elbow",int(elbow_value))
    c.send("drum",int(drum_value))
    #c.send("pan",int(pan_value))
    #c.send("tile",int(tilt_value))
    
   # data = count.to_bytes(2, byteorder='big')
   # if data:
   #     sent = sock.sendto(data, address)
   #     print('sent {} bytes back to {}'.format(
   #         sent, address))  

