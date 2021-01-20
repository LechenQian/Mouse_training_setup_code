from ScopeFoundry import Measurement
from ScopeFoundry.measurement import MeasurementQThread
from AntCamHW.daq_do.daq_do_dev import DAQSimpleDOTask
from AntCamHW.daq_di.daq_di_dev import DAQSimpleDITask
import time
class OdorGen(object):
    def __init__(self,odorindex):
        self.odorindex = odorindex



    def assign_odor(self):
    # initiate all the odor solenoids



        self.odors_DAQ = DAQSimpleDOTask('Dev2_SELECT/port0/line{}'.format(self.odorindex))
        print('Odor {} has been properly assigned'.format(self.odorindex))


    def set_rewardodor(self,index):
        reward_odor = self.odors_DAQ[index]
        print('reward odor is odor {}'.format(index))
        return reward_odor


    def initiate(self):
        self.odors_DAQ.low()

        print('Odor initiation: status low')
    def close(self):
        self.odors_DAQ.close()

        print('Connection has been closed')




print('a ha')

odors_cue = OdorGen(0)
odors_cue.assign_odor()
# reward_odor = odors_cue.set_rewardodor(index=0)
odors_cue.initiate()
# odors_cue.odors_DAQ[i]
odors_cue.close()
print('odor done')
