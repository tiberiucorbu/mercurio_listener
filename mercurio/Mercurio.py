import subprocess
from mercurio.ConfigurationResolver import ConfigurationResolver
from mercurio.LoggerFactory import LoggerFactory
from datetime import datetime
from serial import Serial, serialutil


class Mercurio():
    
    TARGET = 'target'
    TEMPERATURE = 'temperature'
    BUTTON = 'button'
    CHAINED_TOUCHES = 'chainedtouches'
    
    LISTEN_TARGETS = [TARGET, TEMPERATURE, BUTTON, CHAINED_TOUCHES]
    
    
    TIMEOUT = 1
    CONFIG_FILE = 'etc/setup.cfg'
     
    def __init__(self):
        self.log = LoggerFactory().get() 
        
    def _dictionareFromReadline(self, line):
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
    
    
    
    def _prepareCommand(self, command):
        """Prepares a single command to be executed by a subprocess"""
        return command.split(' ')
    
    

    def _connectToDevice(self, port):
        try:
            serial = Serial(port, 9600, timeout=self.TIMEOUT)
        except serialutil.SerialException:
            self.log.critical('ERROR: Mercurio device not connected nor detected.')
            exit(1)
        self.log.info('Mercurio is listening on %s.' % serial.portstr)
        return serial


    def _checkPort(self, port):
        if port is None:
            self.log.critical('ERROR: port missing in ``%s`` file. '
                'Try running ``python -m serial.tools.list_ports``'
                ' to figure out the port of the device.' % self.CONFIG_FILE)
            exit(2)


    def runCommand(self, command):
        command_args = self._prepareCommand(command)
        self.log.info(command)
        # ``subprocess.call`` will wait for the command to complete.
        # no need of blocking the next execution since
        # it won't be available until this is completed
        subprocess.call(command_args)
        self.log.info("Mercurio sucessfuly delivered on %s." % datetime.now())

    def listen(self):
        configuration = ConfigurationResolver(self.CONFIG_FILE)
        port = configuration.get('general','port')
        self._checkPort(port)
        serial = self._connectToDevice(port)
        targets = configuration.listItems('targets')
        while True:
            data = self._dictionareFromReadline(serial.readline())
            if not self.TARGET in data:
                self.log.debug("Ignore recieved data %s any other output that doesn't have a target" % data)
                continue
            destination = data['target'].lower().rstrip()
            if not destination in targets:
                # Inform that we received an unknown target
                self.log.warn("Target %s not found" % destination)
            self.log.info("Instructions received: %s" % destination) 
            self.runCommand(targets[destination])
