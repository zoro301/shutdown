#coding: utf-8
import poplib,email
from email.mime.text import MIMEText
from email.header import decode_header
from config import POP3_HOST,MAIL_USERNAME, MAIL_PASSWORD,SUBJECT,EMAIL_SERVER, RECEVIE_EMAIL,FROM_EMAIL,REPLY_SUBJECT
import smtplib
import time
import os,sys

def connectMailClient():
	pop3 = poplib.POP3_SSL(POP3_HOST)
	pop3.set_debuglevel(1)
	pop3.user(MAIL_USERNAME)
	pop3.pass_(MAIL_PASSWORD)
	return pop3

def disconnectMailClient(pop3):
	pop3.quit()

def checkMailBox(pop3=None):
	pop3 = connectMailClient()
#	ret = pop3.stat()
	ret = pop3.list()
	down = pop3.retr(len(ret[1]))
	#if down[1][12].decode('utf-8') == SUBJECT:
		#return True
	for line in down[1]:
		if line.decode('utf-8') == SUBJECT:
			return True
	disconnectMailClient(pop3)
	
def sendEmail(msg):
	smtp_server = EMAIL_SERVER['server']	
	user = EMAIL_SERVER['user']
	password = EMAIL_SERVER['password']
	port = EMAIL_SERVER['port']

	emailInfo = createEmail(msg)
	print emailInfo
	email = smtplib.SMTP_SSL(smtp_server,port)
	email.login(user, password)
	email.sendmail(FROM_EMAIL, RECEVIE_EMAIL, emailInfo.as_string())
	email.quit()

def createEmail(msg):
	info = MIMEText(msg,_subtype='html', _charset='utf-8')
	info['Subject'] = REPLY_SUBJECT 
	info['From'] = FROM_EMAIL
	info['to'] = ';'.join(RECEVIE_EMAIL)
	return info


if __name__=="__main__":
	command = 'shutdown -h now'
	sudo_passwd = 'passw0rd'
	while True:
		time.sleep(10)
		if checkMailBox():		
			try:
				ewsMsg = '导弹就绪，准备断开安全链接！'		
				sendEmail(ewsMsg)
				#os.system('shutdown -f -s -t 10 -c closing...')
				os.system('echo %s|sudo -S %s' % (sudo_passwd,command))

				break
			except Exception as e:
				errorMsg = '导弹发射失败！'
				sendEmail(errorMsg)
