# # information-extraction.py
#
# import re
# import nltk
# nltk.download('words')
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
#
# string = """Elizabeth Ballard"""
#
#
# def ie_preprocess(document):
#     document = ' '.join([i for i in document.split() if i not in stop])
#     print document
#     sentences = nltk.sent_tokenize(document)
#     sentences = [nltk.word_tokenize(sent) for sent in sentences]
#     sentences = [nltk.pos_tag(sent) for sent in sentences]
#     return sentences
#
#
# def extract_names(document):
#     names = []
#     sentences = ie_preprocess(document)
#     for tagged_sentence in sentences:
#         for chunk in nltk.ne_chunk(tagged_sentence):
#             if type(chunk) == nltk.tree.Tree:
#                 if chunk.label() == 'PERSON':
#                     names.append(' '.join([c[0] for c in chunk]))
#     return names
#
# if __name__ == '__main__':
#     names = extract_names(string)
#     print names
#
#
import nltk
import re
sentence = "Andrea McCormick and Osceola Davis"

p = '[A-Z][a-z]*' + ' and ' + '[A-Z][a-z]*' + ' ' + '[A-Z][a-z]*$'
pattern = [p]

y = re.findall(p, sentence)
x = re.split(' and ', sentence)
husband = x[len(x)-1].split(' ')
print x[0] + ' ' + husband[1]
print x[1]

# tokenized_sent = nltk.word_tokenize(sentence)
#
# tagged_sent = nltk.pos_tag(tokenized_sent)
#
# chunks = nltk.ne_chunk(tagged_sent)
# names = []
# for chunk in chunks:
#     print (chunk)
#     if type(chunk) == nltk.tree.Tree:
#         if chunk.label() == 'PERSON':
#             names.append(' '.join([c[0] for c in chunk]))
#
# print names


