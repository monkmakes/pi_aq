import threading
import time
from guizero import App, Text, Slider
from aq import AQ

aq = AQ()

app = App(title="Air Quality", width=550, height=400, layout="grid")

def update_readings(): # update fields with new temp and eCO2 readings
    while True:
        temp_c_field.value = str(aq.get_temp())
        eco2 = aq.get_eco2()
        eco2_field.value = str(eco2)
        if eco2 > slider.value:
            app.bg = "red"
            app.text_color = "white"
            aq.buzzer_on()
        else:
            app.bg = "white"
            app.text_color = "black"
            aq.buzzer_off()  
        time.sleep(0.5)

t1 = threading.Thread(target=update_readings)

aq.leds_automatic()

# define the user interface
Text(app, text="Temp (C)", grid=[0,0], size=20)
temp_c_field = Text(app, text="-", grid=[1,0], size=100)
Text(app, text="eCO2 (ppm)", grid=[0,1], size=20)
eco2_field = Text(app, text="-", grid=[1,1], size=100)
Text(app, text="Alarm (ppm)", grid=[0,2], size=20)
slider = Slider(app, start=300, end=2000, width=300, height=40, grid=[1,2])
t1.start() # start the thread that updates the readings
app.display()
