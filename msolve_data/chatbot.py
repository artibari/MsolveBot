import sys
sys.path.insert(0, '/var/www/html')
from nearest_meaning import get
import csv

class Chatbot:
	def get_response(self, input_statement):
		response = get(input_statement)
		print("Santosh was here...{}".format(response))
		with open("/var/www/html/training_data.csv") as f:
			for i in csv.reader(f):
				if i[0] == response:
					return i[1]
