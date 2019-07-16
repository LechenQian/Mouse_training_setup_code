from ScopeFoundry import Measurement
from ScopeFoundry.measurement import MeasurementQThread
from AntCamHW.daq_do.daq_do_dev import DAQSimpleDOTask
from AntCamHW.daq_di.daq_di_dev import DAQSimpleDITask
import time


class OdorGen(object):
    def __init__(self,odorindex):
        self.odorindex = odorindex
        self.odors_DAQ = []


    def assign_odor(self):
    # initiate all the odor solenoids

        for item in self.odorindex:

            self.odors_DAQ.append(DAQSimpleDOTask('Dev2_SELECT/port0/line{}'.format(item)))
        print('Odor {} has been properly assigned'.format(self.odorindex))


    def set_rewardodor(self,index):
        reward_odor = self.odors_DAQ[index]
        print('reward odor is odor {}'.format(index))
        return reward_odor


    def initiate(self):
        for odor in self.odors_DAQ:
            odor.low()
        print('Odor initiation: status low')
    def close(self):
        for odor in self.odors_DAQ:
            odor.close()
        print('Connection has been closed')


odors_cue = OdorGen([0, 1, 2, 3])
odors_cue.assign_odor()
reward_odor = odors_cue.set_rewardodor(index=0)
odors_cue.initiate()
odors_cue.close()
events_filename = 'sssss.d.sd..s'

