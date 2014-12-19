Reddcoin-Interest-Tracker
=========================

A simple Python script to notify of interest generation from Raspberry-Pi based staking Reddcoin wallets

This script is designed to be run from root CRON on a Raspberry Pie to track and notify the user of Reddcoin stake events. 
It maintains a file in the /tmp directory on the RPi that records the current amount of interest generated, when this 
amount is found to have changed (aka a wallet stake event has matured) it pulses the GPIO 18 pin (I have a cheap 3.3v piezo 
speaker attached on this pin) and sends an e-mail to the specified recipient.


Note for .wav users: 

Audio quality on the RPi is less than stellar however running this command in the console seems to help:

* amixer set PCM -- 1000

Changelog
---------

19/12/2014

+ Added WAV file playing functionality at the request of artiscience :) (system still toggles the GPIO 18 pin for any attached piezo speakers)
+ Moved to a config driven system (got tired of editing the code file to remove my passwords!)
+ Layout changes to the code to make it more readable
+ Added e-mail error reporting
+ Added better exception reporting for command errors
+ Updated code base to new Python version compliance

**Script requires the following libraries to run correctly**

Bitcoinrpc
----------

https://github.com/jgarzik/python-bitcoinrpc

* cd ~/Downloads
* wget https://github.com/jgarzik/python-bitcoinrpc/archive/master.zip
* unzip master.zip
* cd python-bitcoinrpc-master
* sudo python setup.py install

(big thanks to jgarzik et.al for his excellent RPC lib)

RPi.GPIO
--------

* wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
* tar zxf RPi.GPIO-0.1.0.tar.gz
* cd RPi.GPIO-0.1.0
* sudo python setup.py install

The script's other included function allows you to unlock the wallet for staking in the first place. This avoids you having 
to flush your terminal history every time you re-launch reddcoind. If unlock is successful then the command should return
'None' - go figure...

Config file
-----------

The script now checks a config file to pick up the user settings for passwords / email settings 

**uReddRpc.log**

The location of this config file must be specified when launching the script as an argument:

**Usage: python uReddrpc.py [rpc_command] [config file path]**

See below for examples - there is now no need to alter the python file itself :)

The script contains print statements so you will need to pipe the output in cron to a log file or null to avoid a cron e-mail
**** storm every time the script runs

Example wallet unlock:
---------------------

* python /home/pi/uReddrpc.py unlockforstaking /home/pi/uReddRpc.conf
* Enter wallet passphrase: ##########
* None
* $

(None = success, anything else = failure)

Example get staking info
------------------------

* python /home/pi/uReddRpc.py getstakinginfo /home/pi/uReddRpc.conf

Returns the JSON information about your current staking status

Example root crontab:
---------------------

\* * * * * python /home/pi/uReddRpc.py getinterest /home/pi/uReddRpc.conf >> /home/pi/uReddRpc.log

(under root cron so we have access to the GPIO pins)

Example terminal launch:
------------------------

* sudo python /home/pi/uReddrpc.py getinterest /home/pi/uReddRpc.conf
