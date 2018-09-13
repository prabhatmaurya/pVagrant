from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def t_search(a,b):
    key_words = []
    b1 = b.split()
    for i in a:
        for j in b1:
            accuracy_value = similar(i,j)
            print "Compare:%s with %s" % (i,j)
            print "accuracy_value:%s" % accuracy_value
            if accuracy_value >= 0.8:
                key_words.append(i)
    return key_words
