Reddcoin-Interest-Tracker
=========================

A simple Python script to notify of interest generation from Raspberry-Pi based staking Reddcoin wallets

This script is designed to be run from root CRON on a Raspberry Pie to track and notify the user of Reddcoin stake events. 
It maintains a file in the /tmp directory on the RPi that records the current amount of interest generated, when this 
amount is found to have changed (aka a wallet stake event has matured) it pulses the GPIO 18 pin (I have a cheap 3.3v piezo 
speaker attached on this pin) and sends an e-mail to the specified recipient.

Script requires the following libraries to run correctly

Bitcoinrpc (Thanks to jgarzik et.al for his excellent RPC lib)
----------

https://github.com/jgarzik/python-bitcoinrpc

RPi.GPIO
--------

wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
tar zxf RPi.GPIO-0.1.0.tar.gz
cd RPi.GPIO-0.1.0
sudo python setup.py install

The script's other included function allows you to unlock the wallet for staking in the first place. This avoids you having 
to flush your terminal history every time you re-launch reddcoind. If unlock is successful then the command should return
'None' - go figure...

The script contains print statements so you will need to pipe the output in cron to a log file or null to avoid a cron e-mail
**** storm every time the script runs

Example root crontab: (root so we have access to the GPIO pins)
---------------------

* * * * * python /home/pi/uReddrpc.py getinterest >> /home/pi/uReddrpc.log

Example terminal launch:
------------------------

sudo python /home/pi/uReddrpc.py getinterest
