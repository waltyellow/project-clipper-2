__author__ = 'navyakandkuri'
import sys
import getopt
import string
from senticnet.senticnet import Senticnet

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

# sn = Senticnet()
# concept_info = sn.concept('football')
# polarity_value = sn.polarity_value('love')
# polarity_intense = sn.polarity_intense('love')
# moodtags = sn.moodtags('love')
# semantics = sn.semantics('love')
# sentics = sn.sentics('love')
# print(concept_info)


def word_emotion(word,sn):
    concept_info = sn.concept(word)
    print word, ":", concept_info


def sentics_values(word,sn,comment_sentics):
    word_sentics = sn.sentics(word)
    #print "word sentics ", word_sentics
    for key in comment_sentics:
        comment_sentics[key] = float(comment_sentics[key]) + float(word_sentics[key])
        #print key, comment_sentics[key]
    #print "comment sentics ", comment_sentics


def comment_sentics_average(word_count,comment_sentics):
    for key in comment_sentics:
        comment_sentics[key] = float(comment_sentics[key])/word_count

def add_mood_tags(comment_mood_tags,sn,word):
    current_tags = sn.moodtags(word)
    #print word, current_tags
    for tag in current_tags:
        if tag not in comment_mood_tags:
            comment_mood_tags.append(tag)

def word_parser(comment):
    sn = Senticnet()
    polarity_intense = 0
    comment_sentics = {'sensitivity': 0, 'attention': 0, 'pleasantness': 0, 'aptitude': 0}
    comment_mood_tags = []
    words = comment.split(" ")
    total_word_count = len(words)
    for i in words:

        try:
            #word_emotion(i, sn)
            polarity_intense += float(sn.polarity_intense(i))
            #print sn.sentics(i)
            sentics_values(i,sn,comment_sentics)
            add_mood_tags(comment_mood_tags,sn,i)
        except KeyError:
            #print "This word does not exist", i
            if(total_word_count>1):
                total_word_count -= 1
            pass
    comment_sentics_average(total_word_count,comment_sentics)
    print "comment sentics", comment_sentics
    print "polarity intense: ",polarity_intense/total_word_count
    print "mood tags:", comment_mood_tags

def fileOpen(filename):
    fp = open(filename)
    lines = fp.read().splitlines()
    for line in lines:
        print line.translate(None,string.punctuation)
        word_parser(line.translate(None,string.punctuation))



def main(argv):
    input_comment = input("please enter comment:")
    input_comment.translate(None,string.punctuation)
    word_parser(input_comment.translate(None,string.punctuation))
    #input_file = input("enter file name")
    #fileOpen(input_file)

if __name__ == "__main__":
    main(sys.argv[1:])


