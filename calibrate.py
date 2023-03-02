import time
from aq import AQ

aq = AQ()
print("Calibrate sensor")
print("================")
print("Only for Air Quaility for Raspbewrry Pi boards of version 1e and later")
while True:
    print("Options")
    print("1. Show eCO2 reading")
    print("2. Calibrate to 400 ppm")
    print("3. Reset to factory default")
    print("4. Quit")
    option = input(">")
    if (option == '1') :
        print("Current eCO2 reading: " + str(aq.get_eco2()))
    if (option == '2') :
        print("Your sensor should be in an environment with around 400ppm CO2 (fresh air)")
        confirm = input("Calibrate? (Y/N)")
        if (confirm == 'Y' or confirm == 'y'):
            aq.calibrate_400()
            time.sleep(2)
            print('Sensor calibrated')
        else:
            print('Cancelled calibration')
    elif (option == '3') :
        confirm = input("Reset calibration to factory default? (Y/N)")
        if (confirm == 'Y' or confirm == 'y'):
            aq.reset_calibration()
            time.sleep(2)
            print('Sensor set to factory default')
        else:
            print('Cancelled calibration')
    elif (option == '4') :
        print("Bye")
        break
    else:
        print('unknown option')

