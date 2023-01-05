import serial
import threading
import time

class AQ:
    """A Class for the MonkMakes Air Quality Board for Raspberry Pi"""

    temp = 0
    eco2 = 0
    raw = 0
    version = ""
    ser = None
    delay_period = 0.1

    def __init__(self):
         self.ser = serial.Serial("/dev/serial0", 9600)

    def get_eco2(self):
        self.send("c")
        self._wait_for_message()
        return self.eco2

    def get_temp(self):
        self.send("t")
        self._wait_for_message()
        return self.temp

    def leds_manual(self):
        self.send("m")

    def leds_automatic(self):
        self.send("a")

    def calibrate_400(self):
        self.send("k")

    def reset_calibration(self):
        self.send("K")

    def set_led_level(self, slider_value):
        self.send(str(slider_value))

    def buzzer_on(self):
        self.send("b")

    def buzzer_off(self):
        self.send("q")

    def firmware(self):
        self.send("v")
        self._wait_for_message()
        return self.version

    def get_raw(self):
        self.send("r")
        self._wait_for_message()
        return self.raw

    def send(self, message):
        self.ser.write(bytes(message+"\n", 'utf-8'))
        time.sleep(self.delay_period)

    def _wait_for_message(self):
        time.sleep(self.delay_period) # give attiny time to respond
        incoming_message = str(self.ser.readline()[:-2].decode("utf-8"))  # remove LF, CR turn into string
        message_parts = incoming_message.split("=")
        if len(message_parts) == 2:
            code, value = message_parts
            if code == "t":
                self.temp = float(value)
            elif code == "c":
                self.eco2 = float(value)
                if self.eco2 < 0:
                    self.eco2 = 0
            elif code == "r":
                self.raw = float(value)
            elif code == "Firmware version":
                self.version = value
        


