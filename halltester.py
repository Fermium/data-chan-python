from datachan import init_lib
import struct
from cffi import FFI
dchan = init_lib()
ffi = FFI()
a = 0.008019432
b = 0.9397528
def init():
    return dchan.datachan_init()

def acquire(vid,pid):
    return dchan.datachan_device_acquire(vid,pid)

def acquire_and_test():
    scan = acquire()
    return {'result':scan.result==0xFF, 'scan':scan}

def enable(scan):
    if(scan.result==0xFF):
        return dchan.datachan_device_enable(scan.device)
def queue_size(scan):
    return dchan.datachan_device_enqueued_measures(scan.device)

def pop_measure(scan):
    d = None
    if(queue_size(scan)):
        measure = dchan.datachan_device_dequeue_measure(scan.device)
        if(measure != ffi.NULL):
            d = { 'ch'+str(measure.channels[i]) : measure.values[i] for i in range(len(measure.channels)) }
            d['time']=measure.time*1000+measure.millis
            dchan.datachan_clean_measure(measure)
    return d

def set_current_lockin(scan,current):
    d = struct.pack('ff'*1, *[a-current/b,a+current/b])
    dchan.datachan_send_async_command(scan.device,0x01,d,len(d))
def set_current_fixed(scan,current):
    d = struct.pack('f'*1, *[current])
    dchan.datachan_send_async_command(scan.device,0x02,d,len(d))

def set_current_raw(scan,current):
    d = struct.pack('B'*1, *[current])
    dchan.datachan_send_async_command(scan.device,0x03,d,len(d))

def set_heater_state(scan,power):
    d = struct.pack('B'*len([power]), *[power])
    dchan.datachan_send_async_command(scan.device,0x04,d,len(d))

def set_channel_gain(scan,channel,gain):
    d = struct.pack('BB'*1, *[channel,gain])
    dchan.datachan_send_async_command(scan.device,0x05,d,len(d))

def reset_device(scan):
    d = struct.pack('B'*len([0]), *[0])
    dchan.datachan_send_async_command(scan.device,0x06,d,len(d))
