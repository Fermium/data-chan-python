import time
import signal
import sys
import itertools
from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht


time.sleep(0.5)

hallapparatus = ht.HallEffectApparatus()
# acquire(VID,PID)
hallapparatus.acquire(0x16d0,0x0c9b)

time.sleep(0.5)
# Software power-on
hallapparatus.enable()

time.sleep(0.5)

# Burn, burn. burrrrrn!
hallapparatus.set_heater_state(255)

# Close when pressing CTRL+C
def signal_handler(signal, frame):
        hallapparatus.disconnect_device()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


for i in itertools.count():    
    meas = hallapparatus.pop_measure()
    if meas is not None:
        print("Running for the", i, "nth time")
        print(str(meas).replace(", ", ",\n"))
    if i % 10 is 0:
        print("Setting heater state!")
        hallapparatus.set_heater_state(255)
    time.sleep(0.1)
    
#hallapparatus.shutdown_device()
