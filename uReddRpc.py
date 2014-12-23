#!/usr/bin/env python

from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoinrpc.authproxy import JSONRPCException
import RPi.GPIO as GPIO
import datetime
import smtplib
import time
import pygame
import os
import sys
import getpass

# Load the config file
def loadConfigFile(file_path):

    if os.path.isfile(file_path):
        
        conf_file = open(file_path, "r")
        global config_lines        
        config_lines = conf_file.read().strip().split('\n')
        conf_file.close()
        
    else:
        
        print("Config file not found!")
        sys.exit(0)

    return

# Get a setting from the config
def getSetting(setting):

    for item in config_lines:

        if item != "":
            
            if item.strip().startswith(setting):
                
                pair = item.split('=')
                pair[1] = pair[1].strip()
                return pair[1].strip('"')

    return ""

# Send an e-mail to specified address
def sendemail(message):
               
    if getSetting("email_to_addr") != "":

        header  = 'From: ' + getSetting("email_from_addr") + "\n"
        header += 'To: ' + getSetting("email_to_addr") + "\n"
        header += 'Subject: ' + getSetting("email_subject") + datetime.datetime.now().strftime(" %H:%M:%S") + "\n\n"
        message = header + message

        server = smtplib.SMTP(getSetting("email_smtp_server"))
        server.starttls()
        server.login(getSetting("email_login"),getSetting("email_password"))
        problems = server.sendmail(getSetting("email_from_addr"), getSetting("email_to_addr"), message)
        server.quit()
        
        if len(problems) <= 3:
             print("Email sent to " + str(getSetting("email_to_addr")))
        else:
            print("Error: '" + str(problems) + "'")

    return

#Beep the GPIO speaker    
def beepGpioSpeaker():
    
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, True)
    time.sleep(0.1)
    GPIO.output(12, False)
    time.sleep(0.05)
    GPIO.output(12, True)
    time.sleep(0.1)
    GPIO.output(12, False)
    
    return

#Play the specified .wav file
def playWavFile():
    
    pygame.mixer.init(48000, -16, 1, 4096)
    pygame.mixer.music.load(getSetting("wav_file_location"))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
   
    return
    
def main():

    if len(sys.argv) != 3:
        print("\nUsage: python uReddrpc.py [rpc_command] [config file path]\n")
        sys.exit()
    
    loadConfigFile(sys.argv[2])   

    if getSetting("rpcaddress") == "":
	print("No RPC address specified!")
	sys.exit(1)

    if getSetting("rpcport") == "":
        print("No RPC port specified!")
        sys.exit(1)

    access = AuthServiceProxy("http://"+getSetting("rpcuser")+":"+getSetting("rpcpass") + "@" + getSetting("rpcaddress") + ":" + getSetting("rpcport"))
    
    #print("http://"+getSetting("rpcuser")+ ":" + getSetting("rpcpass") + "@" + getSetting("rpcaddress") + ":" + getSetting("rpcport"))
    
    cmd = sys.argv[1].lower()

    if cmd == "getinterest":

        try:
    
            current_interest = access.getinterest()
            print("Total interest received: " + str(current_interest) + " rdd")
    
            fname = "/tmp/my_interest.log"
    
            if os.path.isfile(fname):
    
                fh = open(fname,"r+")
                file_contents = float(fh.read())
    
                if float(file_contents) != float(current_interest):
                    
                    print("Last interest ammount was " + str(file_contents) + "\nCurrent interest ammount is " + str(current_interest))
    
                    new_total = float(current_interest) - float(file_contents)
    
                    print("New stake event totalling " + str(new_total) + " coins")
    
                    beepGpioSpeaker()
                    
                    if getSetting("wav_file_location") != "":                    
                        playWavFile()
    
                    fh.seek(0)
                    fh.write(str(current_interest))
                    fh.close()
    
                    sendemail(message = "New stake event totalling " + str(new_total) + " coins")
           
            else:
    
                print("File not found, creating " + fname)
                fh = open(fname,"w")
                fh.write(str(current_interest))
                fh.close()
    
        except Exception as e:
            print("Error: " + str(e))
    
    elif cmd == "unlockforstaking":
    
        try:
    
            pwd = getpass.getpass(prompt="Enter wallet passphrase: ")
            print(access.walletpassphrase(pwd, 9999999, True))
    
        except JSONRPCException as e:
            print("JSONRPCException: ({0})".format(e.error))
    
    elif cmd == "getstakinginfo":
        
        try:
            print(access.getstakinginfo())
        except Exception as e:
            print("Error: " + str(e))
    
    else:
        print("Command not found / supported")
    
    print(datetime.datetime.now().strftime("uReddRpc.py last run at %H:%M:%S, ") + datetime.date.today().strftime("%d %b %Y"))
    
    return

main()
