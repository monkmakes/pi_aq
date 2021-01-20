import serial
import serial.tools.list_ports
import threading
import time
from guizero import App, Text, PushButton, CheckBox, Slider

temp = 0
e_co2 = 0
ser = serial.Serial("/dev/ttyS0", 9600)

def wait_for_message():
    global temp, e_co2
    time.sleep(0.1) # give attiny time to respond
    t0=time.monotonic()
    incoming_message = str(ser.readline()[:-2].decode("utf-8"))  # remove LF, CR turn into string
#    print("incoming_message: " + incoming_message)
    t1=time.monotonic()
    print(t1-t0)
    message_parts = incoming_message.split("=")
    if len(message_parts) == 2:
        code, value = message_parts
        if code == "t":
            temp = float(value)
        elif code == "c":
            e_co2 = float(value)

def checkbox_changed():
    if checkbox.value == 1:
        ser.write(b"m\n")
    else:
        ser.write(b"a\n")

def update_readings():
    while True:
        ser.write(b"t\n")
        wait_for_message()
        time.sleep(0.1) # give attiny time to respond
        ser.write(b"c\n")
        wait_for_message()
        time.sleep(1)
        temp_c_field.value = str(temp)
        eco2_field.value = str(e_co2)

t1 = threading.Thread(target=update_readings)
t1.start()

def slider_changed(slider_value):
    arr = bytes(str(slider_value)+"\n", 'utf-8')
    ser.write(arr)

def buzzer_on():
    ser.write(b"b\n")

def buzzer_off():
    ser.write(b"q\n")

app = App(title="Raspberry Pi AQ", layout="grid")
Text(app, text="Temp (C)", grid=[0,0], )
temp_c_field = Text(app, text="-", grid=[1,0])
Text(app, text="eCO2 (ppm)", grid=[0,1])
eco2_field = Text(app, text="-", grid=[1,1])
checkbox = CheckBox(app, text="LEDs Manual", command=checkbox_changed, grid=[0,2
])
Text(app, text="LED Level", grid=[0,3])
slider = Slider(app, start=0, end=6, command=slider_changed, grid=[1,3])
PushButton(app, text="Buzzer on", command=buzzer_on, grid=[0,4])
PushButton(app, text="Buzzer off", command=buzzer_off, grid=[1,4])

app.display()
