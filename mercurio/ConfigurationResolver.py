import os
import ConfigParser

'''
Created on Jul 28, 2013

@author: Tiberiu
'''


class ConfigurationResolver:
    def __init__(self, configFile):
        self._readConfigFile(configFile)
        
    def _findRelativeFile(self, filename):
        '''
        Converts relative path to an absolute one, also checks if the file exists, returns None if not
        '''
        config_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(config_path):
            return os.path.abspath(config_path)
        return None


    def _readConfigFile(self, filename):
        '''
        Reads the config file from the current directory
        '''
        filename = self._findRelativeFile(filename)
        if not filename:
            raise ValueError('``', filename, '`` file is missing.')
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(filename))
    
    def _getConfiguration(self):
        return self.config
    
    def get(self, section, option):  
        if (self.config.has_option(section, option)):
            return self.config.get(section, option);
        else: 
            return None
        
    def getBoolean(self, section, option):  
        if (self.config.has_option(section, option)):
            return self.config.getboolean(section, option);
        else: 
            return None
  
  
    def listItems(self, section):
        result = dict([(i[0], i[1]) for i in self.config.items(section)])
        return result
        
    
