import json
import bs4
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import math
import os


bookkeeping = json.load(open('/webpages_raw/bookkeeping.json'))
stopwords = set(line.strip() for line in open('stopwords.txt'))

# filter out certain html tags
def valid(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    return True

# parse through 'special' html tags and store them into a special index
def findTagsAndIndex(soup, inverted, specialIndex, tag, key):
    taggedLines = soup.findAll(tag)
    wordToIndex = defaultdict(list)
    pos = 0
    
    # Count occurrences of each word and record their relative positions
    if taggedLines:
        for line in taggedLines:
            for word in re.split('[\\W_," ]+', line.get_text().lower()):
                if word.isalnum() and word not in stopwords:
                    wordToIndex[word].append(pos)
                    pos += 1
    # Add the word into the indices as a key and value being 
    # a list of (urlkey, positionsList, specialPositionsList, TFIDF)
    # specialPositionsList is the relative positions list of tagged words
    for word, positions in wordToIndex.items():
        specialIndex[word][tag].append([key, positions, 0])
        inverted[word].append([key, [], positions, 0])

# Construct a 'special' index that contains tagged words and an inverted index that contains all words parsed from the HTML response
# Special Index is of the structure {word : {'title' : [(urlKey1, positions, TF-IDF), (urlKey2, positions, TF-IDF) ...], 'bold' : [(urlKey1, positions, TF-IDF), ...], ...}
# (a word is mapped to a dictionary of tags as keys and values as [urlKey, positionList, TF-IDF])
# Inverted Index is {word : [(urlKey1, positions, specialPositions, TF-IDF), (urlKey2, positions, specialPositions, TF-IDF), ...] }

def constructIndexes(inverted, special):
    # special tags we're paying attention to
    tags = ['title', 'bold', 'h1', 'h2', 'h3']

    # Loop through all HTML files and construct an inverted index and a special index
    for key in bookkeeping:
        pos = 0
        with open('/webpages_raw/'+ key, encoding='utf-8') as rawData:
            wordToIndex = defaultdict(list)
            soup = BeautifulSoup(rawData.read(), "lxml")

            # Construct the special index
            for tag in tags:
                findTagsAndIndex(soup, inverted, special, tag, key)
            
            # Parse through the body of the html
            body = soup.findAll(text=True)
            if body:
                body = filter(valid, body)
            giantString = ''
            for line in body:
                giantString += line
            for word in re.split('[\\W_," ]+', giantString.lower()):
                if word == '' or word in stopwords:
                    continue
                wordToIndex[word].append(pos)
                pos += 1
            
            # Construct the inverted index
            for word, positions in wordToIndex.items():
                if word in special:
                    invertedEntries = inverted[word]
                    added = 0
                    for indx, entry in enumerate(invertedEntries):
                        if key == entry[0]:
                            inverted[word][indx][1] = positions
                            added = True
                            break
                    if not added:
                        inverted[word].append([key, positions, [], 0])
                else:
                    inverted[word].append([key, positions, [], 0])


# Calculate TF-IDF
def tf_idf(inverted, special):
    # 'special' tag weights (multiply TF-IDF by these)
    tagWeights = {'title': 3.0, 'bold': 1.2, 'h1':1.5, 'h2':1.4, 'h3':1.3}
    totalNumDocs = len(bookkeeping)

    # Calculate TF-IDFs for inverted index
    for word, lst in inverted.items():
        IDF = math.log(totalNumDocs / len(lst))
        for indx, entry in enumerate(lst):
            termFreq = 1 + math.log(len(entry[1]) + len(entry[2]))
            tfidf = IDF * termFreq
            inverted[word][indx][3] = tfidf

    # Pull TF-IDF from matching entry in inverted index and update the TF-IDF in the special index entry
    for word, tagDict in special.items():
        for tag, lst in tagDict.items():
            for indx, entry in enumerate(lst):
                url = entry[0]
                invertedEntries = inverted[word]
                for invertedEntry in invertedEntries:
                    if url == invertedEntry[0]:
                        special[word][tag][indx][2] = invertedEntry[3] * tagWeights[tag]
                        break


if __name__ == "__main__":
    inverted = defaultdict(list)
    special = defaultdict(lambda: defaultdict(list))
    constructIndexes(inverted, special)
    tf_idf(inverted, special)
    with open('inverted.json', 'w') as outfile:
        json.dump(inverted, outfile, sort_keys=True)

    with open('special.json', 'w') as outfile:
        json.dump(special, outfile, sort_keys=True)


    totalNumDocs = len(bookkeeping.keys())
    print("Number of documents: ", totalNumDocs)
    vocabSize = len(inverted.keys())
    for key in special.keys():
        if key not in inverted:
            vocabSize += 1
    print("Number of unique words: ", vocabSize)
    print("Size of invertedIndex: ", os.path.getsize('inverted.json'))
    print("Size of special index: ", os.path.getsize('special.json'))
