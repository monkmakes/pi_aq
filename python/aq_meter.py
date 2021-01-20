import serial
import threading
import time
from guizero import App, Text, PushButton, CheckBox, Slider, TextBox
from aq import AQ

app = App(title="Air Quality", width=500, height=300, layout="grid")
aq = AQ()

def update_readings():
    while True:
        temp_c_field.value = str(aq.get_temp())
        eco2_field.value = str(aq.get_eco2())
        time.sleep(0.5)

t1 = threading.Thread(target=update_readings)
t1.start()

aq.leds_automatic()

Text(app, text="Temp (C)", grid=[0,0], size=20)
temp_c_field = Text(app, text="-", grid=[1,0], size=100)
Text(app, text="eCO2 (ppm)", grid=[0,1], size=20)
eco2_field = Text(app, text="-", grid=[1,1], size=100)
app.display()
