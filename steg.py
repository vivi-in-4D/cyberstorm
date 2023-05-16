# team: parasaruas
# date: 05/05/2023
# description: program 7, implements bit and byte stegonography methods using sentinel


import os
import sys


WRAPPER_FILE = ''
HIDDEN_FILE = ''



RIGHT_TO_LEFT = False
USE_OPTIMAL_INTERVAL = False


BIT_MODE = True
STORE_MODE = False
OFFSET = 0  # amt of space beyond header
INTERVAL = 8
sentinel = bytearray([0, 255, 0, 0, 255, 0])    # end of file



def get_data_from_file(file):
    with open(file, 'rb') as f:
        data = f.read()
    
    return data



def store_byte(wrapper, hidden_data, sentinel, INTERVAL, OFFSET):

    hidden_data += sentinel
    for i in range(len(hidden_data)):
        wrapper[OFFSET+i*INTERVAL] = hidden_data[i]
        
    return wrapper



def store_bit(wrapper, hidden_data, sentinel, INTERVAL, OFFSET):
    
    hidden_data += sentinel
    
    i = 0
    while i < len(hidden_data):
        for j in range(8):
            wrapper[OFFSET] &= 0b11111110
            wrapper[OFFSET] |= ((hidden_data[i] & 0b10000000) >> 7)
            hidden_data[i] = (hidden_data[i] << 1) & (2 ** 8 -1)
            OFFSET += INTERVAL

        i += 1

    return wrapper



def extract_byte(wrapper, sentinel, INTERVAL, OFFSET):

    sentinel_index_to_check = 0
    hidden_data = bytearray((len(wrapper) - OFFSET) // INTERVAL + 1)
    i = 0

    while OFFSET < len(wrapper):
        byte = wrapper[OFFSET]

        if byte == sentinel[sentinel_index_to_check]:
            sentinel_index_to_check += 1
        else:
            sentinel_index_to_check = 0

        if sentinel_index_to_check == len(sentinel):
            break

        hidden_data[i] = byte
        OFFSET += INTERVAL
        i += 1



    return hidden_data[:-(len(sentinel)-2)]
        



def extract_bit(wrapper, sentinel, INTERVAL, OFFSET):
    
    sentinel_index_to_check = 0
    hidden_data = bytearray((len(wrapper) - OFFSET) // INTERVAL + 1)
    i = 0

    while OFFSET < len(wrapper):
        byte = 0

        # get byte
        for j in range(8):
            
            try:
                byte |= (wrapper[OFFSET] & 0b00000001)
            except:
                continue
            
            if j < 7:
                byte <<= 1
                OFFSET += INTERVAL

        if byte == sentinel[sentinel_index_to_check]:
            sentinel_index_to_check += 1
        else:
            sentinel_index_to_check = 0

        if sentinel_index_to_check == len(sentinel):
            break

        hidden_data[i] = byte
        OFFSET += INTERVAL
        i += 1

    return hidden_data[:-(len(sentinel))]





# parses command line arguments, changing values accordingly
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i][:2] == '-b':
            BIT_MODE = True
            
        elif sys.argv[i][:2] == '-B':
            BIT_MODE = False
            
        elif sys.argv[i][:2] == '-s':
            STORE_MODE = True
            
        elif sys.argv[i][:2] == '-r':
            STORE_MODE = False
            
        elif sys.argv[i][:2] == '-o':
            OFFSET = int(sys.argv[i][2:])
            
        elif sys.argv[i][:2] == '-i':
            INTERVAL = int(sys.argv[i][2:])
            
        elif sys.argv[i][:2] == '-w':
            WRAPPER_FILE = sys.argv[i][2:]
            
        elif sys.argv[i][:2] == '-h':
            HIDDEN_FILE = sys.argv[i][2:]



input_error = False

if WRAPPER_FILE == '':
    print('ERROR: please provide a wrapper file')
    input_error = True
    
if HIDDEN_FILE == '' and STORE_MODE:
    print('ERROR: please provide a hidden file when using store mode')
    input_error = True
    
# 2 of these checks are performed because the 2 above check for potential issues with creating wrapper
if input_error:
    exit()
    
    

# we need this to check for valid offset and interval
wrapper = bytearray(get_data_from_file(WRAPPER_FILE))



if (RIGHT_TO_LEFT):
    wrapper.reverse()

    
    
if OFFSET < 0 or OFFSET >= len(wrapper):
    print('ERROR: please input a valid offset (range[0-{}])'.format(len(wrapper)))
    input_error = True

if INTERVAL < 0 or INTERVAL >= (len(wrapper) - OFFSET):
    print('ERROR: please input a valid interval (range[0-{}])'.format(len(wrapper) - OFFSET))
    input_error = True
    
if input_error:
    exit()



if STORE_MODE:
    hidden_data = bytearray(get_data_from_file(HIDDEN_FILE))


    if USE_OPTIMAL_INTERVAL:
        INTERVAL = (os.path.getsize(WRAPPER_FILE) - OFFSET) / (os.path.getsize(HIDDEN_FILE) + len(sentinel))

    if BIT_MODE:
        wrapper = store_bit(wrapper, hidden_data, sentinel, INTERVAL, OFFSET)
    else:
        wrapper = store_byte(wrapper, hidden_data, sentinel, INTERVAL, OFFSET)

    
    wrapper.reverse()
    
    
    sys.stdout.buffer.write(wrapper)



else:
    if BIT_MODE:
        hidden_data = extract_bit(wrapper, sentinel, INTERVAL, OFFSET)
    else:
        hidden_data = extract_byte(wrapper, sentinel, INTERVAL, OFFSET)

    
    sys.stdout.buffer.write(hidden_data)