'''
Huawei E8131 library made by Tom Stroobants 17 september 2014

This library works with the Huawei model E8131 and possible previous libraries. 
I am currently adding extra options to disable some functions so 
it could work with older versions (like admin-panel).

For any issues, just use the github issue reported!

Copyright (c) 2014 Tom Stroobants <stroobantstom@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

import requests, sys
from datetime import datetime
from urlparse import urlparse
from xml.dom import minidom
import xmltodict

class ApiUrls(object):
	DEVICE_INFO = '/api/device/information'
	MONITORING_STATUS = '/api/monitoring/status'
	MONITORING_CHECK_NOTIFICATIONS = '/api/monitoring/check-notifications'
	NET_CURRENT_PLMN = '/api/net/current-plmn'
	SMS_COUNT = '/api/sms/sms-count'
	TRAFFIC_STATS = '/api/monitoring/traffic-statistics'
	SMS_SEND_STATUS = '/api/sms/send-status'
	USER_STATUS = '/api/user/state-login'
	USER_REMIND = '/api/user/remind'
	MONITORING_CONVERGED_STATUS = '/api/monitoring/converged-status'
	PIN_STATUS = '/api/pin/status'
	PIN_SIMLOCK = '/api/pin/simlock'
	USSD_STATUS = '/api/ussd/status'
	UPDATE_STATUS = '/api/online-update/status'
	CLEAR_STATISTICS = '/api/monitoring/clear-traffic'
	USER_LOGIN = '/api/user/login'
	SMS_LIST = '/api/sms/sms-list'
	SMS_DELETE = '/api/sms/delete-sms'
	SIM_IMPORt = '/api/sms/backup-sim'
	SMS_SET_READ = '/api/sms/set-read'
	SMS_SEND = '/api/sms/send-sms'
	USER_SESSION = '/api/user/session'

class E8131():
	ip = "http://10.0.0.1"	# IP of the device
	debug = 1				# Show outprint or not

	'''
	Init, will check if there is a connection to the device else stop the program
	'''
	def __init__(self, **kwargs):
		if 'url' in kwargs:
			userUrl = kwargs['url']
		if 'debug' in kwargs:
			self.debug = kwargs['debug']
		url = urlparse(userUrl)
		self.ip = url[0] + "://" + url[1]
		if len(self.ip) == 3:
			self.log("Wrong url input '" + self.ip + "'", 2)
			sys.exit()			
		self.get_request(url=ApiUrls.DEVICE_INFO)
		self.log("I seem to be connected to the device", 0)

	'''
		See included file js2py
	'''
	def js_base64(self, inp_str):
		base64_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
		length = len(inp_str)
		i = 0
		out = ""
		while i < length:
			c1 = ord(inp_str[i]) & 0xff
			i += 1 #Python doesn't have ++
			if i == length:
				out += base64_str[c1 >> 2]
				out += base64_str[(c1 & 0x3) << 4]
				out += "=="
				break

			c2 = ord(inp_str[i])
			i += 1
			if i == length:
				out += base64_str[c1 >> 2]
				out += base64_str[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
				out += base64_str[(c2 & 0xF) << 2]
				out += '='
				break

			c3 = ord(inp_str[i])
			i += 1
			out += base64_str[c1 >> 2]
			out += base64_str[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
			out += base64_str[((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6)]
			out += base64_str[c3 & 0x3F]
		return out

	def parse_xml(self,data):
		temp_xml = minidom.parseString(data)
		xml = dict(error = 0, error_msg = '', data = "")
		if len(temp_xml.getElementsByTagName("error")) > 0:
			self.log("Errors happened!",1)
			if temp_xml.getElementsByTagName("error")[0].getElementsByTagName("code")[0].firstChild is not None:
				xml['error'] = temp_xml.getElementsByTagName("error")[0].getElementsByTagName("code")[0].firstChild.nodeValue
			if temp_xml.getElementsByTagName("error")[0].getElementsByTagName("message")[0].firstChild is not None:
				xml['error_msg'] = temp_xml.getElementsByTagName("error")[0].getElementsByTagName("message")[0].firstChild.nodeValue
			if xml['error'] == "100003":
				self.log("Need to be logged in (if you login while you were already logged in, he will logout!",1)
			if xml['error'] == "100004":
				self.log("System is too busy",1)
		else:
			self.log("Got a response")
			xml['data'] = temp_xml.getElementsByTagName("response")[0]
		return xml

	def log(self, message, v_type = 0):
		v_string = "GENERIC"
		if self.debug == 1:
			if(v_type == 0):
				v_string = "INFO"
			elif(v_type == 1):
				v_string = "ERROR" 
			print "[" + v_string  + "] " + message

	def post_request(self, url, data, headers = ""):
		url = self.ip + url
		try:
			if len(headers) > 0:
				r = requests.post(url,data=data, headers=headers)
				if r.status_code != 200:
					self.log("HTTP status code '" + str(r.status_code) + "'",1)
					sys.exit() 
				return r
			else:
				r = requests.post(url,data=data)
				if r.status_code != 200:
					self.log("HTTP status code '" + str(r.status_code) + "'",1)
					sys.exit() 
				return r
		except requests.exceptions.ConnectionError:
			self.log("Network problem! Could not access the url, check the url and your network",1)
			sys.exit()
		except requests.exceptions.HTTPError:
			self.log("Invalid HTTP response",1)
			sys.exit()
		except requests.exceptions.Timeout:
			self.log("Timeout happened while accessing the website",1)
			sys.exit()
		except requests.exceptions.TooManyRedirects:
			self.log("Too many redirections happened, this shouldn't happen with the standard website",1)
			sys.exit()

	def get_request(self,url):
		if len(url) < 1:
			self.log("No url",1)
			sys.exit()
		try:
			r = requests.get(self.ip + url)
			if r.status_code != 200:
				self.log("HTTP status code '" + str(r.status_code) + "'",1)
				sys.exit() 
			return r
		except requests.exceptions.ConnectionError:
			self.log("Network problem! Could not access the url, check the url and your network",1)
			sys.exit()
		except requests.exceptions.HTTPError:
			self.log("Invalid HTTP response",1)
			sys.exit()
		except requests.exceptions.Timeout:
			self.log("Timeout happened while accessing the website",1)
			sys.exit()
		except requests.exceptions.TooManyRedirects:
			self.log("Too many redirections happened, this shouldn't happen with the standard website",1)
			sys.exit()

	def get_info(self, url, options):
		r = self.get_request(url=url)
		data = self.parse_xml(r.content)
		resp = dict()
		for option in options:
			if data['data'].getElementsByTagName(option)[0].firstChild is not None:
				resp[option] = data['data'].getElementsByTagName(option)[0].firstChild.nodeValue
		return resp

	def get_connection_status(self):
		info_avail = ['ConnectionStatus','SignalStrength','SignalIcon','CurrentNetworkType','CurrentServiceDomain','RoamingStatus','BatteryStatus','BatteryLevel','SimlockStatus','WanIPAddress','PrimaryDns','SecondaryDns','CurrentWifiUser','TotalWifiUser','ServiceStatus','SimStatus','WifiStatus']
		return self.get_info(ApiUrls.MONITORING_STATUS,info_avail)

	def get_device_info(self):
		info_avail = ['DeviceName','SerialNumber','Imei','Imsi','Iccid','Msisdn','HardwareVersion','SoftwareVersion','WebUIVersion','MacAddress1','MacAddress2','ProductFamily','Classify']
		return self.get_info(ApiUrls.DEVICE_INFO,info_avail)

	def get_check_notifications(self):
		info_avail = ['UnreadMessage','SmsStorageFull','OnlineUpdateStatus']
		return self.get_info(ApiUrls.MONITORING_CHECK_NOTIFICATIONS,info_avail)

	def get_network_info(self):
		info_avail = ['State','FullName','ShortName','Numeric','Rat']
		return self.get_info(ApiUrls.NET_CURRENT_PLMN,info_avail)	

	def get_sms_count(self):
		info_avail = ['LocalUnread','LocalInbox','LocalOutbox','LocalDraft','LocalDeleted','SimUnread','SimInbox','SimOutbox','SimDraft','LocalMax','SimMax','NewMsg']
		return self.get_info(ApiUrls.SMS_COUNT,info_avail)

	def get_traffic_stats(self):
		info_avail = ['CurrentConnectTime','CurrentUpload','CurrentDownload','CurrentDownloadRate','CurrentUploadRate','TotalUpload','TotalDownload','TotalConnectTime']
		return self.get_info(ApiUrls.TRAFFIC_STATS,info_avail)
	#Last sms send status
	def get_sms_send_status(self):
		info_avail = ['Phone','SucPhone','FailPhone','TotalCount','CurIndex']
		return self.get_info(ApiUrls.SMS_SEND_STATUS,info_avail)

	def get_user_status(self):
		info_avail = ['State','Username']	#State -1 is not logged in
		return self.get_info(ApiUrls.USER_STATUS,info_avail)

	def user_logged_in(self):
		if self.get_user_status()['State'] == "0":
			return True
		else:
			return False
		
	#Some sort of remind status on IP? Call after login Doesn't do cookies but with IP?
	def get_user_remind(self):
		info_avail = ['remindstate']
		return self.get_info(ApiUrls.USER_REMIND,info_avail)

	def get_converged_status(self):
		info_avail = ['SimState','SimLockEnable','CurrentLanguage']
		return self.get_info(ApiUrls.MONITORING_CONVERGED_STATUS,info_avail)

	def get_pin_status(self):
		info_avail = ['SimState','PinOptState','SimPinTimes','SimPukTimes']
		return self.get_info(ApiUrls.PIN_STATUS,info_avail)

	def get_pin_simlock(self):
		info_avail = ['SimLockEnable','SimLockRemainTimes','pSimLockEnable','pSimLockRemainTimes']
		return self.get_info(ApiUrls.PIN_SIMLOCK,info_avail)

	def get_ussd_status(self):
		print "Could not test this, my provider has no USSD, please fill an issue with info about USSDs in it!"

	def get_update_status(self):
		info_avail['CurrentComponentStatus','CurrentComponentIndex','TotalComponents','DownloadProgress']
		return self.get_info(ApiUrls.UPDATE_STATUS,info_avail)

	def post_get_sms_list(self, readcount = 20, boxtype = 1, sorttype = 0, ascending = 0, unreadpreffered = 0):
		data = self.post_request(ApiUrls.SMS_LIST,"<request><PageIndex>1</PageIndex><ReadCount>20</ReadCount><BoxType>1</BoxType><SortType>0</SortType><Ascending>0</Ascending><UnreadPreferred>0</UnreadPreferred></request>").content
		r = self.parse_xml(data)
		if r['error'] == 0:
			dictingy = xmltodict.parse(data)
			return dictingy['response']
		else:
			return False

	def post_clear_statistics(self):
		r = self.parse_xml(self.post_request(ApiUrls.CLEAR_STATISTICS,"<request><ClearTraffic>1</ClearTraffic></request>").content)
		if r['error'] == 0:
			if r['data'].firstChild.nodeValue == "OK":
				return True
			else:
				return False
		else:
			return False

	def post_user_login(self, user = "admin", password = "admin"):
		r = self.parse_xml(self.post_request(ApiUrls.USER_LOGIN,"<request><Username>" + user + "</Username><Password>" + cell.js_base64(password) + "</Password></request>").content)
		if r['error'] == "108001":
			self.log("Username is wrong",1)
		if r['error'] == "108002":
			self.log("Password is wrong",1 )
		if r['error'] == "108003":
			self.log("Login already logged in!",1)
		if r['error'] == 0:
			if r['data'].firstChild.nodeValue == "OK":
				return True
			else:
				return False
		else:
			return False

	def post_sms_delete(self, index):
		r = self.parse_xml(self.post_request(ApiUrls.SMS_DELETE,"<request><Index>" + index + "</Index></request>").content)
		if r['error'] == 0:
			if r['data'].firstChild.nodeValue == "OK":
				return True
			else:
				return False
		else:
			return False

	def now(self):
		return datetime.now().strftime("%Y-%m-%d %I:%M:%S")

	def post_import_from_sim(self):
		r = self.parse_xml(self.post_request(ApiUrls.SIM_IMPORt,"<request><isMove>0</isMove><Date>"+self.now()+"</Date></request>").content)
		if r['error'] == 0:
			if r['data'].getElementsByTagName("FailNumber")[0].firstChild.nodeValue == "0":
				return True
			else:
				self.log("Import had " + r['data'].getElementsByTagName("FailNumber")[0].firstChild.nodeValue + " failed imports! (But " + r['data'].getElementsByTagName("SucNumber")[0].firstChild.nodeValue + " numbers were imported)",1)
				return False
		else:
			return False	

	def post_set_sms_as_read(self, index):
		r = self.parse_xml(self.post_request(ApiUrls.SMS_DELETE,"<request><Index>" + index + "</Index></request>").content)
		if r['error'] == 0:
			if r['data'].firstChild.nodeValue == "OK":
				return True
			else:
				return False
		else:
			return False

	def post_send_sms(self, numbers, content):
		if len(content) > 140:
			self.log("Message content can't be over 140")
			return False
		else:
			if type(numbers) is list:
				numb_list = ""
				for nr in numbers:
					numb_list += "<Phone>"+nr+"</Phone>"
			else:
				numb_list = "<Phone>" + numbers + "</Phone>"
			req = "<request><Index>-1</Index><Phones>"+numb_list+"</Phones><Sca></Sca><Content>"+content+"</Content><Length>" + str(len(content)) + "</Length><Reserved>1</Reserved><Date>" + self.now() + "</Date></request>"
			r = self.parse_xml(self.post_request(ApiUrls.SMS_SEND,req).content)
			if r['error'] == 0:
				if r['data'].firstChild.nodeValue == "OK":
					return True
				else:
					return False
			else:
				return False

	def post_user_session_refresh(self):
		r = self.parse_xml(self.post_request(ApiUrls.USER_SESSION,"<request><keep>1</keep></request>").content)
		if r['error'] == 0:
			if r['data'].firstChild.nodeValue == "OK":
				return True
			else:
				return False
		else:
			return False

