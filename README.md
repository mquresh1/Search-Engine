# Search Engine
A search engine which creates an inverted index and uses it for repeated queries. Includes a GUI for enhanced user experience.

## How It Works
### indexBuilder
Parses a large amount of raw HTML data in a directory called *webpages_raw* and builds an inverted index. Within this directory is a 
JSON file called *bookkeeping* which maps the filenames with their URL, used for identifying the link during index building and query time.
Unforunately this dataset was too large to include in the repository.

### pageRank
Builds a PageRank graph of the links. PageRank is used to evaluate the "popularity" of a link. After the inverted index is used to pull
top links for a query, the PageRank is used to sort these links so more favorable links appear on top.

### queryLinks
After both the inverted index and PageRank graph are created, they are loaded in so queries can be made. Note that the previous two scripts
only need to be ran once, assuming the *webpages_raw* is unchanged.

### searchGUI
The MAIN script of the program. Essentially provides a user interface to the operations done in *queryLinks* with a search bar at the top
and an organized display of the resulting links below.

## Authors
* Mohammad Qureshi
* Tony Pham
* Andrew Luong
