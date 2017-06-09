#!/usr/bin/python

'''
author = wise-king-sullyman https://github.com/wise-king-sullyman/bitcoin_price_alert
if you have any problems/questions please create an issue on the github page or email me at a.m.sullivan.github@gmail.com
feel free to send me a bitcoin tip if this helps you make any money, or if you're just feeling especially generous 13L2BeJBeRoSWsz79izjiSagwEhPpLLJfc

credit to CrakeNotSnowman for sendMessage.py where I ripped the sendsms function from https://github.com/CrakeNotSnowman/Python_Message

also thanks to all of the fellow lost souls on stack exchange who had already asked every question I had

this works for me with python v2.7.9 on my raspberry pi 3, YMMV


This function below sets up the email or text alerts, if you want to go without those and just have it
print feel free to comment this function and the sendsms lines out
'''
def sendsms( sms ):
    SMTPserver = 'smtp.gmail.com' #enter SMTP server for your email client, this is Gmail's
    sender =     'enter_email_here@gmail.com' #enter email to send alerts from; recommend a new email for this
    destination = ['enter_alert_destination_here@smsgateway.com'] #enter where you want alerts to go
    '''
    for sending to a phone number via sms https://en.wikipedia.org/wiki/SMS_gateway has a list of sms
    gateways, i.e. vtext.com is for verizon wireless. Simply use the gateway domain for your carrier and
    your 10 digit phone number i.e. 1234567890@vtext.com,  charges may apply by your carrier idk
    alternatively just enter an email address for email alerts. If you do go that route make sure to
    add them to your contact list as otherwise they seem to always go straight to the junk folder
    '''
    
                                                            

    USERNAME = "enter_email_here@gmail.com" #enter sender email 
    PASSWORD = "enter_password_here" #enter sender email password

    text_subtype = 'plain'
    import sys
    import os
    import re
    from smtplib import SMTP_SSL as SMTP
    from email.mime.text import MIMEText
    try:
        msg = MIMEText(sms, text_subtype)
        msg['From']   = sender
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME,PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
    except Exception, exc:
        sys.exit( "mail failed; %s" % str(exc) )

        
import json
import urllib2
import time
from socket import error as SocketError
import errno

alarm_amount = 10.00000 #enter value change that you want to be alerted by in USD
#for example with this value you will be alerted if the price increases or decreases by $10 over the
#course of an hour

#sets alarm values starting points at something that they will never reach
global low_alarm_val 
low_alarm_val = 0.000000 #establish variable that will send alert if btc price is lower than it
global high_alarm_val
high_alarm_val = 1000000.00000 #establish variable that will send alert if btc price is higher than it

while True: #will loop until manually closed
    current_time = time.localtime()
    time_var = time.strftime('%M', current_time) #establish minute variable
    time_var_h = time.strftime('%H', current_time) #establish hour variable
    
    try: #this is where we scrape the bitcoin value from the coindesk api
        url = urllib2.urlopen("http://api.coindesk.com/v1/bpi/currentprice.json").read()
        data = json.loads(url)
        BTC_VAL = data['bpi']["USD"]['rate_float'] #save value as BTC_VAL
    except SocketError as e: #this section is trying to address an error on the api server side
        if e.errno != errno.ECONNRESET: #I believe it is fixed but will require more testing to be sure
            raise
        pass
    
    '''
    the if statement below sends an alert at 7 am local time that says the current btc value and the high
    and low alarm values (HAV and LAV) at the time, feel free to comment out if you dont want any alerts, or
    change the time the alert sends. If you change the alert time military time must be used, and with no
    leading zeros i.e. 5:00 am = 5, 3:00 pm = 15
    '''
    if int(time_var_h) == 7 :
        print 'New day'
        print 'new LAV = ', low_alarm_val, 'new HAV = ', high_alarm_val
        print 'Current BTC value = ', BTC_VAL
        sendsms( sms = ('Current BTC value = ' + str(BTC_VAL) + ' LAV = ' + str(low_alarm_val) + ' HAV = ' + str(high_alarm_val)))
        time.sleep(3601)
    
    if int(time_var) == 00 : #resets low and high alarm values every hour based on the current btc value every hour on the hour
        low_alarm_val = BTC_VAL -alarm_amount
        high_alarm_val = BTC_VAL +alarm_amount
        print 'new LAV = ', low_alarm_val, 'new HAV = ', high_alarm_val
        #sendsms( sms = ('new LAV = ' + str(low_alarm_val) + ' new HAV = ' + str(high_alarm_val)))
        #previous line sends alert when values are reset, uncomment to receive these alerts
        time.sleep(60)
        
    if BTC_VAL >= high_alarm_val: #sends alert if btc value increases over the high alarm threshold 
        low_alarm_val = BTC_VAL -alarm_amount
        high_alarm_val = BTC_VAL +alarm_amount
        print 'HAV exceeded, current BTC value = ' + str(BTC_VAL)
        print 'new LAV = ', low_alarm_val, 'new HAV = ', high_alarm_val
        sendsms( sms = ('HAV exceeded, current BTC value = ' + str(BTC_VAL) + ' new LAV = ' + str(low_alarm_val) + ' new HAV = ' + str(high_alarm_val)))
        time.sleep(10)
    if BTC_VAL <= low_alarm_val: #sends alert if btc value decreases below low alarm threshold
        low_alarm_val = BTC_VAL -alarm_amount
        high_alarm_val = BTC_VAL +alarm_amount
        print 'LAV exceeded, current BTC vaue = ' + str(BTC_VAL)
        print 'new LAV = ', low_alarm_val, 'new HAV = ', high_alarm_val
        sendsms( sms = ('LAV exceeded, current BTC value = ' + str(BTC_VAL) + ' new LAV = ' + str(low_alarm_val) + ' new HAV = ' + str(high_alarm_val)))
        time.sleep(10)

    else:
	time.sleep(60)
'''
Copyright 2017 A. M. Sullivan (a.m.sullivan.github@gmail.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''   


