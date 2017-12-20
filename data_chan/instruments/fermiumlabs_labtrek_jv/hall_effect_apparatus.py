import data_chan
import struct

class HallEffectApparatus:

    def __init__(self):
        self.dchan = data_chan.Datachan()
        """Initialize data-chan"""
        self.dchan.dl.datachan_init()

    def acquire(self,vid,pid):
        """acquires a device given USB VID and PID"""

        self.scan = self.dchan.dl.datachan_device_acquire(vid,pid)

        if self.scan.result is 0xFF:
            return self.scan

        elif self.scan.result is 0x04:
            class DataChanDeviceUknownError(Exception):
                pass
            raise DataChanDeviceUknownError("Data-chan acquire returned 0x04, meaning the device is uknown")

        elif self.scan.result is 0x03:
            raise MemoryError("Data-chan acquire returned 0x03, meaning it failed to malloc()")

        elif self.scan is 0x02:
            class DataChanDeviceCannotClaimError(Exception):
                pass
            raise DataChanDeviceCannotClaimError("Data-chan acquire returned 0x02, meaning it could not claim the device, but found it")

        elif self.scan.result is 0x01:
            class DataChanDeviceNotFoundOrInaccessibleError(Exception):
                pass
            raise DataChanDeviceNotFoundOrInaccessibleError("Data-chan acquire returned 0x01, meaning it did not found the device of given VID/PID. Could also be a permission problem on Unix/Linux ")

        elif self.scan.result is 0x00:
            class DataChanUninitializedError(Exception):
                pass
            raise DataChanUninitializedError("Data-chan was not initialized.")
        else:
            class DataChanUknownError(Exception):
                pass
            raise DataChanUknownError("Data chan returned an uknown code") 
        


    def enable(self):
        """enable measurements in the data-chan device"""
        return self.dchan.dl.datachan_device_enable(self.scan.device)

    def queue_size(self):
        """returns the number of measures in the host queue, ready to be popped"""
        return self.dchan.dl.datachan_device_enqueued_measures(self.scan.device)

    def pop_measure(self):
        """pop and returns one measure"""
        d = None
        if(queue_size()):
            measure = dchan.datachan_device_dequeue_measure(self.scan.device)
            if(measure != ffi.NULL):
                d = { 'ch'+str(measure.channels[i]) : measure.values[i] for i in range(len(measure.channels)) }
                d['time']=measure.time*1000+measure.millis
                self.dchan.dl.datachan_clean_measure(measure)
        return d

    def set_current_lockin(self,current):
        """set the current generator in lock-in (AC) mode given the absolute value of a current"""
        d = struct.pack('ff'*1, *[a-float(current)/b,a+float(current)/b])
        self.dchan.dl.datachan_send_async_command(self.scan.device,0x01,d,len(d))

    def set_current_fixed(self,current):
        """set the current generator in CC mode given a current"""
        d = struct.pack('f'*1, *[float(current)])
        self.dchan.dl.datachan_send_async_command(self.scan.device,0x02,d,len(d))

    def set_current_raw(self,current):
        """set the current generator in CC mode given the raw DAC value. To be used only for testing"""
        d = struct.pack('H'*1, *[int(current)])
        self.dchan.dl.datachan_send_async_command(self.scan.device,0x03,d,len(d))

    def set_heater_state(self,power):
        """set the heater given an input value from 0 to 255"""
        if int(power) < 0 or int(power) > 255:
            raise ValueError("The heater power needs to be between 0 and 255")
        d = struct.pack('B'*1, *[power])
        self.dchan.dl.datachan_send_async_command(self.scan.device,0x04,d,len(d))

    def set_channel_gain(self,channel,gain):
        """set the gain for the specified channel"""
        d = struct.pack('BB', channel,int(gain)) 
        self.dchan.dl.datachan_send_async_command(self.scan.device,0x05,d,len(d))
        
    def reset_device(self):
        """reset the device"""
        d = struct.pack('B'*1, *[0])
        self.dchan.dl.datachan_send_async_command(self.device,0x06,d,len(d))

    def disconnect_device(self):
        """disconnect the device and releases it from data-chan's usb control"""
        self.dchan.dl.datachan_device_release(self.scan.device)

    def shutdown_device(self):
        """soft device shutdown"""
        self.dchan.dl.datachan_shutdown()
