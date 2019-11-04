import json
import re
import datetime
import pymongo
import sys
sys.path.insert(0, '/var/www/html')
from file_paths import *

#mongodb client connection
con = pymongo.MongoClient('ntech.mahindra.com',27017)

#database collection variable
mongo_path_frontend_error = con.mSolve.FrontendError
frontend_error_collection = mongo_path_frontend_error

#method to push the details into mongodb
def push_frontend_error_mongo(sessionId,**kwargs):
	mongo_resp_row = frontend_error_collection.find_one({"sessionId":sessionId})
	if mongo_resp_row:
		for key,value in kwargs.items():
			frontend_error_collection.update_one({"sessionId":sessionId},
				{"$set": {key:value} })
	else:
		frontend_error_collection.insert_one({"sessionId" : sessionId})

def application(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		request_type = environ.get('CONTENT_TYPE')
		request_method = environ.get('REQUEST_METHOD')
		if request_method.lower() not in ["post"]:
			status = '406 Unacceptable'
			response_headers = [('Content-type', 'application/json')]
			start_response(status,response_headers)
			return json.dumps({"status":"false", "Error" : "Sorry, only POST request allowed."})
		elif not request_type or request_type.lower() not in ["application/json"]:
			status = '406 Unacceptable'
			response_headers = [('Content-type', 'application/json')]
			start_response(status,response_headers)
			return json.dumps({"status":"false", "Error" : "Sorry, only 'application/json' allowed."})
	except (ValueError):
		request_body_size = 0

	request_body = environ['wsgi.input'].read(request_body_size)

	print("request body {}".format(request_body))

	try:
		raw_request_json = json.loads(request_body)
		# get the request variables
		sessionId = raw_request_json.get("sessionId","")
		error_message = raw_request_json.get("error_message","")
		corporate_id = raw_request_json.get("corporate_id","")
	except Exception as e:
		d = cgi.parse_qs(environ['QUERY_STRING'])
		# get the request variables
		sessionId = d.get('sessionId',[''])[0]
		error_message = d.get('error_message',[''])[0]
		corporate_id = d.get('corporate_id',[''])[0]

	if not sessionId or not error_message or not corporate_id:
		status = '406 Unacceptable'
		response_headers = [('Content-type', 'application/json')]
		start_response(status,response_headers)
		return json.dumps({"status":"false", "Error" : "Sorry, one or more parameters are missing."})
	else:
		push_frontend_error_mongo(sessionId)
		push_frontend_error_mongo(sessionId,corporate_id=corporate_id,error_message=error_message,TS=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		status = '200 OK'
		response_headers = [('Content-type', 'application/json')]
		start_response(status,response_headers)
		return json.dumps({"status":"true", "Message" : "Successful."})
