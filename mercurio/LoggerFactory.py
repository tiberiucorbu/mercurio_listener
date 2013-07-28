import os
import logging 
from mercurio.ConfigurationResolver import ConfigurationResolver 


'''
Created on Jul 28, 2013

@author: Tiberiu
'''


class LoggerFactory():
    
    LOG_CONFIGURATION_FILE='etc/logging.cfg'
    FILESYS = 'filesystem'
    LOGGING_DIR = 'loggingDir'
    
    def __init__(self, name):
        config = ConfigurationResolver(self.LOG_CONFIGURATION_FILE)
        name = name.replace('.log','')
        logger = logging.getLogger('log_namespace.%s' % name)    # log_namespace can be replaced with your namespace 
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(config.get(self.FILESYS,self.LOGGING_DIR), '%s.log' % name)    # usually I keep the LOGGING_DIR defined in some global settings file
            consoleHandler = logging.StreamHandler()
            fileHandler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(filename)s - %(module)s %(funcName)s %(message)s')
            consoleHandler.setLevel(logging.DEBUG)
            consoleHandler.setFormatter(formatter)
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(logging.DEBUG)
            logger.addHandler(fileHandler)
            logger.addHandler(consoleHandler)
        self._logger = logger

    def get(self):
        return self._logger