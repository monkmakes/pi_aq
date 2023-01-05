import serial
import serial.tools.list_ports
import threading
import time
from guizero import App, Text, PushButton, CheckBox, Slider, TextBox

temp = 0
e_co2 = 0
ser = serial.Serial("/dev/serial0", 9600)

def clear_console():
    console.value = ""

app = App(title="Raspberry Pi AQ", layout="grid")
console = TextBox(app, width=40, height=15, scrollbar=True, multiline=True, grid=[0, 6, 2, 1])
log_checkbox = CheckBox(app, text="Log", grid=[0,5])
PushButton(app, text="Clear Console", command=clear_console, grid=[1,5])

def log(message):
    if log_checkbox.value:
        console.value += message

def send(message):
    log(">"+message)
    ser.write(bytes(message+"\n", 'utf-8'))

def wait_for_message():
    global temp, e_co2
    time.sleep(0.1) # give attiny time to respond
    t0=time.monotonic()
    incoming_message = str(ser.readline()[:-2].decode("utf-8"))  # remove LF, CR turn into string
#    print("incoming_message: " + incoming_message)
    t1=time.monotonic()
#    print(t1-t0)
    log("<" + incoming_message)
    message_parts = incoming_message.split("=")
    if len(message_parts) == 2:
        code, value = message_parts
        if code == "t":
            temp = float(value)
        elif code == "c":
            e_co2 = float(value)

def checkbox_changed():
    if checkbox.value == 1:
        send("m")
        #ser.write(b"m\n")
    else:
        ser.write(b"a\n")

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

def slider_changed(slider_value):
    send(str(slider_value))

def buzzer_on():
    send("b")

def buzzer_off():
    send("q")

log("Start")

Text(app, text="Temp (C)", grid=[0,0], )
temp_c_field = Text(app, text="-", grid=[1,0])
Text(app, text="eCO2 (ppm)", grid=[0,1])
eco2_field = Text(app, text="-", grid=[1,1])
checkbox = CheckBox(app, text="LEDs Manual", command=checkbox_changed, grid=[0,2])
Text(app, text="LED Level", grid=[0,3])
slider = Slider(app, start=0, end=6, command=slider_changed, grid=[1,3])
PushButton(app, text="Buzzer on", command=buzzer_on, grid=[0,4])
PushButton(app, text="Buzzer off", command=buzzer_off, grid=[1,4])
t1.start()
app.display()
