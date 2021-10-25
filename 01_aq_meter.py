import threading
import time
from guizero import App, Text
from aq import AQ

aq = AQ()

app = App(title="Air Quality", width=550, height=300, layout="grid")

def update_readings(): # update fields with new temp and eCO2 readings
    while True:
        temp_c_field.value = str(aq.get_temp())
        eco2_field.value = str(aq.get_eco2())
        time.sleep(0.5)

t1 = threading.Thread(target=update_readings)

aq.leds_automatic()

# define the user interface
Text(app, text="Temp (C)", grid=[0,0], size=20)
temp_c_field = Text(app, text="-", grid=[1,0], size=100)
Text(app, text="eCO2 (ppm)", grid=[0,1], size=20)
eco2_field = Text(app, text="-", grid=[1,1], size=100)
t1.start() # start the thread that updates the readings
app.display()
