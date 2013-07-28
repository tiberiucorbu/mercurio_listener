import os
import ConfigParser

'''
Created on Jul 28, 2013

@author: Tiberiu
'''


class ConfigParam:
    def __init__(self, configFile):
        self._readConfigFile(configFile)
        
    def _findRelativeFile(self, filename):
        config_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(config_path):
            return os.path.abspath(config_path)
        return None


    def _readConfigFile(self,filename):
        """Reads the config file from the current directory"""
        filename = self._findRelativeFile(filename)
        if not filename:
            raise ValueError('``',filename,'`` file is missing.')
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(filename))
    
    def _getConfiguration(self):
        return self.config
    
    def get(self, section, option):  
        return self.config.get(section, option);
  
    def listItems(self, section):
        result = dict([(i[0], i[1]) for i in self.config.items(section)])
        return result