from aq import AQ

aq = AQ()
print("Calibrate sensor")
print("================")
print("Only for Air Quaility for Raspbewrry Pi boards of version 1e and later")
print("Options")
print("1. Calibrate to 400 ppm")
print("2. Reset to factory default")
option = input(">")
if (option == '1') :
    print("Your sensor should be in an environment with around 400ppm CO2 (fresh air)")
    confirm = input("Calibrate? (Y/N)")
    if (confirm == 'Y' or confirm == 'y'):
        aq.calibrate_400()
        print('Sensor calibrated')
    else:
        print('Cancelled calibration')
elif (option == '2') :
    confirm = input("Reset calibration to factory default? (Y/N)")
    if (confirm == 'Y' or confirm == 'y'):
        aq.reset_calibration()
        print('Sensor set to factory default')
    else:
        print('Cancelled calibration')
else:
    print('unknown option')

aq.leds_automatic()
