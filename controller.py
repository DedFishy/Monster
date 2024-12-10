import socket

import time

def int_to_hex(num):
    string = hex(num)
    string = string[2:] # remove 0x
    if len(string) < 2: # if only one digit is present
        string = "0" + string
    return string

def hex_to_int(hex):
    num = int(hex, 16)
    return num

def default_if_none(value, default):
    return default if value is None else value

def wrap_rgb(rgb):
    return rgb % 256

data = {
    "on": True,
    "r": 255,
    "g": 255,
    "b": 255,
    "brightness": 100,
    "use_chroma": False,
    "chroma_zone": 0,
    "type": "write"
}

class Timeout(Exception): pass

class StripController:
    query = "0100834317CE"
    identifier = "4143303030573033363234383631390000"
    message_size = 25
    
    _configuration = {
        "on": False,
        "r": 0,
        "g": 0,
        "b": 0,
        "brightness": 0,
        "use_chroma": False,
        "chroma_zone": 0
    }
    
    def __init__(self, ip, port=64000):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM # Use UDP
        )
        self.socket.settimeout(5) 
        try:
            self.send_packet(bytes.fromhex(self.query + self.identifier))
            ping = self.socket.recv(self.message_size)
            self.read_response(ping)
        except socket.timeout:
            raise Timeout("Connection to light strip timed out")
            
    def get_configuration(self):
        return self._configuration
    
    def set_configuration(self,
                          on = None,
                          use_chroma = None,
                          r = None,
                          g = None,
                          b = None,
                          brightness = None,
                          chroma_zone = None):
        self.send_packet(
            self.construct_led_packet(
                {
                    "on": default_if_none(on, self._configuration["on"]),
                    "use_chroma": default_if_none(use_chroma, self._configuration["use_chroma"]),
                    "r": default_if_none(r, self._configuration["r"]),
                    "g": default_if_none(g, self._configuration["g"]),
                    "b": default_if_none(b, self._configuration["b"]),
                    "brightness": default_if_none(brightness, self._configuration["brightness"]),
                    "chroma_zone": default_if_none(chroma_zone, self._configuration["chroma_zone"])
                }
            )
        )
        try:
            self.read_response(self.socket.recv(self.message_size))
            print("Read response; ready for next")
        except socket.timeout:
            raise Timeout("Light strip update response timed out")
            
    def read_response(self, response: bytes):
        hex_response = response.hex(":").split(":")
        self._configuration["on"] = hex_to_int(hex_response[1])
        self._configuration["use_chroma"] = hex_response[2] == "00"
        self._configuration["r"] = hex_to_int(hex_response[3])
        self._configuration["g"] = hex_to_int(hex_response[4])
        self._configuration["b"] = hex_to_int(hex_response[5])
        self._configuration["brightness"] = hex_to_int(hex_response[6])
        self._configuration["chroma_zone"] = hex_to_int(hex_response[7])
    
    def send_packet(self, packet: bytes):
        
        self.socket.sendto(packet, (self.ip, self.port))
    
    def construct_led_packet(self, object, packet_type = "write"):
        print(object)
        packet = ""
        
        if packet_type == "write":
            packet += "02"
        elif packet_type == "read":
            packet += "01"
        elif packet_type == "reply":
            packet += "00"
            
        packet += "01" if object["on"] else "00"
        
        packet += "00" if object["use_chroma"] else "01"
        
        
        packet += int_to_hex(object["r"])
        packet += int_to_hex(object["g"])
        packet += int_to_hex(object["b"])
        
        packet += int_to_hex(object["brightness"])
        
        packet += int_to_hex(object["chroma_zone"])
        
        packet += self.identifier
        return bytes.fromhex(packet)
    
    def close(self):
        self.socket.close()
        
if __name__ == "__main__":
    controller = StripController("192.168.1.41")
    print(controller.get_configuration())
    
    values = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ]
    
    try:
        while True:
            for value in values:
                controller.set_configuration(r=value[0], g=value[1], b=value[2])
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    controller.close()