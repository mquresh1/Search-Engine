import json
import networkx as nx
from networkx.readwrite import json_graph
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin
bookkeeping = json.load(open('/webpages_raw/bookkeeping.json'))
keepbooking = {v: k for k, v in bookkeeping.items()}

graph = nx.DiGraph()
graph.add_nodes_from(bookkeeping.keys())

# Parse through HTML responses and gather up possible links
def gather_links(baseURLKey, html):
    links = []
    for link in BeautifulSoup(html, "lxml", parse_only=SoupStrainer('a')):
        if hasattr(link, "href"):
            url = urljoin(bookkeeping[baseURLKey], link.get('href'))
            
            # Only add into the graph if the link is bookmarked
            if url in keepbooking:
                links.append((baseURLKey, keepbooking[url]))
    return links

# Loop through all links and construct the directed graph 
for k in bookkeeping:
    with open('/webpages_raw/' + k, encoding='utf-8') as rawData:
        links = gather_links(k, rawData.read())
        graph.add_edges_from(links)

# Calculate PageRank
calculated_page_rank = nx.pagerank(graph)

with open('pageranks', 'w') as outfile:
        json.dump(calculated_page_rank, outfile)


