import pygame
#import PyCmdMessenger
import socket
import json
from decimal import Decimal

#Socket connection Info
UDP_IP = "192.168.0.18"
UDP_PORT = 1113

#Arduino connection things 
"""arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=9600)
commands = [["shoulder","i"],
            ["elbow","i"],
            ["left_F","i"],
            ["left_B","i"],
            ["right_F","i"],
            ["right_B","i"],
            ["drum","i"]
                        ]
c = PyCmdMessenger.CmdMessenger(arduino,commands)
"""
#initalize variavles
shoulder_value = 0.0
elbow_value = 440.0 
left_F_value = 0.0
left_B_value = 0.0
right_F_value = 0.0
right_B_value = 0.0
drum_value = 0.0

#other variables
#wheels
MAX_speed = 500    #max speed for the wheels out of 1000
delta_speed = 1.0/5.0 * MAX_speed #wheels maximum speed change
#drum
MAX_drum_speed = 600   #max speed for the drum out of 1000
MAX_drum_delta = 100   #max (safe) E-Stop speed
delta_drum_speed = 100 #speed incrament by button press
old_joystick_1 = 0 #drum speed up
old_joystick_2 = 0 #drum slow down
#TEMP #FIXME #Solves the issue of random motor firing on start up
time_delay = 40 # number of ticks to skipp on start up
#E-stop
old_joystick_3 = 0
Estop = 0 #Estop status (True/ False)
#msg read out
msg_readout = 0


# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 150,   0)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def print_red(self, screen, textString):
        textBitmap = self.font.render(textString, True, RED)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def print_green(self, screen, textString):
        textBitmap = self.font.render(textString, True, GREEN)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    



pygame.init()
 
