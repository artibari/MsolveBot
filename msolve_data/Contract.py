from random import choice, sample, randint
from IPy import IP
from bson import json_util
import bson
import sys
import pytz
import datetime
import time
import re
import json
import csv
import urllib
import string
import random
import hunspell
sys.path.insert(0, '/var/www/html')
from file_paths import *	
from dateutil.parser import parse
import requests
import cgi
import ast
from bucket_extractor import *
from soap_api_module import *
from msolve_soap_apis import *
from send_mail import *
from bs4 import BeautifulSoup
from collections import OrderedDict as od
from ml_model_api_module import prediction
import traceback

import logging
# import logging.config
# logger = logging.getLogger(__name__)

# with open("/var/www/html/logging.json") as f:
# 	config_dict = json.load(f)

# logging.config.dictConfig(config_dict)

# logger.info('it works')
# logging.info("does it work")

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler('/var/www/html/info.log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# logger.info('Hello baby')

coll1 = mongo_path_mSolve_lastResp
collection = mongo_path_mSolve_convoLogs
userDetailsCollection = mongo_path_mSolve_userDetails
ticket_details_collection = mongo_path_mSolve_ticketDetails
ticket_archieve_collection = mongo_path_mSolve_ticketArchieve
bmc_error_collection = mongo_path_mSolve_bmcError
unclassified_query_collection = mongo_path_unclassifiedQueries

from chatbot import Chatbot
bot = Chatbot()

def findWholeWord(w):
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def idGenerator(size=10, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

def ticketGenerator(size=5, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def getPhoneNumber(input_statement):
	match = re.findall(r'(?:s*\d{1}[\s-]*)?(?:s*\d{2}[\s-]*)?(?:\d[-\s]*){10}', input_statement)
	return match

def chatEnable(chat_type,**kwargs):
	if chat_type != "grid" and chat_type != "radio" and chat_type != "rating" and chat_type != "card" and chat_type != "dropdown" and chat_type != "phone":
		return "true"
	else:
		if kwargs.get("force_enable_flag"):
			return "true"
		else:
			return "false"

def get_unresolved_ticket_list(cont_id):
	ticket_dictionary = get_open_tickets_by_user(cont_id)
	if ticket_dictionary:
		return [[i,filter(None,ticket_dictionary[i])] for i in ticket_dictionary]
	else:
		return None

def handleSingleWords(answerId):
	with open("/var/www/html/mSolvebot_response.json") as resp_file:
		respData = json.load(resp_file)
	reply_string = ""
	if answerId == "id-129":
		reply_string = respData["id-1005"]["answer"]
	return reply_string

def get_assigned_group(user_location,company_division,user):
	print "user location ................ {}".format(user_location)
	group = {}
	'''if user == "MSolve":
		group_json = "/var/www/html/bmc_assigned_group.json"
	elif user == "BMC":
		group_json = "/var/www/html/msolve_assigned_group.json"'''
	group_json = "/var/www/html/msolve_assigned_group.json"
	with open(group_json) as f:
		jData = json.load(f)

	for key,value in jData.items():
		# if user_location.lower() in key:
		if key in user_location.lower():
			group = value
			break

	if not group:
		return "mSolve Central Helpdesk"
		#return "IT-INFRA-HELPDESK-KND AD"

	# print "hhhhhhhhhhhhhhhhhh value {} type {}".format(group,type(group))

	print "company division ---------- {}".format(company_division)

	# if kwargs.get("secretary_flag"):
	# 	return group.get("secretary")

	print "group dict ----------- {}".format(group)

	for key,value in group.items():
		print "key ---- {} company_division ...... {}".format(key,company_division.lower())
		if key.lower() in company_division.lower():
			return value
	else:
		if group.get("default"):
			return group["default"]
		else:
			return group[group.keys()[0]]

def pushLastResponseInMongo(sessionId,response,category,sub_bucket,query,count,bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type):
	coll1.insert_one({
		"_sessionId":sessionId,
		"lastResp":response,
		"category":category,
		"sub_bucket":sub_bucket,
		"lastQuery":query,
		"count_rep":count,
		"bucket":bucket,
		"note_flag":note_flag,
		"chat_stage":chat_stage,
		"ticket_number":ticket_number,
		"session_ended":session_ended,
		"ticket_type":ticket_type
		})

def pushLastResponseInMongoBMC(sessionId,response,category,sub_bucket,query,count,bucket,note_flag,chat_stage,ticket_number,session_ended):
        coll1.insert_one({
                "_sessionId":sessionId,
                "lastResp":response,
                "category":category,
                "sub_bucket":sub_bucket,
                "lastQuery":query,
                "count_rep":count,
                "bucket":bucket,
                "note_flag":note_flag,
                "chat_stage":chat_stage,
                "ticket_number":ticket_number,
                "session_ended":session_ended
                })

def pushUserDetailsToMongo(sessionId,**kwargs):
	user_details_row = userDetailsCollection.find_one({"sessionId":sessionId})
	if user_details_row:
		# for loop for accessing values from the keyword arguments 
		for key,value in kwargs.items():
			userDetailsCollection.update_one({"sessionId":sessionId},
					{"$set": {key:value} })
	else:
		userDetailsCollection.insert_one({"sessionId" : sessionId})

def push_to_ticket_archieve_mongo(sessionId,**kwargs):
	ticket_details_rows = ticket_archieve_collection.find_one({"sessionId":sessionId})
	if ticket_details_rows:
		for key,value in kwargs.items():
			ticket_archieve_collection.update_one({"sessionId":sessionId},
				{"$set": {key:value} })
	else:
		ticket_archieve_collection.insert_one({"sessionId" : sessionId})

def push_ticket_details_mongo(sessionId,**kwargs):
	ticket_details_row = ticket_details_collection.find_one({"sessionId":sessionId})
	if ticket_details_row:
		# FOR loop to access values from the keyword arguments 
		for key,value in kwargs.items():
			ticket_details_collection.update_one({"sessionId":sessionId},
					{"$set": {key:value} })
	else:
		ticket_details_collection.insert_one({"sessionId" : sessionId})

def push_bmc_API_error_details_mongo(sessionId,**kwargs):
	error_detail_row = bmc_error_collection.find_one({"sessionId":sessionId})
	if error_detail_row:
		for key,value in kwargs.items():
			bmc_error_collection.update_one({"sessionId":sessionId},
					{"$set": {key:value} })
	else:
		bmc_error_collection.insert_one({"sessionId" : sessionId})

def push_unclassified_queries_mongo(sessionId,**kwargs):
	response = unclassified_query_collection.find_one({"sessionId":sessionId})
	if response:
		for key,value in kwargs.items():
			unclassified_query_collection.update_one({"sessionId":sessionId},
					{"$set": {key:value} })
	else:
		unclassified_query_collection.insert_one({"sessionId" : sessionId})

def pushConversationLogsToMongo(sessionId,time,uMessage,bMessage,user_name,cont_id,notes):
	if collection.find({"sessionId":{"$in":[sessionId]}}).count()>0:
		collection.update_one({"sessionId":sessionId},
			{"$push":{
				"convo":{
					"User":uMessage,
					"Bot":bMessage,
					"TS":time
							}
					},
			"$set":{
					"user_name":user_name,
					"cont_id":cont_id,
					"notes":notes
				}
			})
	else:
		collection.insert_one({
			"sessionId":sessionId,
			"user_name":user_name,
			"cont_id":cont_id,
			"notes":notes,
			"chatbot_tag":"MSolve",
			"convo":[{
				"user":uMessage,
				"Bot":bMessage,
				"TS":time
				}]
		})

def getResponse(input_statement,sessionId,response,cont_id):
	note_flag = False
	lastResponse = ""
	lastQuery = ""
	chat_type = "chat"
	chat_stage="0"
	replyVal = ""
	values = {}
	count_reply = 0
	session_ended = "false"
	vip_list = ["PU","AU","GP","AV","BR"]

	user_name = assigned_group = company_address = company_division =  dbBucket = mongo_bucket = sub_bucket = category = ticket_number = notes = user_problem_query = category_detected = force_enable_flag = ""
	Corporate_ID = Summary = Urgency = Impact = Assigned_Group = MNM_Chatbot_ID = Notes = user_role_band = ticket_type = user = ""
	output_class = ['Incident','Service Request']
	suggestion_enable = False

	print "Santosh Pal is not a Premanent Employee======{}".format(user)
	with open(answers_json) as answer_file:
		answersData = json.load(answer_file)

	with open("/var/www/html/mSolvebot_response.json") as resp_file:
		respData = json.load(resp_file)

	last_resp_row = coll1.find({"_sessionId":sessionId}).sort( [{ "_id",-1 }] ).limit(1)
	if last_resp_row:
		mongoObjjson = json.dumps(list(last_resp_row),default=json_util.default)
		mongoObjjson = json.loads(mongoObjjson)
		mongoObjjson = filter(None,mongoObjjson)
		if mongoObjjson:
			lastResponse = mongoObjjson[0].get('lastResp')
			category = mongoObjjson[0].get('category')
			sub_bucket = mongoObjjson[0].get('sub_bucket')
			lastQuery = mongoObjjson[0].get('lastQuery')
			count_reply = mongoObjjson[0].get('count_rep')
			mongo_bucket = mongoObjjson[0].get('bucket')
			note_flag = mongoObjjson[0].get('note_flag')
			chat_stage = mongoObjjson[0].get('chat_stage')
			ticket_number = mongoObjjson[0].get('ticket_number')	
			ticket_type = mongoObjjson[0].get('ticket_type')


	# user_details_row = userDetailsCollection.find({"sessionId":sessionId}).sort( [{ "_id",-1 }] )
	user_details_row = userDetailsCollection.find({"cont_id":cont_id}).sort( [{ "_id",-1 }] ).limit(1)
	if user_details_row:
		mongoObjjson = json.dumps(list(user_details_row),default=json_util.default)
		mongoObjjson = json.loads(mongoObjjson)
		mongoObjjson = filter(None,mongoObjjson)
		if mongoObjjson:
			user_name = mongoObjjson[0].get('user_name')
			company_address = mongoObjjson[0].get('company_address')
			company_division = mongoObjjson[0].get('company_division')
			role = mongoObjjson[0].get('role')
			manager_id = mongoObjjson[0].get('reports_to')
			manager_role_band = mongoObjjson[0].get('manager_role_band')
			user_role_band = mongoObjjson[0].get('user_role_band')
			mobile = mongoObjjson[0].get('mobile')
			user = mongoObjjson[0].get('user')


	ticket_details_row = ticket_details_collection.find({"sessionId":sessionId}).sort( [{ "_id",-1 }] ).limit(1)
	if ticket_details_row:
		mongoObjjson = json.dumps(list(ticket_details_row),default=json_util.default)
		mongoObjjson = json.loads(mongoObjjson)
		mongoObjjson = filter(None,mongoObjjson)
		if mongoObjjson:
			Corporate_ID = mongoObjjson[0].get('Corporate_ID')
			Summary = mongoObjjson[0].get('Summary')
			asset = mongoObjjson[0].get('asset')
			request_type_id = mongoObjjson[0].get('request_type_id')
			Assigned_Group = mongoObjjson[0].get('Assigned_Group')
			MNM_Chatbot_ID = mongoObjjson[0].get('MNM_Chatbot_ID')
			Notes = mongoObjjson[0].get('Notes')


	input_statement = re.sub(r'[^a-zA-Z0-9-:.@/ ]', '',input_statement).strip()
	input_statement = ' '.join(input_statement.split())
	print "---------------- =++++++++++++++ this is inp {}".format(input_statement)

	greet = getGreetings(input_statement)
	#praise = getPraiseWords(input_statement)
	praise = ""

	if input_statement == "createit":
		replyVal = respData["id-1015"]["answer"]
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		replyJson["data"]=values
		note_flag = False
		chat_stage="0"
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"True"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		'''if user == "MSolve":
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,"",count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		elif user == "BMC":
			pushLastResponseInMongoBMC(sessionId,replyVal,category,sub_bucket,"",count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended)'''
		pushLastResponseInMongoBMC(sessionId,replyVal,category,sub_bucket,"",count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended)
		pushConversationLogsToMongo(sessionId,convoTime,"Create Ticket",replyVal,user_name,cont_id,Notes)
		return replyJson
	elif input_statement == "statusit":
		ticket_list = get_open_tickets_by_user(cont_id)
		if ticket_list:
			ticket_dict = od()
			for i in ticket_list:
				print "ticketttttttttttttt listttttttttttt {}".format(ticket_list)
				ticket_dict[i] = i+":"+str(ticket_list[i])
			replyVal = respData["id-1016"]["answer"]
			ticket_list = od(sorted(ticket_list.items(),reverse=True))
			#values = ticket_list
			values = ticket_dict
			# card_values = card_dictionary
			replyJson = {"reply":replyVal}
			replyJson["data"]=values
			chat_stage = "checkstatus"
			force_enable_flag = "on"
			chat_type = "card"
		else:
			# replyVal = respData["id-1017"]["answer"]
			replyVal = respData["id-1024"]["answer"]
			replyJson = {"reply":replyVal}
			# values = {"createit":"Create Ticket","statusit":"Check Ticket Status"}
			values = {"createit":"Create Ticket"}
			chat_stage = "checkstatus"
			# session_ended = "true"
			force_enable_flag = "on"
			chat_type = "radio"
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
			# replyJson["card_data"] = card_values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		'''if user == "MSolve":
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		elif user == "BMC":
			pushLastResponseInMongoBMC(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended)'''
		pushLastResponseInMongoBMC(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended)
		pushConversationLogsToMongo(sessionId,convoTime,"Check Ticket Status",replyVal,user_name,cont_id,Notes)
		return replyJson

	elif input_statement == "incidentreq":
		replyVal = "Alright.</br>Please elaborate your issue.</br>So that our support team can help you better."
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		chat_stage = "incident_req_notes"
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	elif input_statement == "servicereq":
		replyVal = "Got it.</br>Please elaborate your issue.</br>So that our support team can help you better."
		replyJson = {"reply":replyVal}
		chat_stage = "service_req_notes"
		note_flag = True
		if values:
			replyJson["data"]=values
		replyJson.update({"chat_type":chat_type})
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson
	else:
		pass

	if chat_stage == "sop":
		if input_statement.lower() == "yeshelpful":
			replyVal = "Great " + user_name +". Happy to help you. </br> Have a nice day."
			replyJson = {"reply":replyVal}
			chat_type = "radio"
			replyJson.update({"chat_type":chat_type})
			values = {"createit":"Create Ticket","statusit":"Ticket Status"}
			session_ended = "true"
		elif input_statement.lower() == "nothelpful":
			predicted_class = prediction(lastQuery, output_class)
			#replyVal = "Alright <b>"+user_name+"</b>.</br>I understand that you're trying to raise a ticket for <b>{}</b>, click continue, to proceed with the same.</br>Else, select a different option from below.".format(predicted_class)
			replyVal = "Alright.</br>Please elaborate your issue.</br>So that our support team can help you better."
			#chat_type = "radio"
			suggestion_enable = False
			note_flag = True
			if predicted_class == "Incident":
				chat_stage = "incident_req_notes"
				#values = {"servicereq":"Service Request", "incidentreq":"Continue"}
			else:
				chat_stage = "service_req_notes"
				#values = {"incidentreq":"Incident", "servicereq":"Continue"}
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	elif chat_stage == "ticket_notes":
		Notes = input_statement
		if len(input_statement.split()) < 2:
			replyVal = "That message is too short. Please input a proper message."
			replyJson = {"reply":replyVal}
			chat_stage = "ticket_notes"
			note_flag = True
			if values:
				replyJson["data"]=values
			replyJson.update({"chat_type":chat_type})
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson
		else:
			ticket_type = "unidentified"
			resp = requests.request("get","https://emss.mahindra.com/sap/bc/zhr_tq_emp_det?sap-client=500&IV_PERNR="+Corporate_ID)
			resp_list = resp.text.split("-//-")
			print "Unidentified Service REQUEST....{}".format(resp_list)
			try:
				mobile = resp_list[18]
				pushUserDetailsToMongo(sessionId, mobile=mobile)
			except:
				mobile = ""
			if len(mobile) >= 10:
				replyVal = "Your registered mobile number with us is <b>{}</b>.</br>If you want to create ticket with a different mobile number, please type below.</br><b>Skip</b>, to continue with the registered mobile number.".format(mobile)
				values = {"skip":"Skip"}
				chat_type = "radio"
				force_enable_flag = "on"
			else:
				replyVal = "Please enter your mobile number."
			replyJson = {"reply":replyVal}
			chat_stage = "mobile_servicereq"
			note_flag = True
			if values:
				replyJson["data"]=values
			replyJson.update({"chat_type":chat_type})
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson

	elif chat_stage == "service_req_notes":
		Notes = input_statement
		if len(input_statement.split()) < 2:
			replyVal = "That message is too short. Please input a proper message."
			replyJson = {"reply":replyVal}
			chat_stage = "service_req_notes"
			note_flag = True
			if values:
				replyJson["data"]=values
			replyJson.update({"chat_type":chat_type})
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson	
		else:
			ticket_type = "service request"
			resp = requests.request("get","https://emss.mahindra.com/sap/bc/zhr_tq_emp_det?sap-client=500&IV_PERNR="+Corporate_ID)
			resp_list = resp.text.split("-//-")
			try:
				mobile = resp_list[18]
				pushUserDetailsToMongo(sessionId, mobile=mobile)
			except:
				mobile = ""
			if len(mobile) >= 10:
				replyVal = "Your registered mobile number with us is <b>{}</b>.</br>If you want to create ticket with a different mobile number, please type below.</br><b>Skip</b>, to continue with the registered mobile number.".format(mobile)
				values = {"skip":"Skip"}
				chat_type = "radio"
				force_enable_flag = "on"
			else:
				replyVal = "Please enter your mobile number."
			replyJson = {"reply":replyVal}
			chat_stage = "mobile_servicereq"
			note_flag = True
			if values:
				replyJson["data"]=values
			replyJson.update({"chat_type":chat_type})
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson

	elif chat_stage == "incident_req_notes":
		Notes = input_statement
		if len(input_statement.split()) < 2:
			replyVal = "That message is too short. Please input a proper message."
			replyJson = {"reply":replyVal}
			replyJson.update({"chat_type":chat_type})
			chat_stage = "incident_req_notes"
			note_flag = True
			if values:
				replyJson["data"]=values
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson
		else:
		
			ticket_type = "incident"
			resp = requests.request("get","https://emss.mahindra.com/sap/bc/zhr_tq_emp_det?sap-client=500&IV_PERNR="+Corporate_ID)
			resp_list = resp.text.split("-//-")
			print "Incident Service REQUEST....{}".format(resp_list)
			try:
				mobile = resp_list[18]
				print "MOBILE==========={}".format(mobile)
				pushUserDetailsToMongo(sessionId, mobile=mobile)
			except:
				mobile = ""
			if len(mobile) >= 10:
				replyVal = "Your registered mobile number with us is <b>{}</b>.</br>If you want to create ticket with a different mobile number, please type below.</br><b>Skip</b>, to continue with the registered mobile number.".format(mobile)
				values = {"skip":"Skip"}
				chat_type = "radio"
				force_enable_flag = "on"
			else:
				replyVal = "Please enter your mobile number."
			replyJson = {"reply":replyVal}
			replyJson.update({"chat_type":chat_type})
			chat_stage = "mobile_incidentreq"
			note_flag = True
			if values:
				replyJson["data"]=values
			chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
			replyJson.update({"chatEnable":chat_enable})
			replyJson.update({"suggestion_enable":"False"})
			replyJson.update({"session_ended":session_ended})
			convoTime = datetime.datetime.now()
			push_ticket_details_mongo(sessionId,Notes=Notes)
			pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
			pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
			return replyJson

	elif chat_stage == "msolve_address_incidentreq":
		asset_dict = get_asset_by_user(cont_id)
		replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
		if input_statement.lower() == "skip":
			location = company_address
			assigned_group = get_assigned_group(location,company_division,user)
			push_ticket_details_mongo(sessionId,Assigned_Group=assigned_group)
			print "gggggggggrouppppppppppp 1"+assigned_group
		else:
			location_list = []
			with open("/var/www/html/mahindra_location_list.csv") as f:
				location_data = csv.reader(f)
				for i in location_data:
					location_list.append(i[0].lower())

			location_details = input_statement.lower().split(" - ")
			if len(location_details) > 1:
				location_input = location_details[0].strip()
				company_division = location_details[1].strip()
			else:
				location_input = location_details[0].strip()

			if str(location_input) in location_list:
				location = location_input
				assigned_group = get_assigned_group(location,company_division,user)
				push_ticket_details_mongo(sessionId,Assigned_Group=assigned_group)
				print "gggggggggrouppppppppppp 2"+assigned_group
			else:
				note_flag = True
				chat_stage = "msolve_address_incidentreq"
				chat_type = "address"
				replyVal = "Please enter a valid location."
				replyJson = {"reply":replyVal}
				replyJson.update({"chat_type":"chat"})
				replyJson.update({"chatEnable":"true"})
				replyJson.update({"suggestion_enable":"False"})
				replyJson.update({"session_ended":"false"})
				return replyJson

		replyVal = "Okay.</br>Please, select an asset from below for which you're trying to raise an Incident ticket."
		values = asset_dict
		chat_type = "dropdown"
		chat_stage = "ticket_confirmation"
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson
	
	if chat_stage == "mobile_incidentreq":
		mobile_number = getPhoneNumber(input_statement)
		if input_statement.lower() == "skip":
			push_ticket_details_mongo(sessionId,Mobile_Num=mobile)
			replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
			chat_stage = "msolve_address_incidentreq"
			values = {"skip":"Skip"}
			force_enable_flag = "on"
			chat_type = "address"
		elif mobile_number:
			mobile_number = int(mobile_number[0])
			push_ticket_details_mongo(sessionId,Mobile_Num=mobile_number)
			replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
			chat_stage = "msolve_address_incidentreq"
			values = {"skip":"Skip"}
			force_enable_flag = "on"
			chat_type = "address"
		else:
			replyVal = "Please, enter a valid mobile number."
			chat_stage = chat_stage
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	elif chat_stage == "msolve_address_servicereq":
		request_types = get_all_request_types()
		replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
		if input_statement.lower() == "skip":
			location = company_address
			assigned_group = get_assigned_group(location,company_division,user)
			push_ticket_details_mongo(sessionId,Assigned_Group=assigned_group)
			print "gggggggggrouppppppppppp 3"+assigned_group
		else:
			location_list = []
			with open("/var/www/html/mahindra_location_list.csv") as f:
				location_data = csv.reader(f)
				for i in location_data:
					location_list.append(i[0].lower())

			location_details = input_statement.lower().split(" - ")
			if len(location_details) > 1:
				location_input = location_details[0].strip()
				company_division = location_details[1].strip()
			else:
				location_input = location_details[0].strip()

			if str(location_input) in location_list:
				location = location_input
				assigned_group = get_assigned_group(location,company_division,user)
				push_ticket_details_mongo(sessionId,Assigned_Group=assigned_group)
				print "gggggggggrouppppppppppp 4"+assigned_group
			else:
				note_flag = True
				chat_stage = "msolve_address_servicereq"
				chat_type = "address"
				replyVal = "Please enter a valid location."
				replyJson = {"reply":replyVal}
				replyJson.update({"chat_type":"chat"})
				replyJson.update({"chatEnable":"true"})
				replyJson.update({"suggestion_enable":"False"})
				replyJson.update({"session_ended":"false"})
				return replyJson

		replyVal = "Please, select a Service Request type from below."
		values = request_types
		chat_type = "dropdown"
		chat_stage = "ticket_confirmation"
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	elif chat_stage == "mobile_servicereq":
		mobile_number = getPhoneNumber(input_statement)
		if input_statement.lower() == "skip":
			push_ticket_details_mongo(sessionId,Mobile_Num=mobile)
			replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
			chat_stage = "msolve_address_servicereq"
			values = {"skip":"Skip"}
			force_enable_flag = "on"
			chat_type = "address"
		elif mobile_number:
			mobile_number = int(mobile_number[0])
			push_ticket_details_mongo(sessionId,Mobile_Num=mobile_number)
			replyVal = respData["id-1010"]["answer"]+"<br>"+respData["id-1012"]["answer"].replace("xyz-loc",company_address)
			chat_stage = "msolve_address_servicereq"
			values = {"skip":"Skip"}
			force_enable_flag = "on"
			chat_type = "address"
		else:
			replyVal = "Please, enter a valid mobile number."
			chat_stage = chat_stage
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	elif chat_stage == "service_req_dropdown":
		request_type_id = input_statement
		replyVal = "Got it.</br>Please select from below, this service request is for."
		chat_type = "dropdown"
		replyJson = {"reply":replyVal}
		replyJson.update({"chat_type":chat_type})
		values = {"Office Use":"Office Use", "Personal Use":"Personal Use", "others":"Others"}
		note_flag = True
		chat_stage = "ticket_confirmation"
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		push_ticket_details_mongo(sessionId, request_type_id = request_type_id)
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	# elif chat_stage == "service_req_notes":
	# 	note_flag = True
	# 	chat_stage = "last"
	# 	chat_type = "radio"
	# 	values = {"cancel":"Cancel","confirm":"Confirm"}
	# 	replyVal = respData["id-1008"]["answer"]

	
	if chat_stage == "checkstatus":
		if input_statement.upper().startswith("INC") and len(input_statement) == 15 or input_statement.upper().startswith("WO") and len(input_statement) == 15:
		#if input_statement.upper().startswith("IT") and len(input_statement) == 9 or input_statement.upper().startswith("SR") and len(input_statement) == 9:
			try:
				ticket_stat = get_ticket_status_details(input_statement.upper())
				if len(filter(None,ticket_stat)) > 3:
					if ticket_stat[1] and ticket_stat[3]:
						replyVal = "Dear <b>{}</b>. Status of your ticket: <b>{}</b>.</br>Reason for the status is: {}</br>Your ticket has been assigned to: <b>{}</b>.</br>Happy to help you.".format(user_name,ticket_stat[0],ticket_stat[1],ticket_stat[3])
					elif ticket_stat[1] and not ticket_stat[3]:
						replyVal = "Dear <b>{}</b>. Status of your ticket: <b>{}</b>.</br>Reason for the status is: {}</br>Happy to help you.".format(user_name,ticket_stat[0],ticket_stat[1])
					elif ticket_stat[3] and not ticket_stat[1]:
						replyVal = "Dear <b>{}</b>. Status of your ticket: <b>{}</b>.</br>Your ticket has been assigned to: <b>{}</b>.</br>Have a nice day.".format(user_name,ticket_stat[0],ticket_stat[3])
				elif len(filter(None,ticket_stat)) <= 3:
					replyVal = "Dear <b>{}</b>. Status of your ticket: <b>{}</b>.</br>There are no more details yet. Please check back later.</br>Have a nice day.".format(user_name,ticket_stat[0])
				# ticket_stat,comment = status_ticket_bmc(input_statement.upper())
				# replyVal = "Dear " + user_name + ". Status of your ticket - <b>" + ticket_stat + "</b>.</br> Have a nice day."
				replyJson = {"reply":replyVal}
				# chat_type = "radio"
				chat_type = "phone"
				replyJson.update({"chat_type":chat_type})
				values = {"createit":"Create Ticket","statusit":"Ticket Status","phone":"02224915544"}
				session_ended = "true"
				#ticket_stat = get_ticket_status_details(input_statement.upper())
				#if ticket_stat[0] and ticket_stat[2]:
				#	replyVal = "Dear <b>{}</b>. </br>Status of your ticket: <b>{}</b>.</br>Your ticket has been assigned to: <b>{}</b>.</br>Happy to help you.".format(user_name,ticket_stat[0],ticket_stat[2])
				#else:
				#	replyVal = "Dear <b>{}</b>. </br>Status of your ticket: <b>{}</b>.</br>Happy to help you.".format(user_name,ticket_stat[0])
				#replyJson = {"reply":replyVal}
				#chat_type = "phone"
				#replyJson.update({"chat_type":chat_type})
				#values = {"createit":"Create Ticket","statusit":"Ticket Status","phone":"02224915544"}
				#session_ended = "true"
			except:
				replyVal = respData["id-1018"]["answer"]
				replyJson = {"reply":replyVal}
				replyJson.update({"chat_type":chat_type})
			replyJson["data"]=values
			chat_stage = "checkstatus"
		else:
			replyVal = respData["id-1019"]["answer"]
			replyJson = {"reply":replyVal}
			replyJson.update({"chat_type":chat_type})
			replyJson["data"]=values
			chat_stage = "checkstatus"
		note_flag = True
		if values:
			replyJson["data"]=values
		chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
		replyJson.update({"chatEnable":chat_enable})
		replyJson.update({"suggestion_enable":"False"})
		replyJson.update({"session_ended":session_ended})
		convoTime = datetime.datetime.now()
		pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
		pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
		return replyJson

	if chat_stage == "2" or chat_stage == "ticket_confirmation":
		if ticket_type == "incident":
			asset = input_statement
			notes = Notes
			push_ticket_details_mongo(sessionId,asset=asset)
			push_ticket_details_mongo(sessionId,Notes=notes)
		elif ticket_type == "service request":
			#notes = input_statement
			request_type_id = input_statement
			push_ticket_details_mongo(sessionId,request_type_id=request_type_id)
			push_ticket_details_mongo(sessionId,Summary=Summary)
			#push_ticket_details_mongo(sessionId,Notes=notes)
		note_flag = True
		chat_stage = "last"
		chat_type = "radio"
		values = od()
		values["confirm"] = "Confirm"
		values["cancel"] = "Cancel"
		replyVal = respData["id-1008"]["answer"]

	elif chat_stage == "rating":
		feedback = input_statement.split(":")
		if len(feedback) > 1:
			rating, comment = feedback[0], feedback[1]
		else:
			rating = feedback[0]
			comment = ""
		push_to_ticket_archieve_mongo(sessionId, Rating = rating, Comment = comment)
		replyVal = respData["id-1011"]["answer"] + user_name + ", for your feedback."
		values = {"createit":"Create Ticket","statusit":"Ticket Status"}
		chat_type = "radio"
		session_ended = "true"

	elif chat_stage == "last":
		if input_statement == "cancel":
			replyVal = respData["id-1010"]["answer"] + user_name +". "+ respData["id-1009"]["answer"]
			#remove ticket details which have not been created i.e. cancelled ones
			ticket_details_collection.delete_one({"sessionId":sessionId})
			chat_type = "radio"
			values = {"createit": "Create Ticket", "statusit":"Ticket Status"}
			session_ended = "true"
		elif input_statement == "confirm":
			print "CONFRIMATION CLICKED===={}".format(ticket_type)
			user_details_row = userDetailsCollection.find({"cont_id":cont_id}).sort( [{ "_id",-1 }] ).limit(1)
        		if user_details_row:
                		mongoObjjson = json.dumps(list(user_details_row),default=json_util.default)
                		mongoObjjson = json.loads(mongoObjjson)
                		mongoObjjson = filter(None,mongoObjjson)
                		if mongoObjjson:
                        		user = mongoObjjson[0].get('user')	
			if ticket_type == "incident":
				try:
					#ticket_number = create_incident_ticket(token_number=Corporate_ID, mobile_number=mobile, issue=Summary, description=Notes, asset=asset, chatbot_unique_id=sessionId)
					#assigned_gp = get_assigned_group(company_address,company_division)
					#push_to_ticket_archieve_mongo(sessionId, Assigned_Group=assigned_gp)
					print "INCIDENT USER===={}".format(user)
					ticket_number = create_ticket_bmc(user=user, token_number=Corporate_ID, mobile_number=mobile, issue=Summary, description=Notes, asset=asset, chatbot_unique_id=sessionId, Assigned_Group=Assigned_Group)
				except:
					api_error_report = traceback.format_exc()
					send_mail(Corporate_ID,api_error_report,time_stamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), API_name=ticket_type, mobile_number=mobile, issue=Summary, description=Notes, asset=asset)
					push_bmc_API_error_details_mongo(sessionId)
					push_bmc_API_error_details_mongo(sessionId,token_number=Corporate_ID,TS=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),Summary=Summary, API_name=ticket_type, API_error_report=api_error_report,chatbot_tag="MSolve")				
					raise
				push_to_ticket_archieve_mongo(sessionId)
				push_to_ticket_archieve_mongo(sessionId, incidentId = ticket_number,token_number=Corporate_ID, mobile_number=mobile, issue=Summary, description=Notes, asset=asset, chatbot_tag = "MSolve")
			else:
				#try:
					#ticket_number = create_service_req_ticket(token_number=Corporate_ID, mobile_number=mobile, issue=Summary, description=Notes, request_type_id=request_type_id, chatbot_unique_id=sessionId)
				#assigned_gp = get_assigned_group(company_address,company_division)
				#push_to_ticket_archieve_mongo(sessionId, Assigned_Group=assigned_gp)
				print "SERVICE REQUEST USER===={}".format(user)
				ticket_number = create_ticket_work_order(user=user, token_number=Corporate_ID, issue=Summary, description=Notes, request_type_id=request_type_id, chatbot_unique_id=sessionId, Assigned_Group=Assigned_Group)
				#except:
				#	api_error_report = traceback.format_exc()
				#	send_mail(Corporate_ID,api_error_report,time_stamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),API_name=ticket_type, mobile_number=mobile, issue=Summary, description=Notes, request_type_id=request_type_id)
				#	push_bmc_API_error_details_mongo(sessionId)
				#	push_bmc_API_error_details_mongo(sessionId,token_number=Corporate_ID,TS=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),Summary=Summary,API_name=ticket_type,API_error_report=api_error_report,chatbot_tag="MSolve")				
				#	raise
				push_to_ticket_archieve_mongo(sessionId)
				push_to_ticket_archieve_mongo(sessionId, incidentId = ticket_number,token_number=Corporate_ID, mobile_number=mobile, issue=Summary, description=Notes, request_type_id=request_type_id, chatbot_tag = "MSolve")
			# replyVal = respData["id-1011"]["answer"] + user_name +". "+ respData["id-1002"]["answer"].replace('XYZ123',ticket_number)
			replyVal = respData["id-1002"]["answer"].replace('XYZ123',ticket_number)
			chat_type = "rating"
			chat_stage = "rating"
			note_flag = True
			# values = {"statusit":"Check Ticket Status"}
			# force_enable_flag = "on"
			# session_ended = "true"

	query = input_statement

	if note_flag is False:
		if lastQuery:
			query = lastQuery+" "+query

		bucket,sub_bucket,_,_ = extract_buckets(query.lower())

		if not mongo_bucket:
			mongo_bucket = bucket

		reply = bot.get_response(query)

		push_ticket_details_mongo(sessionId)
		push_ticket_details_mongo(sessionId,Summary=query,Corporate_ID=cont_id,MNM_Chatbot_ID=sessionId,chatbot_tag="MSolve")

		print "response ----------------------- {}".format(reply)

		if mongo_bucket and sub_bucket:
			reply = str(reply)
			category = answersData[reply]['answer']

			if category == "Operating Systems > Drivers Installation > Printer driver installation":
				replyVal = respData["id-1021"]["answer"]+"</br></br>"+respData["id-1022"]["answer"]
				note_flag = True
				chat_stage = "sop"
				chat_type = "radio"
				values = { "yeshelpful" : "Yes", "nothelpful" : "No, create ticket." }
				replyJson = {"reply":replyVal}
				replyJson.update({"chat_type":chat_type})
				replyJson["data"]=values
				if values:
					replyJson["data"]=values
				chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
				replyJson.update({"chatEnable":chat_enable})
				replyJson.update({"suggestion_enable":"False"})
				replyJson.update({"session_ended":session_ended})
				convoTime = datetime.datetime.now()
				pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
				pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
				return replyJson
			
			elif category == "Operating Systems > System settings > System proxy settings":
				replyVal = respData["id-1023"]["answer"]+"</br></br>"+respData["id-1022"]["answer"]
				note_flag = True
				chat_stage = "sop"
				chat_type = "radio"
				values = { "yeshelpful" : "Yes", "nothelpful" : "No, create ticket." }
				replyJson = {"reply":replyVal}
				replyJson.update({"chat_type":chat_type})
				replyJson["data"]=values
				if values:
					replyJson["data"]=values
				chat_enable = chatEnable(chat_type,force_enable_flag=force_enable_flag)
				replyJson.update({"chatEnable":chat_enable})
				replyJson.update({"suggestion_enable":"False"})
				replyJson.update({"session_ended":session_ended})
				convoTime = datetime.datetime.now()
				pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,input_statement,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
				pushConversationLogsToMongo(sessionId,convoTime,input_statement,replyVal,user_name,cont_id,Notes)
				return replyJson

			predicted_class = prediction(query, output_class)
			#replyVal = "I understand that you're trying to raise a ticket for <b>{}</b>, click continue, to proceed with the same.</br>Else, select a different option from below.".format(predicted_class)
			#chat_type = "radio"
			replyVal = "Alright.</br>Please elaborate your issue.</br>So that our support team can help you better."
			suggestion_enable = False
			note_flag = True
			if predicted_class == "Incident":
				chat_stage = "incident_req_notes"
				#values = {"servicereq":"Service Request", "incidentreq":"Continue"}
			else:
				chat_stage = "service_req_notes"
				#values = {"incidentreq":"Incident", "servicereq":"Continue"}
			# chat_stage = ""

		elif mongo_bucket and not sub_bucket:
			reply = str(reply)
			category = answersData[reply]['answer']
			single_word_reply = handleSingleWords(reply)
			if single_word_reply:
				replyVal = single_word_reply
			else:

				predicted_class = prediction(query, output_class)
				#replyVal = "I understand that you're trying to raise a ticket for <b>{}</b>, click continue, to proceed with the same.</br>Else, select a different option from below.".format(predicted_class)
				#chat_type = "radio"
				replyVal = "Alright.</br>Please elaborate your issue.</br>So that our support team can help you better."
				session_enable = False
				note_flag = True
				if predicted_class == "Incident":
					chat_stage = "incident_req_notes"
					#values = {"servicereq":"Service Request", "incidentreq":"Continue"}
				else:
					chat_stage = "service_req_notes"
					#values = {"incidentreq":"Incident", "servicereq":"Continue"}
				# chat_stage = ""

		elif sub_bucket and not mongo_bucket:
			count_reply = count_reply+1
			replyVal = respData["id-1003"]["answer"]
			suggestion_enable = True
			if count_reply == 2:
				#predicted_class = prediction(query, output_class)
				#replyVal = "I understand that you're trying to raise a ticket for <b>{}</b>, click continue, to proceed with the same. Else, select a different option from below.".format(predicted_class)
				replyVal = respData["id-1004"]["answer"]+"</br>Please provide few more details about your issue.</br>So that our support team can help you better."
				suggestion_enable = False
				note_flag = True
				chat_stage = "ticket_notes"
				#if predicted_class == "Incident":
				#	values = {"servicereq":"Service Request", "incidentreq":"Continue"}
				#else:
				#	values = {"incidentreq":"Incident", "servicereq":"Continue"}
				# chat_stage = ""
				push_unclassified_queries_mongo(sessionId)
				push_unclassified_queries_mongo(sessionId,Corporate_ID=cont_id,Query=query,chatbot_tag="MSolve")

		elif not mongo_bucket and not sub_bucket:
			count_reply = count_reply+1
			single_word_reply = handleSingleWords(reply)
			if single_word_reply:
				replyVal = single_word_reply
				suggestion_enable = True
			else:
				replyVal = respData["id-1003"]["answer"]
				suggestion_enable = True
			if count_reply == 2:
				#predicted_class = prediction(query, output_class)
				#replyVal = respData["id-1004"]["answer"]+"</br>Please select the type of ticket from below:"
				#chat_type = "radio"
				replyVal = respData["id-1004"]["answer"]+"</br>Please provide few more details about your issue.</br>So that our support team can help you better."
				suggestion_enable = False
				note_flag = True
				chat_stage = "ticket_notes"
				#values = {"servicereq":"Service Request", "incidentreq":"Incident Request"}
				push_unclassified_queries_mongo(sessionId)
				push_unclassified_queries_mongo(sessionId,Corporate_ID=cont_id,Query=query,chatbot_tag="MSolve")

	replyJson = {"reply":replyVal}
	replyJson.update({"chat_type":chat_type})
	replyJson["data"]=values
	if suggestion_enable:
		replyJson.update({"suggestion_enable":"True"})
	else:
		replyJson.update({"suggestion_enable":"False"})
	if values:
		replyJson["data"]=values
	chat_enable = chatEnable(chat_type,force_enable_flag = force_enable_flag)
	replyJson.update({"chatEnable":chat_enable})
	replyJson.update({"session_ended":session_ended})
	convoTime = datetime.datetime.now() 
	if note_flag is not False:
		input_statement = ""

	print "category --- problem category --------------- {}".format(category)

	pushLastResponseInMongo(sessionId,replyVal,category,sub_bucket,query,count_reply,mongo_bucket,note_flag,chat_stage,ticket_number,session_ended, ticket_type)
	pushConversationLogsToMongo(sessionId,convoTime,query,replyVal,user_name,cont_id,Notes)
	return replyJson

def application(environ, start_response):
	session_ended = "false"
	random_number = randint(1, 100000)
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		request_type = environ.get('CONTENT_TYPE')
		request_method = environ.get('REQUEST_METHOD')

		if request_method.lower() not in ["post"]:
			status = '406 Unacceptable'
			response_headers = [('Content-type', 'application/json')]
			start_response(status,response_headers)
			return json.dumps({"Error" : "Sorry, only POST request allowed."})

		#elif not request_type or request_type.lower() not in ["application/json"]:
		#	status = '406 Unacceptable'
		#	response_headers = [('Content-type', 'application/json')]
		#	start_response(status,response_headers)
		#	return json.dumps({"Error" : "Sorry, 'application/json' allowed."})

	except (ValueError):
		request_body_size = 0

	response = {}
	prev_session = ""
	stage_chat = ""

	request_body = environ['wsgi.input'].read(request_body_size)

	print "Santosh Pal is not a Premanent Employee"

	print "request body {}".format(request_body)

	# print "request bodyyyyyyyyyyy {}".format(environ)

	try:
		raw_request_json = json.loads(request_body)

		id = raw_request_json.get("sessionId","")
		input_statement = raw_request_json.get("chatInput","")
		poll_flag = raw_request_json.get("poll_flag")
		user_name = raw_request_json.get("user_name")
		company_name = raw_request_json.get("company_name")
		company_address = raw_request_json.get("company_address")
		company_division = raw_request_json.get("company_division")
		cont_id = raw_request_json.get("cont_id","foo")
		role = raw_request_json.get("designation")
		user_role_band = raw_request_json.get("user_role_band")
		reports_to = raw_request_json.get("reports_to")		#manager's_cont_id
		user = raw_request_json.get("user")
	except Exception as e:
		# d = cgi.parse_qs(request_body)
		# d = parse_qs(request_body)
		d = cgi.parse_qs(environ['QUERY_STRING'])
		id = d.get('sessionId',[''])[0]
		input_statement = d.get('chatInput',[''])[0]
		poll_flag = d.get('poll_flag',[''])[0].lower()
		user_name = d.get('user_name',[''])[0]
		company_name = d.get('company_name',[''])[0]
		company_address = d.get('company_address',[''])[0]
		company_division = d.get('company_division',[''])[0]
		cont_id = d.get('cont_id',[''])[0]
		role = d.get('designation',[''])[0]
		user_role_band = d.get('user_role_band',[''])[0]
		reports_to = d.get('reports_to',[''])[0]	#manager's_cont_id
		user = d.get('user',[''])[0]

	if cont_id.startswith("0"):
		cont_id = cont_id.lstrip("0")

	# if reports_to.startswith("0"):
	# 	reports_to = reports_to.lstrip("0")

	if re.match(r'.*[\%\$\^\*\@\!\_\-\(\)\:\;\'\"\{\}\[\]<>?.,&$#].*', poll_flag):
		status = '406 Unacceptable'
		response_headers = [('Content-type', 'application/json')]
		start_response(status,response_headers)
		return json.dumps({"Error" : "Sorry, special characters are not allowed."})

	input_statement = ''.join([i if ord(i) < 128 else ' ' for i in input_statement])

	if bool(BeautifulSoup(str(input_statement), "html.parser").find()):
		status = '406 Unacceptable'
		response_headers = [('Content-type', 'application/json')]
		start_response(status,response_headers)
		return json.dumps({"Error" : "Sorry, given input is Unacceptable."})

	print "88888888888888888888888888888888 00000 input {} type {}".format(input_statement,type(input_statement))

	status = '200 OK'

	last_resp_row = coll1.find({"_sessionId":id}).sort( [{ "_id",-1 }] )
	if last_resp_row:
		mongoObjjson = json.dumps(list(last_resp_row),default=json_util.default)
		mongoObjjson = json.loads(mongoObjjson)
		mongoObjjson = filter(None,mongoObjjson)
		if mongoObjjson:
			prev_session = mongoObjjson[0].get('_sessionId')
			stage_chat = mongoObjjson[0].get('chat_stage')

	print "prev session id from mongo ---------------- {} chat stage ........... {}".format(prev_session,stage_chat)

	if id == '' or poll_flag == "true":
		id = idGenerator()

	response_headers = [('Content-type', 'application/json')]
	# ip = get_client_address(environ)
	# deviceInfo = get_client_device(environ)
	# status = '200 OK'

	# if session_ended == "true":
	# 	id = idGenerator()

	if poll_flag == "true":
		print "SANTOSH WAS HERE"
		pushUserDetailsToMongo(id)
		pushUserDetailsToMongo(id,user_name = user_name, company_name = company_name, company_address = company_address, company_division = company_division, cont_id = cont_id, role = role, reports_to = reports_to, user_role_band=user_role_band, chatbot_tag = "MSolve", user = user)
		reply = {"sessionId":id}
		tz = pytz.timezone('Asia/Kolkata')
		time=datetime.datetime.now(tz)
		helloMsg=""
		if(time.hour>=4 and time.hour<12):
			helloMsg="Good Morning "
		elif (time.hour>=12 and time.hour<17):
			helloMsg="Good Afternoon "
		else:
			helloMsg="Good Evening "

		helloMsg+="<b>"+user_name+"</b>.</br>"
		helloMsg+="I am Msolve Bot.</br>You can re-start at any time by clicking the restart button at the top right."
		values = {"createit":"Create Ticket","statusit":"Ticket Status"}
		reply.update({"reply":helloMsg})
		reply.update({"data":values})
		reply.update({"chat_type":"radio"})
		reply.update({"chatEnable":"false"})
		reply.update({"session_ended":"false"})
		pushLastResponseInMongo(id,"","","","",0,"","","0","","","")
		# pushLastResponseInMongo(id,helloMsg,"",count_reply,"","1")
		# pushConversationLogsToMongo(id,datetime.datetime.now(),"","","",userId,globalUserName,globalPhoneNo,globalUserType,globalAuthToken)
	else:
		if id != str(prev_session):
			status = '406 Unacceptable'
			response_headers = [('Content-type', 'application/json')]
			start_response(status,response_headers)
			return json.dumps({"Error" : "Sorry, invalid session id."})

		if input_statement:
			# try:
			reply = getResponse(input_statement,id,response,cont_id)
			# except Exception as e:
			# 	logger.error('caught exception in the logger', exc_info=True)
			# 	print "dfdfd ------------ {}".format(e)
			# 	status = "500 Internal Server Error"
			# 	response_headers = [('Content-type', 'application/json')]
			# 	start_response(status, response_headers)
			# 	return json.dumps({"Error":"We're facing technical difficulties at the moment. Please try again after some time."})
			session_flag = reply.get("session_ended")
			if session_flag == "true":
				id = idGenerator()
				pushLastResponseInMongo(id,"","","","",0,"","","0","","","")
			reply.update({"sessionId":id})
			reply.update({"session_ended":session_ended})
		elif not input_statement:
			status = '406 Unacceptable'
			response_headers = [('Content-type', 'application/json')]
			start_response(status,response_headers)
			return json.dumps({"Error" : "chatInput parameter required."})

	start_response(status, response_headers)

	user_details_row = userDetailsCollection.find({"cont_id":cont_id}).sort( [{ "_id",-1 }] ).limit(1)
        if user_details_row:
                mongoObjjson = json.dumps(list(user_details_row),default=json_util.default)
                mongoObjjson = json.loads(mongoObjjson)
                mongoObjjson = filter(None,mongoObjjson)
                if mongoObjjson:
                        user = mongoObjjson[0].get('user')
	
	reply.update({"user":user})
	jsonReply = json.dumps(reply)

	print "44444444444444 reply {}".format(jsonReply)

	return [jsonReply]
