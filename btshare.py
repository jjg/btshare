# btshare.py

import os
import smtplib
import mimetypes
from flask import Flask
from flask import request

# config
SHARE_ROOT = ''
SERVER_HOST = ''
SERVER_EMAIL_ADDRESS = ''
SERVER_EMAIL_PASSWORD = ''
SMTP_SERVER = ''
SMTP_PORT = ''
BTSYNC_HOST = ''
BTSYNC_PORT = ''



app = Flask(__name__)

def send_notification(destination_email, subject, message):
	# assemble email
	message = MIMEText(message)
	message['Subject'] = subject
	message['From'] = EMAIL_ADDRESS
	message['To'] = destination_email
	
	# send
	s = smtplib.SMTP(SMTP_SERVER + ':' + SMTP_PORT)
	s.ehlo()
	s.starttls()
	s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	s.sendmail(EMAIL_ADDRESS, destination_email, message.as_string())
	s.quit()
	
	
@app.route('/')
def hello_world():
	return 'Hello Jerk!'
	
@app.route('/user')
def user():
	return 'not implemented'
	
@app.route('/share', methods=['POST'])
def share():
	if request.method == 'POST':
		#
		# create a new share
		#
		
		# debug
		print request.form['owneremail']
		print request.form['password']
		print request.form['secret']
		print request.form['guestemail']
		
		secret = request.form['secret']
		
		# TODO: authenticate user
		
		# create share folder
		os.makedirs(share_root + secret)
		
		# TODO: enable sync
		# ex:
		# http://[address]:[port]/api?method=add_folder&dir=(folderPath)[&secret=(secret)&selective_sync=1]
		
		# TODO: email link to owner & guests
		
		return 'ok'
	else:
		show_share_form()

	
if __name__ == '__main__':
	app.run()