#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

import smtplib
import smtplogger

#Here is the magic

def enviaEmail(msg, from_who,to_who):
	fromaddr = from_who
	toaddr = to_who
	msg = msg
	host = smtplogger.host
	port = smtplogger.port
	user = smtplogger.logger
	passw = smtplogger.key
	server = smtplib.SMTP(host,port)
	server.starttls()
	server.login(user,passw)
	server.sendmail(fromaddr,toaddr,msg.as_string())		
	server.quit()

#.:.
