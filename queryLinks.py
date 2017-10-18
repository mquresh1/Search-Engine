import json
from collections import defaultdict
from bs4 import BeautifulSoup, SoupStrainer
import bs4


# Import bookkeeping file, indices, and PageRank map
def importIndex():
    bookkeeping = json.load(open('/webpages_raw/bookkeeping.json'))
    inverted = json.load(open('inverted.json'))
    special = json.load(open('special.json'))
    pageranks = json.load(open('pageranks'))
    return bookkeeping, inverted, special, pageranks


def query(q, bookkeeping, inverted, special, pageranks):
    visited = defaultdict(bool)
    tagWeights = {'title': 3.0, 'bold': 1.2, 'h1':1.5, 'h2':1.4, 'h3':1.3}
    q = q.lower().split()

    # Map URLs to their TF-IDF scores
    champion_list = {}

    # First try and find the keyword in the special index, and if found, record a net TF-IDF for each URL
    for keyword in q:
        if keyword in special:
            # Loop through the highest weighest tags first
            for tag in sorted(tagWeights, key=lambda x: x[1], reverse=True):
                if tag in special[keyword]:
                    for entry in special[keyword][tag]:
                        url = entry[0]
                        # Only count TF-IDF for keywords that haven't been seen yet in this URL
                        if not visited[url]:
                            if url not in champion_list:
                                champion_list[url] = entry[2]
                            else:
                                champion_list[url] += entry[2]
                            visited[url] = True
            # Reset the visited set when moving on to the next keyword
            visited = defaultdict(bool)

    # Then try and find the keyword in the inverted index, if found and the word wasn't already accounted for when 
    # looking in the special index, add to the current TF-IDF score
    for keyword in q:
        if keyword in inverted:
            for entry in inverted[keyword]:
                url = entry[0]
                if url not in champion_list:
                    champion_list[url] = entry[3]
                elif len(entry[2]) == 0: # dont double count
                    champion_list[url] += entry[3]
    
    # Sort the list of possible champions by their TF-IDF score
    links = sorted(champion_list, key=champion_list.get, reverse=True)

    # Find the top 5 URLs ordered by TF-IDF and find each URL's PageRank
    url_to_pageRank = []
    for link in links[:5]:
        url_to_pageRank.append((link, pageranks[link]))

    # Order these 5 urls by their page rank
    urls = sorted(url_to_pageRank, key=lambda x: x[1], reverse=True)
    return [url[0] for url in urls]

# Pull the title from each URL's HTML response if possible and also generate a snippet of text for display in the GUI
def getPreview(links, bookkeeping):
    titles = []
    urls = []
    previews = []

    # Loop through all the links returned by the query and parse through their HTML responses
    for link in links:
        with open('/webpages_raw/'+link, encoding='utf-8') as rawData:
            soup = BeautifulSoup(rawData.read(), "lxml")
            tags = ['h1', 'h2', 'h3', 'h4', 'p', 'li', 'table', 'address']
            snippit = ''
            for child in soup.recursiveChildGenerator():
                if child.name in tags:
                    # join lines of text so they look nice
                    segment = " ".join(word for word in child.get_text().strip().split() if word)
                    if segment:
                        snippit += segment if snippit == '' else ' ' + segment

                # Break when we have a large enough snippet
                if len(snippit) > 200:
                    break
            
            # If there was a title in the HTML text, grab it, else pull the first 50 characters from the snippet
            if soup.title and soup.title.string:
                titles.append(soup.title.string[:100])
            else:
                titles.append(snippit[:50] + '...')

            urls.append(bookkeeping[link])
            previews.append(snippit[:200] + '...')

    return titles, urls, previews

