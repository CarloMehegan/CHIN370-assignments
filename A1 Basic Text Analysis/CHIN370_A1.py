#Carlo Mehegan
#CHIN370

with open('crazy_rich_asians_screenplay.txt', 'r', encoding='utf8') as read_file:
	text = read_file.read()

#clean the text - remove punctuation and capitalization
text = text.lower()
punctuation = [",", ".", ":", "?", "!", "\n", "-", "--", "(", ")"]
for symbol in punctuation:
	text = text.replace(symbol, " ")

#lexical diversity
text_words = text.split(" ")
unique_words = set(text_words)
lexical_diversity = len(unique_words) / len(text_words)

#word frequency
word_freq_dictionary = {}
for word in unique_words:
    #ignore empty strings
    if word != "":
        word_freq_dictionary[word] = text_words.count(word)

#print lexical diversity
print("Lexical diversity:", lexical_diversity)

#print top ten most frequent words
sorted_word_frequency_list = sorted(word_freq_dictionary, key=word_freq_dictionary.get, reverse=True)
print("Ten most frequent words:", sorted_word_frequency_list[:100])