from PyQt4.QtCore import QThread, SIGNAL
import time
from multiprocessing import Pool
from sendconfig import configure_device, update_device


class run_configs_thread(QThread):
    def __init__(self, _devices):
        QThread.__init__(self)
        self.devices = _devices

    def __del__(self):
        self.wait()

    def run(self):
        work_list = []
        for device in self.devices:
            cmd = run_config
            args = (device, )      
            work_list.append((cmd, args))
        
        for device_result in p_execute(work_list):
            self.emit(SIGNAL('device_finished'), device_result)

def run_config(device):
        switch, port, do_update, do_config, config_file = device
        if do_update:
            update_device(switch, port, 'isr4300-universalk9.16.03.04.SPA.bin')
        if do_config:
            configure_device(switch, port, config_file)


def _map_worker((func, args)):

    """ Worker function for use with p_execute

        Args:
            tuple(func, args): 
                func (function ptr): function to be executed
                args (tuple): arguments to be passed to func

    """

    result = func(*args)
    return result

def p_execute(work_list):
    
    results = []
    for result in Pool(24).imap_unordered(_map_worker, work_list):
        results.append(result)   
    return results

