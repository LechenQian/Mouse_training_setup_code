'''
Created on Mar 26, 2018

@author: Hao Wu
'''
from ScopeFoundry import BaseMicroscopeApp

class AntCamApp(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'Selina_Contingency'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    def setup(self):
        
        #Add App wide settings
        
        #Add hardware components
        print("Adding Hardware Components")
        from AntCamHW.flircam.flircam_hw import FLIRCamHW
        wide_cam = FLIRCamHW(self)
        wide_cam.settings.camera_sn.update_value('14273815')
        wide_cam.name = 'wide_cam'
        self.add_hardware(wide_cam)
        
        from AntCamHW.flircam.flirrec_hw import FLIRRecHW
        self.add_hardware(FLIRRecHW(self))
        
        #self.add_hardware(DAQTimerHW(self))

        #Add measurement components
        
        #from AntCamMS.nune_training_2P_5odor import NuneTraining
        #self.add_measurement(NuneTraining(self))
        
        
        #from AntCamMS.nune_training_2P_noodors import NuneTraining
        #self.add_measurement(NuneTraining(self))
        
        #from AntCamMS.spencer_pretraining import NuneTraining
        #self.add_measurement(NuneTraining(self))
        
        from AntCamMS.Selina_Contingency import SelinaTraining
        self.add_measurement(SelinaTraining(self))
        
#         from AntCamMS.nune_training_2P_odor_sound_second_half_sated import NuneTraining
#         self.add_measurement(NuneTraining(self))
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()
    

if __name__ == '__main__':
    import sys
    
    app = AntCamApp(sys.argv)
    
    app.hardware['wide_cam'].connected.update_value(True)
    app.hardware['flirrec'].connected.update_value(True)
    #app.hardware['daq_timer'].connected.update_value(True)
    
    sys.exit(app.exec_())
    
    