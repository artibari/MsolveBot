import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



def send_mail(cond_id,api_error_report,**kwargs):
    msg = MIMEMultipart() ## Object Instance for message
    password = 'mahindra@123'
    msg['From']= "BMCERRORTRACK@mahindra.com"
    msg['To'] = "BMCERRORTRACK@mahindra.com"
##    message = send_mail_error(cond_id,api_error_report,**kwargs)
##    print(message)
    msg['Subject']= "MC API didn't work for" +cond_id
    #body = "BMC API didn't work for "+cont_id+".\nError Stack Trace is :\n"+api_error_report+"\n\n Ticket details: \n"+str(kwargs)
    #msg.attach(MIMEText(body,'plain'))

    server =smtplib.SMTP('10.2.202.42',25)
    server.starttls()
    server.login(msg['From'],password)
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()



def send_mail_main(cont_id,api_error_report,**kwargs):
	import requests

	url = "http://10.2.152.188:8580/mailapi/DataController"

	payload = "fromId=BMCERRORTRACK@mahindra.com&fromNm=Prashant&mailTo=BMCERRORTRACK@mahindra.com&mailSubj=BMC API Error for token id {}&mailText=BMC API did not work for {}. <br>Error Stack Trace is: <br> {}<br><br> Ticket details: <br> {}".format(cont_id, cont_id, api_error_report, str(kwargs))
	headers = {
	    'content-type': "application/x-www-form-urlencoded",
	    'cache-control': "no-cache",
    	'postman-token': "125a3b31-b58c-807e-ffd4-d066ae1d61d6"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	#print(response)

	print(response.text)
	#return response.text

send_mail('23180189','Internal Server Error')
