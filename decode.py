###############################
# Group: Parasaurus
# Class: CSC 442/542-CYEN 301
# Date: 24 March 2023
###############################

import sys

# Read binary message from stdin
message = sys.stdin.read().strip()

# Convert binary to ASCII
def decode(message):
    #checks if binary length is divisible by 7 or 8
    if len(message) % 7 == 0:
        ascii = []
        #converts each segment to ascii
        for i in range(0, len(message), 7):
            segment = message[i:i+7]
            #converts using base 2
            ascii.append(chr(int(segment, 2)))
        return ascii
    elif len(message) % 8 == 0:
        ascii = []
        for i in range(0, len(message), 8):
            segment = message[i:i+8]
            ascii.append(chr(int(segment, 2)))
        return ascii
    else:
        #fixes error if value is not divisible by 7 or 8
        raise ValueError("Invalid")

# Output decoded message to stdout
print("".join(decode(message)))
