from socket import *
from time import sleep

ZERO = .025
ONE = .1

port = 31337

s = socket(AF_INET, SOCK_STREAM)
s.bind(("", port))  # ip goes in quotes

s.listen(0)
print("Server is listening...")

c, addr = s.accept()

msg = "Some message...\n"

for i in msg:
    c.send(i.encode())
    sleep(.1)
    
c.send("EOF".encode())
print("Message sent...")
c.close()