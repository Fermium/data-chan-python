import time

from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
time.sleep(0.5)
hallapparatus = ht.HallEffectApparatus()
time.sleep(0.5)
hallapparatus.acquire(0x16d0,0x0c9b)
time.sleep(0.5)
hallapparatus.enable()
time.sleep(0.5)
hallapparatus.set_heater_state(255)
time.sleep(15)
