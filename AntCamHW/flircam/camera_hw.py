'''
Created on Aug 9, 2017
@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from AntCamHW.flircam.camera_dev import CameraDev

class CameraHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='camera'

    def setup(self, camera_id=0):
        self.settings.New(name='camera_id',dtype=int, initial=camera_id,ro=False)
        #self.settings.New(name='file_name',dtype=str, initial= 'C:\Users\MurthyLab\Test.avi' ,ro=True)
                
    def connect(self):

        self.dev = CameraDev(self.settings.camera_id.value)
        
    def read(self):
        return self._dev.read()
    
    def write(self):
        self._dev.write()
    
    def open_file(self):
        self._dev.open_file(self.settings.file_name.value())
    
    def close_file(self):
        self._dev.close_file()
        
    def disconnect(self):
        try:
            self._dev.close()
            del self._dev
            
        except AttributeError:
            pass
        
if __name__ == '__main__':
    ai=DAQaiHW()
    ai.connect()
    print(ai._data)
    time.sleep(1)
    ai.disconnect()
