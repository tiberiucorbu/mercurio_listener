import subprocess
from mercurio.ConfigParam import ConfigParam
from mercurio.Logger import Logger
from datetime import datetime
from serial import Serial, serialutil


class Mercurio():
    
    TIMEOUT = 1
    MERCURIO_CONFIG_NAME = 'mercurio.cfg'
     
    def __init__(self):
        self.log = Logger("mercurio").get() 
        
    def _dict_from_readline(self, line):
        """Creates a dictionary from the raw input from the serial.
        e.g.
    
        target=something
    
        Is transformed into
        { 'target': 'something' }
        """
        self.log.debug('Recieved raw data: %s' % line)
        try:
            items = ''.join(line.splitlines()).split('=', 1)
        except ValueError:
            items = None
            self.log.warn('Error parsing line: %s' % ValueError)
        retVal = []    
        if items and len(items) == 2:
            for item in items:
                retVal.append(item.strip().lower())
            self.log.debug('Parsed dictionary: %s' % retVal)    
            return dict([retVal])
        return {}
    
    
    
    def _prepare_command(self, command):
        """Prepares a single command to be executed by a subprocess"""
        return command.split(' ')
    
    
    def listen(self):
        configuration = ConfigParam(self.MERCURIO_CONFIG_NAME)
        port = configuration.get('general','port')
        if port is None:
            self.log.critical('ERROR: port missing in ``mercurio.cfg`` file. '
                             'Try running ``python -m serial.tools.list_ports``'
                             ' to figure out the port of the device.')
            exit(2)
        
        try:
            serial = Serial(port, 9600, timeout=self.TIMEOUT)
        except serialutil.SerialException:
            self.log.critical('ERROR: Mercurio device '
                             'not connected nor detected.')
            exit(1)
        self.log.info('Mercurio is listening on %s.' % serial.portstr)
        targets = configuration.listItems('targets')
        while True:
            data = self._dict_from_readline(serial.readline())
            if not 'target' in data:
                # Ignore any other output that doesn't have a target
                continue
            destination = data['target'].lower().rstrip()
            if not destination in targets:
                # Inform that we received an unknown target
                self.log.warn("Target %s not found" % destination)
            self.log.info("Instructions received.")
            
            command_args = self._prepare_command(targets[destination])
            self.log.info("Mercurio delivering to target: %s" % destination.title())
            self.log.info(targets[destination])
            # ``subprocess.call`` will wait for the command to complete.
            # no need of blocking the next execution since
            # it won't be available until this is completed
            subprocess.call(command_args)
            
            self.log.info("Mercurio sucessfuly delivered on %s." % datetime.now())
