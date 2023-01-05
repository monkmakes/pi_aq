import threading
import time
from aq import AQ
from guizero import App, Text, PushButton, CheckBox, Slider, TextBox

aq = AQ()

v = aq.firmware()

def calibrate():
    aq.calibrate_400()

def reset_calibrate():
    aq.reset_calibration()

app = App(title="Raspberry Pi AQ Tester", width=300, height=300, layout="grid")
PushButton(app, text="Calibrate", command=calibrate, grid=[0,7])
PushButton(app, text="Factory Reset", command=reset_calibrate, grid=[1,7])


def checkbox_changed():
    if checkbox.value == 1:
        aq.leds_manual()
    else:
        aq.leds_automatic()

def update_readings():
    while True:
        temp = aq.get_temp()
        e_co2 = aq.get_eco2()
        raw = aq.get_raw()
        temp_c_field.value = str(temp)
        eco2_field.value = str(e_co2)
        raw_field.value = str(raw)
        time.sleep(0.5)

t1 = threading.Thread(target=update_readings)

def slider_changed(slider_value):
    aq.set_led_level(slider_value)

def buzzer_on():
    aq.buzzer_on()

def buzzer_off():
    aq.buzzer_off()

Text(app, text="Temp (C)", grid=[0,0] )
temp_c_field = Text(app, text="-", grid=[1,0])

Text(app, text="eCO2 (ppm)", grid=[0,1])
eco2_field = Text(app, text="-", grid=[1,1])

Text(app, text="VOC (raw)", grid=[0,2])
raw_field = Text(app, text="-", grid=[1,2])

checkbox = CheckBox(app, text="LEDs Manual", command=checkbox_changed, grid=[0,3])

Text(app, text="LED Level", grid=[0,4])
slider = Slider(app, start=0, end=6, command=slider_changed, grid=[1,4])

PushButton(app, text="Buzzer on", command=buzzer_on, grid=[0,5])
PushButton(app, text="Buzzer off", command=buzzer_off, grid=[1,5])

Text(app, text="Firmware: " + v, grid=[0,6])
t1.start()
app.display()
