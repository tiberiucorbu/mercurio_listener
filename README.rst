Mercurio
========

Mercurio is a set of components to run commands in a host. Also known as the deployment machine. It is designed to be plugglable, so you can run whatever you want to in the host.

The aim of Mercurio is to transmit a message to the host. It is most useful used as a deployment machine.

The other component is the Mercurio box


Mercurio listener
-----------------

Python listener on the serial port that translates the slugs passed into commands in the host machine.


Installation
------------

The installation can be done with the source::


    python setup.py install


Configuration
-------------

The most important value in the configuration is the ``port`` where the ``mercurio box`` is attached.

This can be determined by running, after the ``mercurio listener`` has been installed:

    python -m serial.tools.list_ports

The box by default will only send four possible targets:

* Test - Used to run the tests of the application.
* Development - Used to deploy to the development environment.
* Staging - Used to deploy to the staging environment.
* Production - Used to deploy to the producton environment.

These settings must be expressed in a ``mercurio.cfg`` file, located where the listener is run.

e.g.

    [mercurio]
    # Use python -m serial.tools.list_ports`` to determine it.
    port: /dev/tty.usbserial-A900cfep
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

After that it determines from the confing file what command needs to be run according to the target passed

If you require more complex functionality on your deployment, I suggest you look into fabric.
