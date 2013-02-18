import os
import ConfigParser
import subprocess

from datetime import datetime
from serial import Serial, serialutil
from clint.textui import puts, colored

TIMEOUT = 1
MERCURIO_CONFIG_NAME = 'mercurio.cfg'


def _dict_from_readline(line):
    """Creates a dictionary from the raw input from the serial.
    e.g.

    target=something

    Is transformed into
    { 'target': 'something' }
    """
    try:
        items = ''.join(line.splitlines()).split('=', 1)
    except ValueError:
        items = None
    if items and len(items) == 2:
        return dict([items])
    return {}


def _find_relative_file(filename):
    config_path = os.path.join(os.getcwd(), MERCURIO_CONFIG_NAME)
    if os.path.exists(config_path):
        return os.path.abspath(config_path)
    return None


def _read_config_file():
    """Reads the config file from the current directory"""
    filename = _find_relative_file(MERCURIO_CONFIG_NAME)
    if not filename:
        raise ValueError('``mercurio.cfg`` file is missing.')
    config = ConfigParser.ConfigParser()
    config.readfp(open(filename))
    config_dict = {
        'port': config.get('general', 'port'),
        'targets': dict([(i[0], i[1]) for i in config.items('targets')]),
    }
    return config_dict


def _prepare_command(command):
    """Prepares a single command to be executed by a subprocess"""
    return command.split(' ')


def listen():
    config = _read_config_file()
    if not 'port' in config or not config['port']:
        puts(colored.red('ERROR: port missing in ``mercurio.cfg`` file. '
                         'Try running ``python -m serial.tools.list_ports``'
                         ' to figure out the port of the device.'))
        exit(0)
    port = config['port']
    try:
        serial = Serial(port, 9600, timeout=TIMEOUT)
    except serialutil.SerialException:
        puts(colored.red('ERROR: Mercurio device '
                         'not connected nor detected.'))
        exit(0)
    puts(colored.yellow('Mercurio is listening on %s.' % serial.portstr))
    while True:
        data = _dict_from_readline(serial.readline())
        if not 'target' in data:
            # Ignore any other output that doesn't have a target
            continue
        destination = data['target'].lower().rstrip()
        if not destination in config['targets']:
            # Inform that we received an unknown target
            puts(colored.red("Target %s not found" % destination))
        puts(colored.yellow("Instructions received."))
        targets = config['targets']
        command_args = _prepare_command(targets[destination])
        puts(colored.yellow("Mercurio delivering to target:"
                            " %s" % destination.title()))
        puts(colored.green(targets[destination]))
        puts('-' * 60)
        # ``subprocess.call`` will wait for the command to complete.
        # no need of blocking the next execution since
        # it won't be available until this is completed
        subprocess.call(command_args)
        puts('-' * 60)
        puts(colored.yellow("Mercurio sucessfuly delivered on"
                            " %s." % datetime.now()))
