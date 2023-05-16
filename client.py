# Group: parasauras
# Date: 4/19/23
# Description: cyen301 program 4, implements a chat server that recieves a covert message in binary using the time it takes between each characters arrival



import socket
from sys import stdout
from time import time


TIMING_CUTOFF = .05
binary_message = ""
delta_array = []
message = ""


# enables debugging output
DEBUG = False


# set the server's IP address and port
ip = "138.47.99.64"
port = 31337


# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# connect to the server
s.connect((ip, port))


# receive data until EOF
data = s.recv(4096).decode()
while (data.rstrip("\n") != "EOF"):
	# output the data
	stdout.write(data)
	stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096).decode()
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	delta_array.append(delta)
	if (DEBUG):
		stdout.write(" {}\n".format(delta))
		stdout.flush()
 
 
print("\n\n")
  
for i in range(len(delta_array)):
    print(delta_array[i] + " ", end='')
    
print("\n\n")
 

for i in range(0, len(delta_array)):
	if (delta_array[i] < TIMING_CUTOFF):
		binary_message += '0'
	else:
		binary_message += '1'
  
print(binary_message)   

for i in range(0, len(binary_message), 8):
	message += chr(int(binary_message[i:i+8], 2))
   

print("/n" + message + "/n/n")

message = message.split("EOF")[0]

print("message after EOF:\n" + message)


# close the connection to the server
s.close()