# Set the width and height of the screen [width,height]
size = [300, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        """# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")"""
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    #textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    #textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    #Shoulder:
        shoulder_value = 0
        if (joystick.get_axis(2) >= 0.9):
            shoulder_value += 1000
        if (joystick.get_button(5) == 1):
            shoulder_value -= 1000
            
    #Elbow:
        elbow_value = 0
        if (joystick.get_axis(2) <= -0.9):
            elbow_value += 1000
        if (joystick.get_button(4) == 1):
            elbow_value -= 1000
            
    #Left motor:
        #Front:
        #if speed change is > than 'delta_speed'...
        if(abs(left_F_value-joystick.get_axis(1)*MAX_speed) >= delta_speed):
            #if negative delta
            if(left_F_value < joystick.get_axis(1)*MAX_speed):
                left_F_value += delta_speed
            #if positive delta
            elif(left_F_value > joystick.get_axis(1)*MAX_speed):
                left_F_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            left_F_value = joystick.get_axis(1)*MAX_speed
        #Back:
        #if speed change is > than 'delta_speed'...
        if(abs(left_B_value-joystick.get_axis(1)*MAX_speed) >= delta_speed):
            #if negative delta
            if(left_B_value < joystick.get_axis(1)*MAX_speed):
                left_B_value += delta_speed
            #if positive delta
            elif(left_B_value > joystick.get_axis(1)*MAX_speed):
                left_B_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            left_B_value = joystick.get_axis(1)*MAX_speed

    #Right motor:
        #Front:
        #if speed change is > than 'delta_speed'...
        if(abs(right_F_value-joystick.get_axis(4)*MAX_speed) >= delta_speed):
            #if negative delta
            if(right_F_value < joystick.get_axis(4)*MAX_speed):
                right_F_value += delta_speed
            #if positive delta
            elif(right_F_value > joystick.get_axis(4)*MAX_speed):
                right_F_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            right_F_value = joystick.get_axis(4)*MAX_speed
        #Back:
        #if speed change is > than 'delta_speed'...
        if(abs(right_B_value-joystick.get_axis(4)*MAX_speed) >= delta_speed):
            #if negative delta
            if(right_B_value < joystick.get_axis(4)*MAX_speed):
                right_B_value += delta_speed
            #if positive delta
            elif(right_B_value > joystick.get_axis(4)*MAX_speed):
                right_B_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            right_B_value = joystick.get_axis(4)*MAX_speed

    #drum:
        #forward (dig)
        if(old_joystick_1 == joystick.get_button(1)): #if button is the same...
            drum_value = drum_value #do nothing
        elif(joystick.get_button(1) == 1 and drum_value < MAX_drum_speed):
            drum_value += delta_drum_speed
        old_joystick_1 = joystick.get_button(1) #updates old value
        #reverse (dump)
        if(old_joystick_2 == joystick.get_button(2)): #if button is the same...
            drum_value = drum_value #do nothing
        elif(joystick.get_button(2) == 1 and drum_value > -MAX_drum_speed):
            drum_value -= delta_drum_speed
        old_joystick_2 = joystick.get_button(2) #updates old value
        #Estop for just the drum (with ramp down)
        if(joystick.get_button(0) == 1): #X button
            if(drum_value > MAX_drum_delta):
                drum_value -= MAX_drum_delta
            elif(drum_value < -MAX_drum_delta):
                drum_value += MAX_drum_delta
            else:
                drum_value = 0

    #E-STOP for everything
        #old_joystick_3 = 0
        if(old_joystick_3 == joystick.get_button(3)): #Triangle button
            Estop = Estop #do nothing
        elif(joystick.get_button(3) == 1):
            if(Estop):
                Estop=0
            else:
                Estop=1
        old_joystick_3 = joystick.get_button(3) #updates old value
        if(Estop): #Triangle button
            shoulder_value = 0
            elbow_value = 0
            left_F_value = 0
            left_B_value = 0
            right_F_value = 0
            right_B_value = 0
            drum_value = 0
        


        #TEMP # FIXME #Solves the issue of random motor firing on start up
        if(time_delay > 0):
            time_delay -= 1
            shoulder_value = 0
            elbow_value = 0
            left_F_value = 0
            left_B_value = 0
            right_F_value = 0
            right_B_value = 0
            drum_value = 0
            

        left_F_value_fake = 0.0 #-----FIXME-----# temp while we wait for parts

        #Sending commands through the UDP Socket -------------
        my_str = json.dumps({"shoulder_value":shoulder_value, "elbow_value":elbow_value, "left_F_value":left_F_value, "left_B_value":left_B_value, "right_F_value":right_F_value, "right_B_value":right_B_value, "drum_value":drum_value})
        MESSAGE = str.encode(my_str)
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        #print("waiting for response")
        data, address = sock.recvfrom(UDP_PORT)

        json_data = data.decode(encoding = "utf-8")
        json_obj = json.loads(json_data, parse_float = Decimal)
       # print("Printing Drum value: ")
        #print (json_obj['drum'])

        real_shoulder_value = json_obj['shoulder_value']
        real_elbow_value = json_obj['elbow_value']
        real_left_F_value = json_obj['left_F_value']
        real_left_B_value = json_obj['left_B_value']
        real_right_F_value = json_obj['right_F_value']
        real_right_B_value = json_obj['right_B_value']
        real_drum_value = json_obj['drum_value']
        
        #print(data)
        #-----------------------------------------------------

        #E-stop satus
        if (Estop):
            textPrint.print_red(screen, "E-STOP: TRUE")
        else:
            textPrint.print_green(screen, "E-STOP: FALSE")
        
        #motor status
        textPrint.print(screen, "Drive Train:")
        textPrint.indent()
        textPrint.print(screen, "Left:")
        textPrint.indent()
        textPrint.print(screen, "Front: {}".format(-real_left_F_value))
        textPrint.print(screen, "Back:  {}".format(-real_left_B_value))
        textPrint.unindent()
        textPrint.print(screen, "Right:")
        textPrint.indent()
        textPrint.print(screen, "Front: {}".format(-real_right_F_value))
        textPrint.print(screen, "Back:  {}".format(-real_right_B_value))
        textPrint.unindent()
        textPrint.unindent()

        #Acctuator status
        textPrint.print(screen, "Arm:")
        textPrint.indent()
        textPrint.print(screen, "shoulder: {}".format(real_shoulder_value))
        textPrint.print(screen, "elbow:     {}".format(real_elbow_value))
        textPrint.unindent()

        #Drum status
        textPrint.print(screen, "Drum:")
        textPrint.indent()
        textPrint.print(screen, "Speed: {}".format(real_drum_value))
        textPrint.unindent()
  
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(50)
    
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
