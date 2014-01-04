# btshare.py

import os
import smtplib
import mimetypes
import ConfigParser
import httplib
from flask import Flask
from flask import request
from email.mime.text import MIMEText

# load config
config = ConfigParser.RawConfigParser()
config.read('btshare.cfg')
	
IMAP_SERVER = config.get('mailserver', 'imap_server')
SMTP_SERVER = config.get('mailserver', 'smtp_server')
SMTP_PORT = config.get('mailserver', 'smtp_port')
EMAIL_ADDRESS = config.get('mailserver', 'email_address')
EMAIL_PASSWORD = config.get('mailserver', 'email_password')
WEB_HOST = config.get('webserver', 'web_hostname')
SHARE_ROOT = config.get('webserver', 'share_root')
BTSYNC_HOST = config.get('btsync', 'btsync_host')
BTSYNC_PORT = config.get('btsync', 'btsync_port')
BTSYNC_API_KEY = config.get('btsync', 'btsync_api_key')


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
	
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'hello jerk!'
	
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
		
		owner_email = request.form['owneremail']
		secret = request.form['secret']
		
		# TODO: authenticate user
		
		# create share folder
		new_share_fs_path = SHARE_ROOT + secret
		os.makedirs(new_share_fs_path)
		
		# TODO: enable sync
		# ex:
		# http://[address]:[port]/api?method=add_folder&dir=(folderPath)[&secret=(secret)&selective_sync=1]
		api_url = '/api?method=add_folder&dir=%s&secret=%s' % (new_share_fs_path, secret)
		
		# debug
		print(api_url)
		
		API_CONNECTION = httplib.HTTPConnection(BTSYNC_HOST)
		API_CONNECTION.request('GET', api_url)
		
		# TODO: something reasonable based on the response (if error, etc.)
		response = API_CONNECTION.getresponse()
		raw_response = response.read()
		API_CONNECTION.close()
		
		# debug
		print(raw_response)
		
		# email link to owner & guests (probably shouldn't email secret...)
		message = 'Your files are shared here:\n\n http://%s/shares/%s/' % (WEB_HOST, secret)
		
		send_notification(owner_email, 'Your btshare ready!', message)
		
		return 'ok'
	else:
		show_share_form()

	
if __name__ == '__main__':
	app.run(debug=True)