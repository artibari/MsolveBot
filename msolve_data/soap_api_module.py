import requests
import ssl
from suds.client import Client
from collections import OrderedDict as od

proxy_setting = { 'http' : 'http://srivpra-cont:12mahindr@@10.2.152.4:80' }

def create_ticket_bmc(**kwargs):
	print("here ooooo {}".format(kwargs))
	Corporate_ID = str(kwargs.get("Corporate_ID"))
	Summary = str(kwargs.get("Summary"))
	Urgency = str(kwargs.get("Urgency"))
	Impact = str(kwargs.get("Impact"))
	Assigned_Group = str(kwargs.get("Assigned_Group"))
	Status = "New"
	Service_Type = "User Service Request"
	Reported_Source = "Chatbot"
	MNM_Chatbot_ID = str(kwargs.get("MNM_Chatbot_ID"))
	Notes = str(kwargs.get("Notes"))
	#resp = requests.request("get","https://emss.mahindra.com/sap/bc/zhr_tq_emp_det?sap-client=500&IV_PERNR="+Corporate_ID)
        #resp_list = resp.text.split("-//-")
        #print "Unidentified Service REQUEST....{}".format(resp_list)
      	#try:
       		#mobile = resp_list[18]
                #pushUserDetailsToMongo(sessionId, mobile=mobile)
        #except:
        #	mobile = ""

	Submitted_By="mSolve"
	mobile =str(kwargs.get("mobile"))
	asset = str(kwargs.get("asset"))

	##print("Santosh ka phone number {} aur asset.{}".format(mobile, asset))
	#url = "http://10.2.146.76:8081/arsys/WSDL/public/mmkndremapp-dev/HPD_IncidentInterface_Create_WS"
	url ="https://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/HPD_IncidentInterface_Create_WS"
	#url ="http://mmkndremmtrss01.corp.mahindra.com:8080/arsys/services/ARService?server=itsmremars&webService=HPD_IncidentInterface_Create_WS"
	port = 'HPD_IncidentInterface_Create_WSPortTypeSoap'
	#cl = Client(url,proxy=proxy_setting)
	if hasattr(ssl, '_create_unverified_context'):
		ssl._create_default_https_context = ssl._create_unverified_context	
	cl = Client(url)
	cl = Client(url,proxy=proxy_setting)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	ticket_number = cl.service.HelpDesk_Submit_Service(Login_ID=Corporate_ID,Summary=Summary,Urgency=Urgency,Impact=Impact,Assigned_Group=Assigned_Group,Status=Status,Service_Type=Service_Type,Reported_Source=Reported_Source,MNM_Chatbot_ID=MNM_Chatbot_ID,Phone_Number=mobile,Notes=Notes,Submitted_By=Submitted_By,asset=asset)
	ticket_number = str(ticket_number)
	return ticket_number

