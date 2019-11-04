import json
import re
import sys
sys.path.insert(0, '/var/www/html')
from file_paths import *
from bucket_extractor import *

def getResponse(input_statement):
	from chatbot import Chatbot
	bot = Chatbot()

	with open(answers_json) as ans:
		ans_json = json.load(ans)

	input_statement = re.sub(r'[^a-zA-Z0-9-:.@/ ]', '',input_statement).strip()
	input_statement = ' '.join(input_statement.split())

	bucket,sub_bucket,_,_ = extract_buckets(input_statement.lower())
	reply = bot.get_response(input_statement)
	print("reply ---- {}".format(reply))

	if bucket and sub_bucket:
		reply = reply
	elif bucket and not sub_bucket:
		reply = reply
	elif not bucket and sub_bucket:
		reply = ""
	else:
		reply = ""

	reply = str(reply)
	if not reply:
		suggestions = ""
	else:
		suggestions = ans_json[reply]["category"]
	replyJson = {"suggestions":suggestions}
	return replyJson

def application(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		request_type = environ.get('CONTENT_TYPE')
		request_method = environ.get('REQUEST_METHOD')

	except (ValueError):
		request_body_size = 0

	request_body = environ['wsgi.input'].read(request_body_size)
	raw_request_json = json.loads(request_body)
	input_statement = raw_request_json.get("chatInput","")

	status = '200 OK'

	response_headers = [('Content-type', 'application/json')]

	reply = getResponse(input_statement+" hello ")

	start_response(status, response_headers)

	return json.dumps(reply)

