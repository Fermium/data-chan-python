import halltester as ht

ht.init()
scan = ht.acquire(0x16d0,0x0c9b)
ht.enable(scan)
ht.set_current_lockin(scan,0.5)
ht.set_heater_state(scan,200)
ht.reset_device(scan)
ht.pop_measure(scan)
