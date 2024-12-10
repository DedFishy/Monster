import socket
import math
import time
import colorsys
from winvolume import get_value

UDP_IP = "239.255.255.250"
UDP_PORT = 57254
MESSAGE_LEN = 19
#with open("specimen.raw", "rb") as raw:
#    MESSAGE = raw.read()

def int_to_hex(num):
    string = hex(num)
    string = string[2:] # remove 0x
    if len(string) < 2: # if only one digit is present
        string = "0" + string
    return string



data = {
    "on": True,
    "r": 255,
    "g": 255,
    "b": 255,
    "brightness": 100,
    "use_chroma": False,
    "chroma_zone": 0
}

with open("specimen.raw", "rb") as specimen:
    MESSAGE = specimen.read()
    
#MESSAGE = bytes.fromhex(input("HEX code >"))
print("Message len:", len(MESSAGE))

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message: *specimen.raw*")

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM,
             socket.IPPROTO_UDP) # UDP
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, \
         socket.inet_aton("192.168.1.30"))

colors = [
    "ff0000",
    "ffff00"
    "00ff00",
    "00ffff"
    "0000ff",
    "ff00ff"
]

try:
    while True:
        color_tuple = colorsys.hsv_to_rgb(0, 0, get_value())
        color = "".join([int_to_hex(int(x * 255) % 256) for x in color_tuple])
        print(color)
        sock.sendto(bytes.fromhex("03006dca" + (color * 5)), (UDP_IP, UDP_PORT))
        #time.sleep(0.05)
except KeyboardInterrupt: pass

exit()

print("Listening for response...")
returned = sock.recv(MESSAGE_LEN)

with open("returned.raw", "wb+") as out:
    out.write(returned)
    
sock.close()