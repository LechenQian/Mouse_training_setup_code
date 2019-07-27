import PyDAQmx as nidaq
from matplotlib import pyplot
import numpy as np
import time

t = nidaq.Task()
t.CreateAIVoltageChan("Dev1/ai1", None, nidaq.DAQmx_Val_Diff, 0, 1, nidaq.DAQmx_Val_Volts, None)
t.CfgSampClkTiming("", 1000, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, 5000)
t.StartTask()
timeout = time.time() + 100
pyplot.figure()
while time.time() < timeout:
    data = np.zeros((1,), dtype=np.float64)
    read = nidaq.int32()
    analog = t.ReadAnalogF64(1, 5, nidaq.DAQmx_Val_GroupByChannel, data, len(data), nidaq.byref(read), None)
    pyplot.scatter(time.time(),analog)
pyplot.show()