def create_ticket_bmc_(**kwargs):
	print("here ooooo {}".format(kwargs))
	Corporate_ID = str(kwargs.get("Corporate_ID"))
	Summary = str(kwargs.get("Summary"))
	Urgency = str(kwargs.get("Urgency"))
	Impact = str(kwargs.get("Impact"))
	Assigned_Group = str(kwargs.get("Assigned_Group"))
	Status = "New"
	Service_Type = "User Service Request"
	Reported_Source = "Chatbot"
	MNM_Chatbot_ID = str(kwargs.get("MNM_Chatbot_ID"))
	Notes = str(kwargs.get("Notes"))

	url = "https://servicedesk.mahindra.com/arsys/services/ARService"
	querystring = {"server":"itsmremars","webService":"HPD_IncidentInterface_Create_WS"}

	# payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:urn=\"urn:HPD_IncidentInterface_Create_WS\">\r\n   <soapenv:Header>\r\n      <urn:AuthenticationInfo>\r\n         <urn:userName>REMEDYADMIN</urn:userName>\r\n         <urn:password>RemedyAdmin</urn:password>\r\n         <!--Optional:-->\r\n         <urn:authentication></urn:authentication>\r\n         <!--Optional:-->\r\n         <urn:locale></urn:locale>\r\n         <!--Optional:-->\r\n         <urn:timeZone></urn:timeZone>\r\n      </urn:AuthenticationInfo>\r\n   </soapenv:Header>\r\n   <soapenv:Body>\r\n      <urn:HelpDesk_Submit_Service>\r\n         <!--Optional:-->\r\n         <urn:Assigned_Group>IT-INFRA-HELPDESK-KND AD</urn:Assigned_Group>\r\n         <!--Optional:-->\r\n         <urn:Assigned_Group_Shift_Name></urn:Assigned_Group_Shift_Name>\r\n         <!--Optional:-->\r\n         <urn:Assigned_Support_Company></urn:Assigned_Support_Company>\r\n         <!--Optional:-->\r\n         <urn:Assigned_Support_Organization></urn:Assigned_Support_Organization>\r\n         <!--Optional:-->\r\n         <urn:Assignee></urn:Assignee>\r\n         <!--Optional:-->\r\n         <urn:Categorization_Tier_1></urn:Categorization_Tier_1>\r\n         <!--Optional:-->\r\n         <urn:Categorization_Tier_2></urn:Categorization_Tier_2>\r\n         <!--Optional:-->\r\n         <urn:Categorization_Tier_3></urn:Categorization_Tier_3>\r\n         <!--Optional:-->\r\n         <urn:CI_Name></urn:CI_Name>\r\n         <!--Optional:-->\r\n         <urn:Closure_Manufacturer></urn:Closure_Manufacturer>\r\n         <!--Optional:-->\r\n         <urn:Closure_Product_Category_Tier1></urn:Closure_Product_Category_Tier1>\r\n         <!--Optional:-->\r\n         <urn:Closure_Product_Category_Tier2></urn:Closure_Product_Category_Tier2>\r\n         <!--Optional:-->\r\n         <urn:Closure_Product_Category_Tier3></urn:Closure_Product_Category_Tier3>\r\n         <!--Optional:-->\r\n         <urn:Closure_Product_Model_Version></urn:Closure_Product_Model_Version>\r\n         <!--Optional:-->\r\n         <urn:Closure_Product_Name></urn:Closure_Product_Name>\r\n         <!--Optional:-->\r\n         <urn:Department></urn:Department>\r\n         <urn:First_Name></urn:First_Name>\r\n         <urn:Impact>4-Minor/Localized</urn:Impact>\r\n         <urn:Last_Name></urn:Last_Name>\r\n         <!--Optional:-->\r\n         <urn:Lookup_Keyword></urn:Lookup_Keyword>\r\n         <!--Optional:-->\r\n         <urn:Manufacturer></urn:Manufacturer>\r\n         <!--Optional:-->\r\n         <urn:Product_Categorization_Tier_1></urn:Product_Categorization_Tier_1>\r\n         <!--Optional:-->\r\n         <urn:Product_Categorization_Tier_2></urn:Product_Categorization_Tier_2>\r\n         <!--Optional:-->\r\n         <urn:Product_Categorization_Tier_3></urn:Product_Categorization_Tier_3>\r\n         <!--Optional:-->\r\n         <urn:Product_Model_Version></urn:Product_Model_Version>\r\n         <!--Optional:-->\r\n         <urn:Product_Name></urn:Product_Name>\r\n         <!--Optional:-->\r\n         <urn:Resolution></urn:Resolution>\r\n         <!--Optional:-->\r\n         <urn:Resolution_Category_Tier_1></urn:Resolution_Category_Tier_1>\r\n         <!--Optional:-->\r\n         <urn:Resolution_Category_Tier_2></urn:Resolution_Category_Tier_2>\r\n         <!--Optional:-->\r\n         <urn:Resolution_Category_Tier_3></urn:Resolution_Category_Tier_3>\r\n         <urn:Service_Type>User Service Request</urn:Service_Type>\r\n         <urn:Status>New</urn:Status>\r\n         <urn:Action></urn:Action>\r\n         <!--Optional:-->\r\n         <urn:Create_Request></urn:Create_Request>\r\n         <urn:Summary>testing API</urn:Summary>\r\n         <!--Optional:-->\r\n         <urn:Notes>please ignore</urn:Notes>\r\n         <urn:Urgency>4-Low</urn:Urgency>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Summary></urn:Work_Info_Summary>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Notes></urn:Work_Info_Notes>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Type></urn:Work_Info_Type>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Date></urn:Work_Info_Date>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Source></urn:Work_Info_Source>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_Locked>No</urn:Work_Info_Locked>\r\n         <!--Optional:-->\r\n         <urn:Work_Info_View_Access>Internal</urn:Work_Info_View_Access>\r\n         <!--Optional:-->\r\n         <urn:Middle_Initial></urn:Middle_Initial>\r\n         <!--Optional:-->\r\n         <urn:Status_Reason></urn:Status_Reason>\r\n         <!--Optional:-->\r\n         <urn:Direct_Contact_First_Name></urn:Direct_Contact_First_Name>\r\n         <!--Optional:-->\r\n         <urn:Direct_Contact_Middle_Initial></urn:Direct_Contact_Middle_Initial>\r\n         <!--Optional:-->\r\n         <urn:Direct_Contact_Last_Name></urn:Direct_Contact_Last_Name>\r\n         <!--Optional:-->\r\n         <urn:TemplateID></urn:TemplateID>\r\n         <!--Optional:-->\r\n         <urn:ServiceCI></urn:ServiceCI>\r\n         <!--Optional:-->\r\n         <urn:ServiceCI_ReconID></urn:ServiceCI_ReconID>\r\n         <!--Optional:-->\r\n         <urn:HPD_CI></urn:HPD_CI>\r\n         <!--Optional:-->\r\n         <urn:HPD_CI_ReconID></urn:HPD_CI_ReconID>\r\n         <!--Optional:-->\r\n         <urn:HPD_CI_FormName></urn:HPD_CI_FormName>\r\n         <!--Optional:-->\r\n         <urn:WorkInfoAttachment1Name></urn:WorkInfoAttachment1Name>\r\n         <!--Optional:-->\r\n         <urn:WorkInfoAttachment1Data>cid:982032760795</urn:WorkInfoAttachment1Data>\r\n         <!--Optional:-->\r\n         <urn:WorkInfoAttachment1OrigSize></urn:WorkInfoAttachment1OrigSize>\r\n         <!--Optional:-->\r\n         <urn:Login_ID>23180189</urn:Login_ID>\r\n         <!--Optional:-->\r\n         <urn:Customer_Company></urn:Customer_Company>\r\n         <!--Optional:-->\r\n        <urn:Corporate_ID></urn:Corporate_ID>\r\n         <!--Optional:-->\r\n         <urn:MNM_Chatbot_ID>xyz009opq</urn:MNM_Chatbot_ID>\r\n         <!--Optional:-->\r\n         <urn:Reported_Source>Chatbot</urn:Reported_Source>\r\n         <!--Optional:-->\r\n         <urn:Submitted_By>mSolve</urn:Submitted_By>\r\n      </urn:HelpDesk_Submit_Service>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>\r\n"
	payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:HPD_IncidentInterface_Create_WS">
	   <soapenv:Header>
	      <urn:AuthenticationInfo>
	         <urn:userName>REMEDYADMIN</urn:userName>
	         <urn:password>RemedyAdmin</urn:password>
	         <!--Optional:-->
	         <urn:authentication></urn:authentication>
	         <!--Optional:-->
	         <urn:locale></urn:locale>
	         <!--Optional:-->
	         <urn:timeZone></urn:timeZone>
	      </urn:AuthenticationInfo>
	   </soapenv:Header>
	   <soapenv:Body>
	      <urn:HelpDesk_Submit_Service>
	         <!--Optional:-->
	         <urn:Assigned_Group>{}</urn:Assigned_Group>
	         <!--Optional:-->
	         <urn:Assigned_Group_Shift_Name></urn:Assigned_Group_Shift_Name>
	         <!--Optional:-->
	         <urn:Assigned_Support_Company></urn:Assigned_Support_Company>
	         <!--Optional:-->
	         <urn:Assigned_Support_Organization></urn:Assigned_Support_Organization>
	         <!--Optional:-->
	         <urn:Assignee></urn:Assignee>
	         <!--Optional:-->
	         <urn:Categorization_Tier_1></urn:Categorization_Tier_1>
	         <!--Optional:-->
	         <urn:Categorization_Tier_2></urn:Categorization_Tier_2>
	         <!--Optional:-->
	         <urn:Categorization_Tier_3></urn:Categorization_Tier_3>
	         <!--Optional:-->
	         <urn:CI_Name></urn:CI_Name>
	         <!--Optional:-->
	         <urn:Closure_Manufacturer></urn:Closure_Manufacturer>
	         <!--Optional:-->
	         <urn:Closure_Product_Category_Tier1></urn:Closure_Product_Category_Tier1>
	         <!--Optional:-->
	         <urn:Closure_Product_Category_Tier2></urn:Closure_Product_Category_Tier2>
	         <!--Optional:-->
	         <urn:Closure_Product_Category_Tier3></urn:Closure_Product_Category_Tier3>
	         <!--Optional:-->
	         <urn:Closure_Product_Model_Version></urn:Closure_Product_Model_Version>
	         <!--Optional:-->
	         <urn:Closure_Product_Name></urn:Closure_Product_Name>
	         <!--Optional:-->
	         <urn:Department></urn:Department>
	         <urn:First_Name></urn:First_Name>
	         <urn:Impact>{}</urn:Impact>
	         <urn:Last_Name></urn:Last_Name>
	         <!--Optional:-->
	         <urn:Lookup_Keyword></urn:Lookup_Keyword>
	         <!--Optional:-->
	         <urn:Manufacturer></urn:Manufacturer>
	         <!--Optional:-->
	         <urn:Product_Categorization_Tier_1></urn:Product_Categorization_Tier_1>
	         <!--Optional:-->
	         <urn:Product_Categorization_Tier_2></urn:Product_Categorization_Tier_2>
	         <!--Optional:-->
	         <urn:Product_Categorization_Tier_3></urn:Product_Categorization_Tier_3>
	         <!--Optional:-->
	         <urn:Product_Model_Version></urn:Product_Model_Version>
	         <!--Optional:-->
	         <urn:Product_Name></urn:Product_Name>
	         <!--Optional:-->
	         <urn:Resolution></urn:Resolution>
	         <!--Optional:-->
	         <urn:Resolution_Category_Tier_1></urn:Resolution_Category_Tier_1>
	         <!--Optional:-->
	         <urn:Resolution_Category_Tier_2></urn:Resolution_Category_Tier_2>
	         <!--Optional:-->
	         <urn:Resolution_Category_Tier_3></urn:Resolution_Category_Tier_3>
	         <urn:Service_Type>{}</urn:Service_Type>
	         <urn:Status>{}</urn:Status>
	         <urn:Action></urn:Action>
	         <!--Optional:-->
	         <urn:Create_Request></urn:Create_Request>
	         <urn:Summary>{}</urn:Summary>
	         <!--Optional:-->
	         <urn:Notes>{}</urn:Notes>
	         <urn:Urgency>{}</urn:Urgency>
	         <!--Optional:-->
	         <urn:Work_Info_Summary></urn:Work_Info_Summary>
	         <!--Optional:-->
	         <urn:Work_Info_Notes></urn:Work_Info_Notes>
	         <!--Optional:-->
	         <urn:Work_Info_Type></urn:Work_Info_Type>
	         <!--Optional:-->
	         <urn:Work_Info_Date></urn:Work_Info_Date>
	         <!--Optional:-->
	         <urn:Work_Info_Source></urn:Work_Info_Source>
	         <!--Optional:-->
	         <urn:Work_Info_Locked>No</urn:Work_Info_Locked>
	         <!--Optional:-->
	         <urn:Work_Info_View_Access>Internal</urn:Work_Info_View_Access>
	         <!--Optional:-->
	         <urn:Middle_Initial></urn:Middle_Initial>
	         <!--Optional:-->
	         <urn:Status_Reason></urn:Status_Reason>
	         <!--Optional:-->
	         <urn:Direct_Contact_First_Name></urn:Direct_Contact_First_Name>
	         <!--Optional:-->
	         <urn:Direct_Contact_Middle_Initial></urn:Direct_Contact_Middle_Initial>
	         <!--Optional:-->
	         <urn:Direct_Contact_Last_Name></urn:Direct_Contact_Last_Name>
	         <!--Optional:-->
	         <urn:TemplateID></urn:TemplateID>
	         <!--Optional:-->
	         <urn:ServiceCI></urn:ServiceCI>
	         <!--Optional:-->
	         <urn:ServiceCI_ReconID></urn:ServiceCI_ReconID>
	         <!--Optional:-->
	         <urn:HPD_CI></urn:HPD_CI>
	         <!--Optional:-->
	         <urn:HPD_CI_ReconID></urn:HPD_CI_ReconID>
	         <!--Optional:-->
	         <urn:HPD_CI_FormName></urn:HPD_CI_FormName>
	         <!--Optional:-->
	         <urn:WorkInfoAttachment1Name></urn:WorkInfoAttachment1Name>
	         <!--Optional:-->
	         <urn:WorkInfoAttachment1Data>cid:717964040312</urn:WorkInfoAttachment1Data>
	         <!--Optional:-->
	         <urn:WorkInfoAttachment1OrigSize></urn:WorkInfoAttachment1OrigSize>
	         <!--Optional:-->
	         <urn:Login_ID>{}</urn:Login_ID>
	         <!--Optional:-->
	         <urn:Customer_Company></urn:Customer_Company>
	         <!--Optional:-->
	         <urn:Corporate_ID></urn:Corporate_ID>
	         <!--Optional:-->
	         <urn:MNM_Chatbot_ID>{}</urn:MNM_Chatbot_ID>
	         <!--Optional:-->
	         <urn:Reported_Source>{}</urn:Reported_Source>
	         <!--Optional:-->
	         <urn:Submitted_By></urn:Submitted_By>
	         <!--Optional:-->
	         <urn:Asset_List></urn:Asset_List>
	         <!--Optional:-->
	         <urn:Phone_Number></urn:Phone_Number>
	      </urn:HelpDesk_Submit_Service>
	   </soapenv:Body>
	</soapenv:Envelope>""".format(Assigned_Group, Impact, Service_Type, Status, Summary, Notes, Urgency, Corporate_ID, MNM_Chatbot_ID, Reported_Source)
	headers = {
	    'content-type': "text/xml",
	    'soapaction': "urn:HPD_IncidentInterface_Create_WS",
	    'cache-control': "no-cache"
	    }

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

	print("-------------- +++++++++++++++ {}".format(response.text))

#not being used this function
def status_ticket_bmc(ticket_number):
	Reported_Source = "Chatbot"
	url = "http://10.2.146.76:8081/arsys/WSDL/public/mmkndremapp-dev/MNM_HPD_IncidentInterface_GetStatus_WS"
	port = 'HPD_IncidentInterface_WSPortStatusSoap'
	cl = Client(url)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	response =cl.service.Get_Operation(Incident_Number=ticket_number,Reported_Source=Reported_Source)
	status = str(response["Status"])
	status_comment = str(response["Status_Reason"])
	return status,status_comment
###########################

def unresolved_ticket_list(Corporate_ID):
	recent_open_tickets = {}
	query_string = """'Customer Login ID'="{}" and 'Status' &lt; "Resolved" """.format(Corporate_ID)
	url = "http://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/HPD_IncidentInterface_WS"
	#url = "http://10.2.146.76:8081/arsys/WSDL/public/mmkndremapp-dev/HPD_IncidentInterface_WS"
	port = "HPD_IncidentInterface_WSPortTypeSoap"
	if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
	cl = Client(url)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	try:
		response = cl.service.HelpDesk_QueryList_Service(query_string)
		for i in range(len(response)-1,-1,-1):
			if len(recent_open_tickets) >= 10:
				break
			category1 = response[i].Categorization_Tier_1
			category2 = response[i].Categorization_Tier_2
			category3 = response[i].Categorization_Tier_3
			if category1 and category2 and category3:
				recent_open_tickets[response[i].Incident_Number] = [category1,category2,category3]
			else:
				recent_open_tickets[response[i].Incident_Number] = response[i].Summary.encode('ascii', 'ignore')
		return recent_open_tickets
	except:
		return recent_open_tickets

def ticket_status_details(ticket_number):
	url = "http://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/HPD_IncidentInterface_WS"
	#url = "http://10.2.146.76:8081/arsys/WSDL/public/mmkndremapp-dev/HPD_IncidentInterface_WS"
	port = "HPD_IncidentInterface_WSPortTypeSoap"
	if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
	cl = Client(url)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	response = cl.service.HelpDesk_Query_Service(ticket_number)
	return response["Status"],response["Status_Reason"],response["Assigned_Group"],response["Assignee"]

def create_ticket_work_order(**kwargs):
	Corporate_ID = str(kwargs.get("Corporate_ID"))
	Summary = str(kwargs.get("Summary"))
	# Urgency = str(kwargs.get("Urgency"))
	# Impact = str(kwargs.get("Impact"))]
	Priority = "L3"
	Request_Type = str(kwargs.get("Request_Type"))
	Assigned_Group = str(kwargs.get("Assigned_Group"))
	Status = "Assigned"
	# Service_Type = "User Service Request"
	Reported_Source = "Chatbot"
	MNM_Chatbot_ID = str(kwargs.get("MNM_Chatbot_ID"))
	Notes = str(kwargs.get("Notes"))

	#url = "http://10.2.146.76:8081/arsys/WSDL/public/10.2.146.76/WorkOrder_interface_Create_WS_"
	url = "http://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/WorkOrder_interface_Create_WS_"
	port = "WOI_Create_ServiceSoap"
	if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
	cl = Client(url)
	cl = Client(url,proxy=proxy_setting)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	ticket_number = cl.service.WOI_WorkOrder_Create_WS(RequestType_CP=Request_Type,Status=Status,RequesterLoginID=Corporate_ID,Summary=Summary,Detailed_Description=Notes,Support_Group_Name=Assigned_Group,MNM_Chatbot_ID=MNM_Chatbot_ID,Reported_Source=Reported_Source,Priority=Priority,Msolve="mSolve")
	return str(ticket_number)

def unresolved_ticket_list_work_order(Corporate_ID):
	recent_open_tickets = {}
	query_string = """ 'Requestor ID'="{}" AND 'Status' &lt; "Completed" """.format(Corporate_ID)
	#url = "http://10.2.146.76:8081/arsys/WSDL/public/10.2.146.76/WorkOrder_Interface_Get" 
	url = "http://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/WorkOrder_Interface_Get"
	port = "WOI_PortSoap"
	if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
	cl = Client(url)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)

	try:
		response = cl.service.WOI_WorkOrder_Getlist(query_string)
		for i in range(len(response)-1,-1,-1):
			if len(recent_open_tickets) >= 10:
				break
			category1 = response[i].Categorization_Tier_1
			category2 = response[i].Categorization_Tier_2
			category3 = response[i].Categorization_Tier_3
			if category1 and category2 and category3:
				recent_open_tickets[response[i].Work_Order_ID] = [category1,category2,category3]
			else:
				recent_open_tickets[response[i].Work_Order_ID] = response[i].Description.encode('ascii', 'ignore')
		return recent_open_tickets
	except:
		return recent_open_tickets

def get_open_tickets_by_user(token_number):
        d1 = unresolved_ticket_list_work_order(token_number)
        d2 = unresolved_ticket_list(token_number)
        if d1 and d2:
                d = od()
                d.update(d1)
                d.update(d2)
                return d
        elif d1 and not d2:
                return d1
        elif d2 and not d1:
                return d2
        else:
                return {}

def ticket_status_details_work_order(ticket_number):
	#url = "http://10.2.146.76:8081/arsys/WSDL/public/10.2.146.76/WorkOrder_Interface_Get" 
	url = "http://servicedesk.mahindra.com/arsys/WSDL/public/itsmremars/WorkOrder_Interface_Get"
	port = "WOI_PortSoap"
	if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
	cl = Client(url)
	user = cl.factory.create('AuthenticationInfo')
	user['userName'] = 'ChatBotUser'
	user['password'] = 'password'
	cl.set_options(soapheaders=user)
	cl.set_options(port=port)
	response = cl.service.WOI_Workorder_get(ticket_number)
	return response["Status"],response["Status_Reason"],response["Support_Group_Name"],response["Assigned_To"]

def get_ticket_status_details(ticket_number):
        if ticket_number.upper().startswith("INC"):
                return ticket_status_details(ticket_number)
        else:
                return ticket_status_details_work_order(ticket_number)
