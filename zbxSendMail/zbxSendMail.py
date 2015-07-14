#!/usr/bin/python

import os
import sys
import re
import smtplib
import datetime
import subprocess
from zbxAuth import zapi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


count = 0

def main():
	smtp_server_addr = "smtp.example.com"
	smtp_server_port = "25"
	smtp_server_tls = "False" # Or True (With first capital letter)
	smtp_sender = "Zabbix <zabbix@example.com>"

	# Mail Authentication	
	#smtp_auth_user = 'auth_user'
	#smtp_auth_passwd = 'v3ry_s3cUr3_P@ssw0rd'

	# list of arguments
	zbx_message = sys.argv[3]
	zbx_subject = sys.argv[2]
	zbx_sendto  = sys.argv[1]

	zbx_subject = zbx_subject.split("#")
	itemid = zbx_subject[0]
	subject = zbx_subject[1]

	zbx_app = zapi.application.get({
		"output": "extend",
		"itemids": itemid
	})

	zbxAppName = zbx_app[0]['name']

	zbx_message = zbx_message.replace("{APP.NAME}", zbxAppName)
	if zbx_message.find("OK") > 0:
		font_color = "green";
	else:
		font_color = "red";

	zbx_message = zbx_message.replace("#color",font_color)

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = smtp_sender
	msg['To'] = zbx_sendto
	
	def sendMail():
		
		footer = "</body></html>"

		MailMsg = '''
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>

<body>
%s
%s 
		''' % (zbx_message, footer)

		_WriteOutput( MailMsg )

		html_message = MIMEText(MailMsg, 'html')

		msg.attach(html_message)
		
		try:
			smtpObj = smtplib.SMTP(smtp_server_addr, smtp_server_port)

			if smtp_server_tls == True :
				smtpObj.ehlo()
				smtpObj.starttls()
				smtpObj.ehlo
				smtpObj.login(smtp_auth_user, smtp_auth_passwd)
			try:
  				smtpObj.sendmail(smtp_sender, zbx_sendto, msg.as_string())
				print "OK-> We are sending emails"
			except Exception as e:
		 	   print "Error: unable to send email:  %s" % (e)

#			smtpObj.quit()
			smtpObj.close()

		except Exception as e:
			_WriteOutput("Error: unable to send email:  %s" % (e))

	sendMail()
	
def _WriteOutput(strToWrite):
	global count
	logfile = "log_sendmail.log"
	log_file_folder = "/usr/lib/zabbix/alertscripts"

	jobDate = datetime.datetime.now().strftime('%Y%m%d')
	log_file = "%s/%s-%s.log" % (log_file_folder, logfile, jobDate)

	if not os.path.exists(log_file_folder):
			os.makedirs(log_file_folder)
	try:
		with open(log_file, "a+") as logfile: 
			if strToWrite:
				dtNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				logLine = "%d) %s - %s" % (count, dtNow, strToWrite)
				if "debug" in map(lambda each:each.lower(), sys.argv):
					print logLine
				try:
					logfile.writelines(logLine)
					logfile.write("\n")
				except IOError as e:
					_WriteOutput ("Error while writing log:  %s " % (e) )

				count = count + 1

	except IOError as e:
		_WriteOutput ("Error: %s " % (e) )

# Execute main function
if __name__ == "__main__":
    main()

