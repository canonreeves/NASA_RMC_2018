import pygame
#import PyCmdMessenger
import socket
import json
from decimal import Decimal
import time

#Socket connection Info
#UDP_IP = "192.168.1.254"
UDP_IP = "192.168.1.252"
UDP_PORT = 1113

print("connected")

count = 0

#initalize variavles
shoulder_value = 0.0
elbow_value = 0.0 
left_F_value = 0.0
left_B_value = 0.0
right_F_value = 0.0
right_B_value = 0.0
drum_value = 0.0

#other variables
#wheels
MAX_speed = 1000    #max speed for the wheels out of 1000
delta_speed = 1.0/5.0 * MAX_speed #wheels maximum speed change
#drum
MAX_drum_speed = 1000   #max speed for the drum out of 1000
MAX_drum_delta = 100   #max (safe) E-Stop speed
delta_drum_speed = 100 #speed incrament by button press
old_joystick_1 = 0 #drum speed up
old_joystick_2 = 0 #drum slow down
#TEMP #FIXME #Solves the issue of random motor firing on start up
time_delay = 0 # number of ticks to skipp on start up
#E-stop
old_joystick_3 = 0
Estop = 1 #Estop status (True/ False)
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
print("joysticks initialized")
    
# Get ready to print
textPrint = TextPrint()

print("at main loop")
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        pygame.event.clear()
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    #print("counted joysticks")
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
        if (joystick.get_button(4) == 1):
            shoulder_value -= 1000
        
            
    #Elbow:
        elbow_value = 0
        if (joystick.get_axis(2) <= -0.9):
            elbow_value += 1000
        if (joystick.get_button(5) == 1):
            elbow_value -= 1000
        
            
    #Left motor:
        #Front:
        #if speed change is > than 'delta_speed'...
        axis_1 = joystick.get_axis(1)
        if(abs(left_F_value-axis_1 * MAX_speed) >= delta_speed):
            #if negative delta
            if(left_F_value < axis_1 * MAX_speed):
                left_F_value += delta_speed
            #if positive delta
            elif(left_F_value > axis_1 * MAX_speed):
                left_F_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            left_F_value = axis_1 *MAX_speed
        #Back:
        #if speed change is > than 'delta_speed'...
        if(abs(left_B_value-axis_1 *MAX_speed) >= delta_speed):
            #if negative delta
            if(left_B_value < axis_1 *MAX_speed):
                left_B_value += delta_speed
            #if positive delta
            elif(left_B_value > axis_1 *MAX_speed):
                left_B_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            left_B_value = axis_1 *MAX_speed

    #Right motor:
        #Front:
        axis_3 = joystick.get_axis(3)

        #if speed change is > than 'delta_speed'...
        if(abs(right_F_value-axis_3 * MAX_speed) >= delta_speed):
            #if negative delta
            if(right_F_value < axis_3 * MAX_speed):
                right_F_value += delta_speed
            #if positive delta
            elif(right_F_value > axis_3 * MAX_speed):
                right_F_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            right_F_value = axis_3 * MAX_speed
        #Back:
        #if speed change is > than 'delta_speed'...
        if(abs(right_B_value-axis_3 * MAX_speed) >= delta_speed):
            #if negative delta
            if(right_B_value < axis_3 *MAX_speed):
                right_B_value += delta_speed
            #if positive delta
            elif(right_B_value > axis_3 *MAX_speed):
                right_B_value -= delta_speed
        else: #if speed change is < than 'delta_speed'...
            right_B_value = axis_3 * MAX_speed

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
        #print("motor stuf happened")
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
        my_str = json.dumps({"shoulder_value":shoulder_value,
                             "elbow_value":elbow_value,
                             "left_F_value":left_F_value,
                             "left_B_value":left_B_value,
                             "right_F_value":right_F_value,
                             "right_B_value":right_B_value,
                             "drum_value":drum_value})
        MESSAGE = str.encode(my_str)
        #print("connecting to socket")
        count = count + 1
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(.3)
        """other_count, address = sock.recvfrom(UDP_PORT)
        #print("received response")
        other_count = int.from_bytes(other_count, byteorder = 'big')
        diff = count - int(other_count)
        print(diff)
        if(abs(diff) > 1):
            time.sleep(.11 * diff)"""
            
        #print( count - other_count)
        print(count)
        if(count > 600):
            print("Exiting to prevent horrible latency")
            pygame.quit()
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
        textPrint.print(screen, "Front: {}".format(-left_F_value))
        textPrint.print(screen, "Back:  {}".format(-left_B_value))
        textPrint.unindent()
        textPrint.print(screen, "Right:")
        textPrint.indent()
        textPrint.print(screen, "Front: {}".format(-right_F_value))
        textPrint.print(screen, "Back:  {}".format(-right_B_value))
        textPrint.unindent()
        textPrint.unindent()

        #Acctuator status
        textPrint.print(screen, "Arm:")
        textPrint.indent()
        textPrint.print(screen, "shoulder: {}".format(shoulder_value))
        textPrint.print(screen, "elbow:     {}".format(elbow_value))
        textPrint.unindent()

        #Drum status
        textPrint.print(screen, "Drum:")
        textPrint.indent()
        textPrint.print(screen, "Speed: {}".format(drum_value))
        textPrint.unindent()

        pygame.event.clear()
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
   # print("updated display")
    # Limit to 20 frames per second
    clock.tick(5)
   # print("clearing events")
    
  #  print("events have been cleared")
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
