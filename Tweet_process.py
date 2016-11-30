import operator 
import json
from collections import Counter
from collections import defaultdict
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk import bigrams

# Remove punctuation and stop words
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'via', '…']

# Emoticons
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


if __name__ == '__main__':
	filename = 'datascience.json'

	with open(filename, 'r') as f:
		# Intialize the counters
		count_all = Counter()
		count_stop = Counter()
		count_hash = Counter()
		count_only = Counter()
		count_bigrams = Counter()
		com = defaultdict(lambda : defaultdict(int))

		for line in f:
			tweet = json.loads(line)

			# All words, no filter
			terms_all = [term for term in preprocess(tweet['text'])]
			# All words without punctuation and stop-words
			terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
			terms_bigram = bigrams(terms_stop)
			# Count hashtags only
			terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
			# Count terms only (no hashtags, no mentions)
			terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))]

			# Build co-occurrence matrix
			for i in range(len(terms_only)-1):            
				for j in range(i+1, len(terms_only)):
					w1, w2 = sorted([terms_only[i], terms_only[j]])                
					if w1 != w2:
						com[w1][w2] += 1

			com_max = []
			# For each term, look for the most common co-occurrent terms
			for t1 in com:
				t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
				for t2, t2_count in t1_max_terms:
					com_max.append(((t1, t2), t2_count))
			# Get the most frequent co-occurrences
			terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
			#print(terms_max[:5])

			# Update the counter
			count_all.update(terms_all)
			count_stop.update(terms_stop)
			count_hash.update(terms_hash)
			count_only.update(terms_only)
			count_bigrams.update(terms_bigram)
	        #tokens = preprocess(tweet['text'])
			#print(tokens)
			#print(json.dumps(tweet, indent=4)) # pretty-print
		# Print the first 10 most frequent words
		print(count_all.most_common(10))
		print(count_stop.most_common(10))
		print(count_hash.most_common(10))
		print(count_only.most_common(10))
		print(count_bigrams.most_common(10))
		print(terms_max[:5])
