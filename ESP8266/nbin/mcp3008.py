#Simple driver for MCP3008

from machine import Pin

class MCP3008:
    def __init__(self, clk=14, mosi=13, miso=12, cs=15):
        self._clk = Pin(clk, Pin.OUT)
        self._mosi = Pin(mosi, Pin.OUT)
        self._miso = Pin(miso, Pin.IN)
        self._cs = Pin(cs, Pin.OUT)

    def read(self, channel):
        # """ Reads an analog value from the given channel (0-7) and returns it. """
        if channel not in range(0, 8):
            raise ValueError("channel must be 0-7")

        self._cs(1)  # negative edge
        self._cs(0)
        self._clk(0)

        send_cmd = channel
        send_cmd |= 0b00011000  # 0x18 (start bit + single/ended)

        # send bits (only 5 bits considered)
        for i in range(5):
            self._mosi(bool(send_cmd & 0x10))  # check bit on index 4
            self._clk(1)  # negative edge
            self._clk(0)
            send_cmd <<= 1

        # receive value from MCP
        v = 0
        for i in range(11):
            self._clk(1)  # negative edge
            self._clk(0)
            v <<= 1
            if self._miso():
                v |= 0x01

        return v

    def getCurrent(self, channel):
        #read = self.read(channel)
        A = (self.read(channel) -511.5)/20.46 #resolution
        return A
    
    def get_U(self):
        u = 150/41,6 #150w nominal / 41,6Ah/d nominal - diferencial
        return u


    