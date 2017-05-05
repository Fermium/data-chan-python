from cffi import FFI

ffi = FFI()
ffi.cdef("""
typedef struct {
	uint8_t type;
	uint8_t mu;
    uint8_t measuresNum;
	uint8_t channels[8];
	float values[8];
	uint32_t time;
	uint16_t millis;
} measure_t;
 typedef enum {
     uninitialized 				= 0x00,
     not_found_or_inaccessible	= 0x01,
     cannot_claim				= 0x02,
     malloc_fail				= 0x03,
     unknown					= 0x04,
     success					= 0xFF,
 } search_result_t;

 typedef struct {
     search_result_t result;
     void* device;
 } datachan_acquire_result_t;

 bool datachan_is_initialized(void);
 void datachan_init(void);
 void datachan_shutdown(void);
 datachan_acquire_result_t datachan_device_acquire(void);
 void datachan_device_release(void* dev);
 bool datachan_device_enable(void* dev);
 bool datachan_device_is_enabled(void* dev);
 bool datachan_device_disable(void* dev);
 void datachan_send_sync_command(void* dev, uint8_t cmdType, uint8_t* cmdBuf, uint8_t cmdBufLength);
 void datachan_send_async_command(void* dev, uint8_t cmdType, uint8_t* cmdBuf, uint8_t cmdBufLength);
 measure_t* datachan_device_dequeue_measure(void* dev);
 int32_t datachan_device_enqueued_measures(void*);
 void datachan_clean_measure(measure_t* measure);
 void datachan_device_set_config(void*, uint32_t, uint8_t, void*, uint16_t);
""")

dc = ffi.dlopen('./libDataChan.so')
################################################################################
dc.datachan_init()
scan = dc.datachan_device_acquire()
if(scan.result==0xFF):
    print("yeah")
else :
    print("nope")
