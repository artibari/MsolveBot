import sklearn
import dill
import json
import ast
import sys
sys.path.insert(0,'/var/www/html')
from sklearn.feature_extraction.text import TfidfVectorizer

def prediction(input_statement, output_class):
	# with open("/var/www/html/training_data.pk") as f:
	# 	training_data = dill.load(f)

	with open("/var/www/html/tfidf_pkl.pk") as f:
		loaded_tfidf = dill.load(f)

	# tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words='english')
	# tfidf.fit_transform(training_data["Issue"]).toarray()

	with open("/var/www/html/trained_model_pkl.pk") as f:
		loaded_model = dill.load(f)

	# pred = loaded_model.predict(tfidf.transform([input_statement]))
	pred = loaded_model.predict(loaded_tfidf.transform([input_statement]))
	return output_class[pred[0]]

def application(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		request_type = environ.get('CONTENT_TYPE')
		request_method = environ.get('REQUEST_METHOD')

	except (ValueError):
		request_body_size = 0

	request_body = environ['wsgi.input'].read(request_body_size)
	raw_request_json = json.loads(request_body)
	input_statement = raw_request_json.get("input_query", "")
	output_class = raw_request_json.get("labels", "")
	output_class = ast.literal_eval(output_class)

	status = '200 OK'

	response_headers = [('Content-type', 'application/json')]

	reply = prediction(input_statement, output_class)

	start_response(status, response_headers)

	return json.dumps(reply)
