import time
from aq import AQ

aq = AQ()
aq.leds_automatic()

interval = int(input("Enter interval between readings (seconds):"))
file_name = input("Enter filename:")
f = open(file_name, "w")

last_update = 0
t0 = int(time.monotonic())

while True:
    now = time.monotonic()
    if (now > last_update + interval):
        last_update = now
        t = str(int(now) - t0)
        temp_c = str(aq.get_temp())
        eco2 = str(int(aq.get_eco2()))
        f.write(t + "\t")
        f.write(temp_c + "\t")
        f.write(eco2 + "\n")
        print(t + "\t" + temp_c + "\t" + str(int(eco2)))
