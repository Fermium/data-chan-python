import halltester as ht
from time import sleep
ht.init()

scan = ht.acquire(0x16d0,0x0c9b)

ht.enable(scan)



ht.set_current_lockin(scan,0.5)
ht.set_current_fixed(scan, 0.05)


ht.set_heater_state(scan,200)
ht.reset_device(scan)

ht.pop_measure(scan)


measures = {}

for i in range (int(4095/2-500), int(4095/2+500)):
    ht.set_current_raw(scan,i)
    #pop all old measures
    while(ht.pop_measure(scan) != None ):
        pass
    sleep(0.150)
    measures[i] = ht.pop_measure(scan)
    if measures[i] is not None:
        measures[i]["raw_current_code"] = i

measures

import csv
outfile = open("output.csv", "w")

fieldnames = ["raw_current_code", "ch1", "ch2", "ch3", "ch5", "ch6", "ch7"]
csvwriter = csv.DictWriter(outfile, fieldnames=fieldnames,extrasaction='ignore')
csvwriter.writeheader()



for measure in measures:
    if measures[measure] is not None:
        csvwriter.writerow(measures[measure])
import rpy2.robjects
