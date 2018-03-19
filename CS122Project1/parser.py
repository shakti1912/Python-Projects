# get names from list here
# check nltk
import pickle
import nltk
import re

# f = open('data.p', 'r')   # 'rb' for reading binary file
# x = 0
# mydict = {}
# mydict = pickle.load(f)
# print mydict



#print mydict[2]
#test_list = mydict[2]['http://www.newyorksocialdiary.com/party-pictures/2007/the-new-york-philharmonic-symphony-space']
names_set = set()


def parse_names(names_list):
    for sentence in names_list:

        if len(sentence) > 250:
            continue
        else:   # parse names
            couples = couples_case(sentence)

            if type(couples) == tuple:
                names_set.add(couples[0])
                names_set.add(couples[1])
            else:
                try:
                    tokenized_sent = nltk.word_tokenize(sentence)
                except UnicodeDecodeError:
                    continue;

                tagged_sent = nltk.pos_tag(tokenized_sent)

                chunks = nltk.ne_chunk(tagged_sent)
                names = []
                for chunk in chunks:
                    if type(chunk) == nltk.tree.Tree:
                        if chunk.label() == 'PERSON':
                            names.append(' '.join([c[0] for c in chunk]))
                #print names
                # add to the names_set
                names_set.update(names)

    print names_set


def couples_case(sentence):
    p = r'^[A-Z][a-z]*' + ' and ' + '[A-Z][a-z]*' + ' ' + '[A-Z][a-z]*$'
    y = re.findall(p, sentence)
    if len(y) != 0:
        x = re.split(' and ', y[0])
        husband = x[len(x) - 1].split(' ')
        c1 = x[0] + ' ' + husband[1]
        c2 = x[1]
        couples = (c1, c2)
        return couples
    else:
        return sentence

# sentence = "Andrea and Osceola Davis"
# print couples_case(sentence)

#parse_names(test_list)

