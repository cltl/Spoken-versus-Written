from nltk.tokenize import RegexpTokenizer

def prepare_data(inputfile):
	"""
	This functions takes as input a Frog-file with following structure:
	'1	word1_sentence1	[lemma]	POS-tag
	 2	word2_sentence1	[lemma]	POS-tag
	...
	1	word1_sentence_n	[lemma]	POS-tag
	m	word_m_sentence_n	[lemma]	POS-tag'

	The file is transformed into a list (all_lists)
	that contains lists of all sentences (one_list).
	The one_list is a list that consists of 
	(word, POS-tag, lemma)-tuples of each word of the sentence.
	As output, it returns a list (all_lists) that contains lists of tuples.
	"""

	# Read Frog-file.
	text = open(inputfile, 'rt', encoding='latin1') 

	# Initiate empty lists.
	all_lists = []
	one_list = []

	for line in text:
		
		tokenizer = RegexpTokenizer(r'[^\n+\t+]+')
		tokenized = tokenizer.tokenize(line)

		if len(tokenized) > 0:
			if tokenized[0] == '1':  # '1' indicates beginning of sentence.
				one_list = []
			# For each word of the sentence, add a tuple to the sentence list.
			one_list.append((tokenized[1], tokenized[3], tokenized[2]))
			# [1] = word, [3] = POS-tag, [2] = lemma.
		else:
			if len(one_list) > 0:  # Empty line indicates end of sentence.
				# Add the lists of all sentences to a main list.
				all_lists.append(one_list)

	return all_lists