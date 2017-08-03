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
################################################################################
#importing package for r
import numpy
import rpy2.robjects as robj
r = robj.r
#aliasing r funcions for faster usage
summary = r['summary']
coef = r['coef']
attach = r['attach']
read_csv = r['read.csv']
deviance = r['deviance']
dfres = r['df.residual']

#importing ggplot2 for plots, if doesn't exist donwload it and then import it
try:
    import rpy2.robjects.lib.ggplot2 as ggplot2
except ImportError:
    utils = robj.packages.importr('utils')
    utils.install_packages('ggplot2')
    import rpy2.robjects.lib.ggplot2 as ggplot2
#grdevices to plot to file
grdevices = robj.packages.importr('grDevices')

#loading and attaching 'output.csv' to model on that
robj.globalenv['data'] = read_csv('./output.csv')
data = robj.globalenv['data']
attach(data)

#first model, ch3=a+b*raw_current_code
model1 = r.lm('ch3~raw_current_code')
check1 = False
if(r['pf'](summary(model1)[9][0],summary(model1)[9][1],summary(model1)[9][2],lower_tail=False)<=0.005):
    check1=True
ch3vsraw = coef(model)
ch3vsraw[0] #intercept
ch3vsraw[1] #slope
grdevices.png(file='./plots/ch3vsraw.png',width=512,height=512)
gp = ggplot2.ggplot(data)
pp = gp + \
    ggplot2.aes_string(x='raw_current_code',y='ch3')+\
    ggplot2.geom_abline(intercept=ch3vsraw[0],slope=ch3vsraw[1],color='red')+\
    ggplot2.geom_line()+\
    ggplot2.ggtitle('Ch3 vs Raw Current')
pp.plot()
grdevices.dev_off()
#plot for visual check, red line is the fitting line and black is the data

#second model, raw_current_code=a'+b' * ch3
model2 = r.lm('raw_current_code~ch3') # like the other model data here is in a straight line
check2 = False
if(r['pf'](summary(model2)[9][0],summary(model2)[9][1],summary(model2)[9][2],lower_tail=False)<=0.005):
    check2=True
rawvsch3 = coef(model2)
rawvsch3[0]#intercept
rawvsch3[1]#slope
grdevices.png(file='./plots/rawvsch3.png',width=512,height=512)
gp = ggplot2.ggplot(data)
pp = gp + \
    ggplot2.aes_string(y='raw_current_code',x='ch3')+\
    ggplot2.geom_abline(intercept=rawvsch3[0],slope=rawvsch3[1],color='red')+\
    ggplot2.geom_line()+\
    ggplot2.ggtitle('Raw Current vs Ch3')
pp.plot()
grdevices.dev_off()
#plot for visual check, red line is the fitting line and black is the data

################################################################################
