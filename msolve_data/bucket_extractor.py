import random
from random import choice, sample, randint
import datetime
import re
import json

def findWholeWord(w):
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def extract_buckets(input_statement):
	#input_statement = input_statement.lower()
	with open("D:\\NEW MSOLVE\\msolve_data\\buckets.json") as bucket_file:
	    bucketData = json.load(bucket_file)

	hash_string_replace = {}

	# hash_string_replace['no water supply'] = ['no water']
	# hash_string_replace['geyser work'] = ['hot water']
	# hash_string_replace['power fluctuation'] = ['fluctuation','fluctuations']

	for key,value in hash_string_replace.items():
		for v in value:
			if input_statement.find(v) != -1:
				input_statement = input_statement.replace(v,key)

	replace_string = []
	for key,value in bucketData["replace_by_word"].items():
		if type(value) is list:
			for v in value:
				if findWholeWord(v)(input_statement) is not None:
					replace_string.append(v)
		else:
			# replace_string = value
			replace_string.append(value)

		if replace_string:
			for elem in replace_string:
				input_statement = input_statement.replace(elem,key)


	print("Input Statement is ************---------{}".format(input_statement))   

	input_tokens = input_statement.split(" ")
	#print "Santosh inputTokens.........{}".format(input_tokens)

	j = 0
	count = 0

	for i in input_tokens:
		for keys,values in bucketData["synonym_dict"].items():
			if i == keys:
				break
			else:
				for value in values:
					if i.lower() == value:
						input_tokens[j] = keys
						break
		j+=1

	input = " ".join(input_tokens)

	##print("dkjfkdjfkdjkfjdk util {}".format(input))

	bucket_list = bucketData["bucket_priority_list"]

	bucket_token = ""
	for k in bucket_list:
		if k in input_tokens:
			bucket_token = k
			break

	keyword_in_input = []

	for i in bucket_list:
		if i in input_tokens:
			keyword_in_input.append(i)


	input_tokens_list = input.split(" ")


	if bucket_token in bucketData["syn_keyword_list"]:
		cnt = 0
		for i in input_tokens_list:
			for keys,values in bucketData[bucket_token].items():
				if i == keys:
					break
				else:
					for value in values:
						if i == value:
							input_tokens_list[cnt] = keys
							break
			cnt+=1

	transformed_input = " ".join(input_tokens_list)

	sub_bucket = ""
	for k in bucketData["sub_bucket_priority_list"]:
		if k in input_tokens_list:
			sub_bucket = k
			break

	##print("sub bucket tokennnn util.......... {}".format(sub_bucket))

	##print("main bucket token util.......{}".format(bucket_token))

	####

	if sub_bucket and not bucket_token:
		if sub_bucket in bucketData["no_priority"]:
			sub_bucket = ""
	##print("after removal sub token util...... {}".format(sub_bucket))

	##print("final input statement @@@@ --------------- {}".format(transformed_input))
	#print "Santosh is testing...........1.{}2.{}3.{}4.{}".format(bucket_token,sub_bucket,keyword_in_input,transformed_input)
	return bucket_token,sub_bucket,keyword_in_input,transformed_input


def getRandomApology():
	msgList=['I understand your issue.','Thanks for telling me your problem.','Thanks for telling me your issue.']
	msg=random.choice(msgList)
	return msg

def getGreetings(input_statement):
	msg = ""
	replyMsg = []
	reply_list = ["Hey xyz, please tell me the problem you are facing.","Hi xyz, tell me the issue you are facing."]
	greetings_dict = {
		"hi" : 3,
		"hello" : 3,
		"hey" : 3,
		"how are you" : 5,
		"how r u" : 5
	}

	for key,value in greetings_dict.items():
		if key in input_statement.lower() and len(input_statement.split()) <= value:
			msg = key
	if not msg:
		msg = input_statement
		replyMsg = [msg,False]
	else:
		msg = random.choice(reply_list)
		replyMsg = [msg,True]
	return replyMsg

def getPraiseWords(input_statement):
	msg = ""
	replyMsg = []
	reply_list = ["Happy to help you xyz.","Glad to help you out xyz. Have a nice day.","Fantastic! I'm so glad to be of help."]
	greetings_dict = {
		"thank you" : 3,
		"thankyou" : 3,
		"thank-you" : 3,
		"cool" : 3,
		"awesome" : 3,
		"great" : 3,
		"okay" : 3,
		"ok" : 3,
		"thanks" : 3,
		"sure" : 3,
		"bye" : 3,
		"thnx" : 3
	}

	input_word_list = input_statement.lower().split()

	for key,value in greetings_dict.items():
		if key in input_word_list and len(input_word_list) <= value:
			msg = key
	if not msg:
		msg = input_statement
		replyMsg = [msg,False]
	else:
		msg = random.choice(reply_list)
		replyMsg = [msg,True]
	return replyMsg
