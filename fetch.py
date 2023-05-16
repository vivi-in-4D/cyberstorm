# group: parasauras
# date: 3/31/23
# description: program 3, gets file permissions from an ftp server, then converts them into an ascii string


from ftplib import FTP

# FTP server details
IP = "138.47.136.89"
PORT = 21
USER = "ianmalcolm"
PASSWORD = "jurassicpark"
FOLDER = "/files/10/"
USE_PASSIVE = True # set to False if the connection times out\


if FOLDER == "/files/7/":
    METHOD = 7
else:
    METHOD = 10


# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()

message = ""    # final converted message
temp_file_perms = ""    # use to store the file perms for each file
binary_message = "" # final message in binary, before we convert

# converts file perms into a binary string
for i in range(len(files)):
    
    # removes noise from 7 bit binary
    if int(files[i].split(" ")[0][:10-METHOD] != "---") and (METHOD == 7):
        continue
        
    
    temp_file_perms = files[i].split(" ")[0][10-METHOD:]
    
    for c in range(len(temp_file_perms)):
        if temp_file_perms[c] == '-':
            binary_message += '0'
        else:
            binary_message += '1'

    
# converts binary to ascii
for i in range(0, len(binary_message), 7):
    message += chr(int(binary_message[i:i+7], 2))



# display the folder contents
print(message)