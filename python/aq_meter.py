import serial
import threading
import time
from guizero import App, Text, PushButton, CheckBox, Slider, TextBox

temp = 0
e_co2 = 0
ser = serial.Serial("/dev/ttyS0", 9600)

def clear_console():
    console.value = ""

app = App(title="Air Quality", width=500, height=300, layout="grid")

def send(message):
    ser.write(bytes(message+"\n", 'utf-8'))

def wait_for_message():
    global temp, e_co2
    time.sleep(0.1) # give attiny time to respond
    incoming_message = str(ser.readline()[:-2].decode("utf-8"))  # remove LF, CR turn into string
    message_parts = incoming_message.split("=")
    if len(message_parts) == 2:
        code, value = message_parts
        if code == "t":
            temp = float(value)
        elif code == "c":
            e_co2 = float(value)

def update_readings():
    while True:
        send("t")
        wait_for_message()
        time.sleep(0.1) # give attiny time to respond
        send("c")
        wait_for_message()
        time.sleep(1)
        temp_c_field.value = str(temp)
        eco2_field.value = str(e_co2)

t1 = threading.Thread(target=update_readings)
t1.start()

send("a")

Text(app, text="Temp (C)", grid=[0,0], size=20)
temp_c_field = Text(app, text="-", grid=[1,0], size=100)
Text(app, text="eCO2 (ppm)", grid=[0,1], size=20)
eco2_field = Text(app, text="-", grid=[1,1], size=100)
app.display()
