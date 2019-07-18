from ScopeFoundry import Measurement
from ScopeFoundry.measurement import MeasurementQThread
from AntCamHW.daq_do.daq_do_dev import DAQSimpleDOTask
from AntCamHW.daq_di.daq_di_dev import DAQSimpleDITask
import time
import cv2

# this test roughly consumes 5 ml water
water = DAQSimpleDOTask('Dev1/port0/line0')

timeout = time.time() + 50

while time.time() < timeout:
    water.high()
    time.sleep(5)
    water.low()
    time.sleep(1)

    # key = cv2.waitKey(2000)
    # if key == 27:  # exit on ESC
    #     break


water.close()


# from ScopeFoundry import Measurement
# from ScopeFoundry.measurement import MeasurementQThread
# from AntCamHW.daq_do.daq_do_dev import DAQSimpleDOTask
# from AntCamHW.daq_di.daq_di_dev import DAQSimpleDITask
# import time
#
#
# lick = DAQSimpleDITask('Dev2_SELECT/port1/line0')
#
# timeout = time.time() + 100
#
# while time.time() < timeout:
#     odor0.high()
#     time.sleep(0.5)
#     odor0.low()
#     time.sleep(2)
#     print(lick.read())
#     time.sleep(0.2)
# lick.close()
