import threading
import time
from aq import AQ
from guizero import App, Text, PushButton

aq = AQ()

v = aq.firmware()

if v < "1e":
    print("Calibration only available for version 1e and up. Exiting!")
    exit()

def calibrate():
    aq.calibrate_400()

def reset_calibrate():
    aq.reset_calibration()

app = App(title="Raspberry Pi Calibrator", width=300, height=150, layout="grid")
PushButton(app, text="Calibrate", command=calibrate, grid=[0,7])
PushButton(app, text="Factory Reset", command=reset_calibrate, grid=[1,7])

def update_readings():
    while True:
        e_co2 = aq.get_eco2()
        eco2_field.value = str(e_co2)
        time.sleep(0.5)

t1 = threading.Thread(target=update_readings)

Text(app, text="eCO2 (ppm)", grid=[0,0])
eco2_field = Text(app, text="-", grid=[1,0])

Text(app, text="Firmware: " + v, grid=[0,1])
t1.start()
app.display()
