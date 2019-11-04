##import smtplib
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail_1(cont_id,api_error_report,**kwargs):
	fromaddr = "BMCERRORTRACK@mahindra.com"
	toaddr = "BMCERRORTRACK@mahindra.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "BMC API Error for token id "+cont_id

	body = "BMC API did not work for "+cont_id+". \nError Stack Trace is: \n"+api_error_report+"\n\n Ticket details: \n"+str(kwargs)
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('10.2.202.42', 25)
	server.starttls()
	server.login(fromaddr, "mahindra@123")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def send_mail(cont_id,api_error_report,**kwargs):
	import requests

	url = "http://10.2.152.188:8580/mailapi/DataController"

	payload = "fromId=BMCERRORTRACK@mahindra.com&fromNm=Prashant&mailTo=BMCERRORTRACK@mahindra.com&mailSubj=BMC API Error for token id {}&mailText=BMC API did not work for {}. <br>Error Stack Trace is: <br> {}<br><br> Ticket details: <br> {}".format(cont_id, cont_id, api_error_report, str(kwargs))
	headers = {
	    'content-type': "application/x-www-form-urlencoded",
	    'cache-control': "no-cache",
    	'postman-token': "125a3b31-b58c-807e-ffd4-d066ae1d61d6"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	

	print(response.text)

"""def send_mail_location(cont_id,api_error,**kwargs):
	import requests

	email_list = ["MSOLVE@mahindra.com", "MSOLVE-LEADS@mahindra.com"]

	from i in email_list:
		url = "http://10.2.152.188:8580/mailapi/DataController"

        	payload = "fromId=BMCERRORTRACK@mahindra.com&fromNm=Prashant&mailTo={}&mailSubj=BMC API Error for token id {}&mailText=BMC API did not work for {}. <br>Error Stack Trace is: <br> {}<br><br> Ticket details: <br> {}".format(i, cont_id, cont_id, api_error_report, str(kwargs))
        	headers = {
            		'content-type': "application/x-www-form-urlencoded",
            		'cache-control': "no-cache",
        		'postman-token': "125a3b31-b58c-807e-ffd4-d066ae1d61d6"
            	}

        	response = requests.request("POST", url, data=payload, headers=headers)

        	print(response.text)"""
