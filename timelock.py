# Team: parasauras
# Date: 05/05/2023
# Description: CYEN 301 program 5, implemets a time based code generator (intended for 2fa) using md5sum

import time
import hashlib
import sys



DAYLIGHT_SAVINGS = True    # change if getting the wrong output
CUSTOM_SYSTIME = '2010 06 13 12 55 34'  # if testing a particular system time, change this, otherwise, if using current time, leave blank



def check_valid_epoch_len(epoch):
    
    input_error = False



    if len(epoch) == 6:
        if len(epoch[0]) != 4:
            input_error = True
            
        for i in range(1, 5):
            if len(epoch[i]) != 2:
                input_error = True
    else:
        input_error = True
        
        
    if input_error:
        print("ERROR: Please use the following format:\n\t[YYYY] [MM] [DD] [HH] [mm] [SS]")
        exit()





def check_valid_epoch_maxtime(epoch):

    input_error = False
    max_time_vals = [2023, 12, 31, 23, 59, 59]
    min_time_vals = [1970, 1, 1, 0, 0, 0]



    for i in range(len(epoch)):
        if epoch[i] > max_time_vals[i] or epoch[i] < min_time_vals[i]:
            input_error = True
    

    if input_error:
        print("ERROR: Please provide input in the following ranges:\n\t", end='')
        for i in range(len(max_time_vals)):
            print("[{}-{}]".format(min_time_vals[i], max_time_vals[i]), end='')
        print("\n\t- note do not put more days than there are in a month, this isn't as explicitly checked for")
        exit()




def secs_from_epoch(epoch):
    
    temp_days = 0
    years_since_leap = 0
    epoch_between_dates = 0
    multipliers = [60, 60, 24]  # second | minute | hour
    
    
    
    epoch = epoch.split(" ")
    
    check_valid_epoch_len(epoch)
    
    epoch = [int(i) for i in epoch]

    check_valid_epoch_maxtime(epoch)
    
    years_since_leap = epoch[0] % 4

    # subtract epoch time that will be given by calling time.time()
    epoch[0] -= 1970   # year:     1970
    epoch[1] -= 1      # month:    january
    epoch[2] -= 1      # day:      1st



    # days contributed by year given
    epoch[0] = 366 * ((epoch[0] + 1) // 4) + 365 * (epoch[0] - (epoch[0] + 1) // 4)

    # days contributed by month given
    # i hate the gregorian calendar
    for i in range(epoch[1]):
        if i == 1:  # feb
            if years_since_leap == 0:
                temp_days += 29
            else:
                temp_days += 28
            continue
        
        if (i + i//7) % 2 == 1:  # 31s and 30s reverse at 8th month, but we start at index 0... qwq... ;-;... :(... o_o...
            temp_days += 30
        else:
            temp_days += 31
        
    epoch[1] = temp_days



    for i in range(len(epoch) - 1): # last index already in seconds
        for j in range(len(multipliers) - (i//3 == 1) - (i//4 == 1)):   # yuck
            epoch[i] *= multipliers[j]
            


    for i in range(len(epoch)):
        epoch_between_dates += epoch[i]
        
        
        
    return epoch_between_dates





def generate_code(time_to_hash):
    
    final_code = ''
    
    
    
    time_to_hash = str(time_to_hash).encode('utf-8')
    md5 = hashlib.md5()

    md5.update(time_to_hash)
    time_to_hash = md5.hexdigest().encode('utf-8')

    md5 = hashlib.md5()

    md5.update(time_to_hash)
    time_to_hash = md5.hexdigest()



    # gets final code from hash
    for i in range(len(time_to_hash)):
        if time_to_hash[i].isalpha():
            final_code += time_to_hash[i]

            if len(final_code) == 2:
                break
            
            
    for i in range(len(time_to_hash)-1, 0, -1):
        if time_to_hash[i].isdigit():
            final_code += time_to_hash[i]
            
            if len(final_code) == 4:
                break
            
            
            
    return final_code





def get_time_to_hash(epoch_time):
    
    if len(CUSTOM_SYSTIME) != 0:
        systime = secs_from_epoch(CUSTOM_SYSTIME)
    else:
        systime = time.time()



    time_to_hash = int(systime - epoch_time) // 60 * 60

    if DAYLIGHT_SAVINGS:
        time_to_hash -= 3600
        
    return time_to_hash





# if we don't get an IO redirect or pipe, no need to print
if sys.stdin.isatty():
    print("Epoch Time: ", end='')

epoch = input()

epoch_time = secs_from_epoch(epoch)

time_to_hash = get_time_to_hash(epoch_time)

final_code = generate_code(time_to_hash)

print(final_code)
