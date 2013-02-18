Mercurio
========

Mercurio is a set of components designed to run commands in a host. Also known as the deployment machine. It is designed to be pluggable, so you can run arbitrary commands in the host.

The aim of Mercurio is to transmit a message to the host. The other component required to do this is the Mercurio box.


Mercurio Listener
-----------------

Python listener on the serial port that translates the slugs passed into commands in the host machine.


Installation
------------

The installation can be done with the source::


    python setup.py install


Configuration
-------------

The most important value in the configuration is the ``port`` where the ``mercurio box`` is attached.

This can be determined by running, after the ``mercurio listener`` has been installed::

    python -m serial.tools.list_ports

The box by default will only send four possible targets:

* ``Test`` - Used to run the tests of the application.
* ``Staging`` - Used to deploy to the staging environment.
* ``Production`` - Used to deploy to the producton environment.

These settings must be expressed in a ``mercurio.cfg`` file, located where the listener is run.

e.g.::

    [general]
    # Use python -m serial.tools.list_ports`` to determine it.
    port: /dev/tty.usbserial-A900cfep
    [targets]
    # Command to be run when this destination is targeted.
    test : ls
    development: ls
    staging: ls
    production: fab production deploy

Please note that at the moment the functionality of the host scripts that it can run is limited, at the moment it only runs a single command.


Start the listener
------------------

The listener can be run with the following command::


    $ mercurio-run.py


It will show some output once the instruction has been received and the command is being executed.


Behind the scenes
-----------------

The listener expects the target to be passed in the following form::

    target=production

After that it determines from the config file what command needs to be run according to the target passed
