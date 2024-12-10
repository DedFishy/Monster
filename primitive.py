import socket

UDP_IP = "192.168.1.41"
UDP_PORT = 64000
MESSAGE_LEN = 25
#with open("specimen.raw", "rb") as raw:
#    MESSAGE = raw.read()

def int_to_hex(num):
    string = hex(num)
    string = string[2:] # remove 0x
    if len(string) < 2: # if only one digit is present
        string = "0" + string
    return string

def construct_led_packet(object: str):
    packet = ""
    packet += "02"
    packet += "01" if object["on"] else "00"
    packet += "00" if object["use_chroma"] else "01"
    packet += int_to_hex(object["r"])
    packet += int_to_hex(object["g"])
    packet += int_to_hex(object["b"])
    packet += int_to_hex(object["brightness"])
    packet += int_to_hex(object["chroma_zone"])
    packet += "4143303030573033363234383631390000"
    return bytes.fromhex(packet)

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
    
MESSAGE = bytes.fromhex(input("HEX code >"))
print("Message len:", len(MESSAGE))

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message: *specimen.raw*")

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
print("Listening for response...")
returned = sock.recv(MESSAGE_LEN)

with open("returned.raw", "wb+") as out:
    out.write(returned)
    
sock.close()