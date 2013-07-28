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
    



    def __init__(self, name="mercurio"):
        self.config = ConfigurationResolver(self.LOG_CONFIGURATION_FILE)
        name = name.replace('.log','')
        logger = logging.getLogger('log_namespace.%s' % name)    # log_namespace can be replaced with your namespace 
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(filename)s - %(module)s %(funcName)s %(message)s')
            if self.config.getBoolean('handlers', 'console'):
                self.addConsoleHandler(logger, formatter)
            if self.config.getBoolean('handlers', 'file'):
                self.addFileHandler(name, logger, formatter)
            
        self._logger = logger
    

    def getLoggerLevel(self):
        return logging._levelNames.get(self.config.get('prop', 'logLevel'))

    def addConsoleHandler(self, logger, formatter):
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(self.getLoggerLevel())
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)


    def addFileHandler(self, name, logger, formatter):
        file_name = os.path.join(self.config.get(self.FILESYS, self.LOGGING_DIR), '%s.log' % name)
        fileHandler = logging.FileHandler(file_name)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(self.getLoggerLevel())
        logger.addHandler(fileHandler)
    
    def get(self):
        return self._logger