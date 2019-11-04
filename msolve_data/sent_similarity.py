from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def penn_to_wn(tag):
	if tag.startswith('N'):
		return 'n'
	if tag.startswith('V'):
		return 'v'
	if tag.startswith('J'):
		return 'a'
	if tag.startswith('R'):
		return 'r'

def lemmatize(word, tag):
	wn_tag = penn_to_wn(tag)
	if wn_tag is None:
		return None
	return lemmatizer.lemmatize(word, wn_tag)

def tagged_to_synset(word, tag):
	wn_tag = penn_to_wn(tag)
	if wn_tag is None:
		return None
	try:
		return wn.synsets(word, wn_tag)[0]
	except:
		return None

def sentence_similarity(sentence1, sentence2):
	sentence1 = pos_tag(word_tokenize(sentence1))
	sentence2 = pos_tag(word_tokenize(sentence2))

	# print "+++++++++++++++ {}".format(sentence1)

	sent1 = [lemmatize(*i) for i in sentence1]
	sent2 = [lemmatize(*i) for i in sentence2]

	sentence1 = pos_tag(filter(None, sent1))
	sentence2 = pos_tag(filter(None, sent2))

	# print "************** {}".format(sentence1)

	synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
	synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

	synsets1 = [ss for ss in synsets1 if ss]
	synsets2 = [ss for ss in synsets2 if ss]

	score, count = 0.0, 0

	for synset in synsets1:
		li = [max(synset.path_similarity(ss), ss.path_similarity(synset)) for ss in synsets2]
		if li:
			best_score = max(li)
		else:
			best_score = 0
		if best_score is not None:
			score += best_score
			count += 1

	if count > 0:
	# print li
		score /= count
	return score

# print sentence_similarity("For local conveyance, this group will be governed by our policy on Local Conveyance.".lower(), "are we covered any medical policies")

def jac_sim(sentence1, sentence2):
	sentence1 = pos_tag(word_tokenize(sentence1))
	sentence2 = pos_tag(word_tokenize(sentence2))

	sent1 = [lemmatize(*i) for i in sentence1]
	sent2 = [lemmatize(*i) for i in sentence2]
	
	sentence1 = set(filter(None, sent1))

	sentence2 = set(filter(None, sent2))

	intersect = sentence1.intersection(sentence2)
	return float(len(intersect)) / (len(sentence1)+len(sentence2)-len(intersect))


def cosine_sim(sentence1, sentence2):
	import math
	from collections import Counter

	sentence1 = pos_tag(word_tokenize(sentence1))
	sentence2 = pos_tag(word_tokenize(sentence2))

	sent1 = [lemmatize(*i) for i in sentence1]
	sent2 = [lemmatize(*i) for i in sentence2]

	tf1 = Counter(filter(None, sent1))
	tf2 = Counter(filter(None, sent2))

	norm1 = math.sqrt(sum([x**2 for x in tf1.values()]))
	norm2 = math.sqrt(sum([x**2 for x in tf2.values()]))

	vect1 = [float(x)/norm1 for x in tf1.values()]
	vect2 = [float(x)/norm2 for x in tf2.values()]

	return sum(x*y for x,y in zip(vect1, vect2))

def term_freq(term, doc):
	doc_tokens = doc.lower().split()
	return doc_tokens.count(term.lower())/float(len(doc_tokens))


# query = "life learning"
# doc1 = "The game of life is a game of everlasting learning"
# doc2 = "The unexamined life is not worth living"
# doc3 = "Never stop learning"
# li = [doc3, doc2, doc1]
# for i in li:
# 	print cosine_sim(query.lower(), i.lower())

# print term_freq("game", doc1)

# q = "printer ink"
# d1 = "printer issue"
# d2 = "printer ink over"
# d3 = "printer"

# li = [d3,d2,d1]
# for i in li:
# 	print "{} ==> {} ==> {}".format(i, q, cosine_sim(q.lower(), i.lower()))
	# print "{} ==> {} ==> {}".format(i, q, sentence_similarity(q.lower(), i.lower()))
	# print "{} ==> {} ==> {}".format(i, q, jac_sim(q.lower(), i.lower()))
