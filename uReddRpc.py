from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoinrpc.authproxy import JSONRPCException

import RPi.GPIO as GPIO
import datetime
import smtplib
import time
import os
import sys
import string
import getpass

# ===== BEGIN USER SETTINGS =====

rpcuser = "YOUR_RPC_USERNAME"
rpcpass = "YOUR_RPC_PASSWORD"
rpcport = "45443"

email_from_addr = "YOUR_FROM_EMAIL_ADDRESS"
email_to_addr = "YOUR_DESTINATION_EMAIL_ADDRESS"
email_subject = "New Reddcoin stake event"
email_login = "YOUR_FULL_EMAIL_LOGIN"
email_password = "YOUR_EMAIL_PASSWORD"
email_smtp_server="smtp.gmail.com:587"

# ====== END USER SETTINGS ======

def sendemail(message):
               
    header  = 'From: %s\n' + email_from_addr
    header += 'To: %s\n' + email_to_addr
    header += 'Subject: %s\n\n' + email_subject
    message = header + message

    server = smtplib.SMTP(email_smtp_server)
    server.starttls()
    server.login(email_login,email_password)
    problems = server.sendmail(email_from_addr, email_to_addr, message)
    server.quit()

    print "Email sent to " + str(email_to_addr)
    return

access = AuthServiceProxy("http://"+rpcuser+":"+rpcpass+"@127.0.0.1:" + rpcport)

if len(sys.argv) != 2:
    print "\nUsage: python uReddrpc.py [rpc_command]\n"
    sys.exit()

cmd = sys.argv[1].lower()

if cmd == "getinterest":

    try:

        current_interest = access.getinterest()
        print "JSON Received: " + str(current_interest)

        fname = "/tmp/my_interest.log"

        if os.path.isfile(fname):

            fh = open(fname,"r+")
            file_contents = float(fh.read())

            print "Last interest ammount was " + str(file_contents) + "\nCurrent interest ammount is " + str(current_interest)

            if float(file_contents) != float(current_interest):

                new_total = float(current_interest) - float(file_contents)

                print "New stake event totalling " + str(new_total) + " coins"

                GPIO.setup(12, GPIO.OUT)
                GPIO.output(12, True)
                time.sleep(0.1)
                GPIO.output(12, False)
                time.sleep(0.05)
                GPIO.output(12, True)
                time.sleep(0.1)
                GPIO.output(12, False)

                fh.seek(0)
                fh.write(str(current_interest))
                fh.close()

                sendemail(message = "New stake event totalling " + str(new_total) + " coins")
       
        else:

            print "File not found, creating " + fname
            fh = open(fname,"w")
            fh.write(str(current_interest))
            fh.close()

    except Exception,e:
        print str(e)

elif cmd == "unlockforstaking":

    try:

        pwd = getpass.getpass(prompt="Enter wallet passphrase: ")
        print access.walletpassphrase(pwd, 9999999, True)

    except JSONRPCException as e:
        print "JSONRPCException: ({0})".format(e.error)

elif cmd == "getstakinginfo":
    try:
        print access.getstakinginfo()
    except:
        print "Error"

else:
    print "Command not found or not supported"

print datetime.datetime.now().strftime("Finished at %H:%M:%S, ") + datetime.date.today().strftime("%d %b %Y")
