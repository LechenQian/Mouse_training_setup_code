from ScopeFoundry import Measurement
from ScopeFoundry.measurement import MeasurementQThread
from AntCamHW.daq_do.daq_do_dev import DAQSimpleDOTask
from AntCamHW.daq_di.daq_di_dev import DAQSimpleDITask
import time

odor0 = DAQSimpleDOTask('Dev1/port0/line1')
# lick = DAQSimpleDITask('Dev2_SELECT/port1/line0')
odor0.low()
timeout = time.time() + 100

while time.time() < timeout:
    # odor0.high()
    # time.sleep(0.02)
    # odor0.low()
    # time.sleep(5)
    print(lick.read())
    time.sleep(0.2)
lick.close()
# odor0.close()