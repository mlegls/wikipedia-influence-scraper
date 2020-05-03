# Wikipedia Influence Scraper
Scrapes influences from Wikipedia; graphs it (except not yet)

## Parts
Everything is build on scrapy. The main robot is at [wis/wis/spiders/influence_spider.py](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/spiders/influence_spider.py). The executable python file is at [wis/wis/run.py](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/run.py).

[graph.gml](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/graph.gml) and [thinkers.json](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/thinkers.json) were scraped starting from [Deleuze](https://en.wikipedia.org/wiki/Gilles_Deleuze). They may comprehensively span all Wikipedia pages with or directed to from "**Influences**" and "**Influenced**" infobox section links, but I'm not sure.

![image-20200502232514106](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502232514106.png)

## How to Use (Gephi)

The easiest way to see cool stuff is by importing [graph.gml](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/graph.gml) (Graph Markup Language) into a program like [Gephi](https://gephi.org/). Gephi has its own [quickstart tutorial](https://gephi.org/tutorials/gephi-tutorial-quick_start.pdf), but here are my some of my own recommendations. 

*Warning: may take pretty significant CPU/GPU power. It's a large graph (5061 nodes, 11374 edges)*

### Quickstart

**1** 

First open graph.gml (from "Open Graph File..." or File>Open) in Gephi, and select Graph Type "Directed". Hit OK.

![image-20200502214316419](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502214316419.png)

Everything will initially be all clustered together in an illegible square. To make things prettier, first use the "ForceAtlas 2" Layout with as many threads as possible, and tinker around with the settings. Play around with the other layouts too to get different-looking graphs.

*Tip: start with "Approximate Repulsion" on, and a super high scaling (around 1000). Then turn "Approximate Scaling" off and "Prevent Overlap" on, and reduce "Tolerance (speed)"*

At this point, if you haven't already, turn labels on from the bottom menu. Also run the "Label Adjust" Layout so they don't overlap.

![image-20200502224532107](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502224532107.png)

**2**

Run some tests from the right menu. "HITS", "Modularity", and "PageRank" are fun ones.

![image-20200502224742193](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502224742193.png)

You can visualize data (from your tests) from the top left menu. Factors are color, size, font color, and font size. Choose the factor from the top four icons, then Nodes>Ranking, and select the measure you want to visualize.

![image-20200502225548250](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502225548250.png)

![image-20200502225921942](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502225921942.png)

![image-20200502230017622](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502230017622.png)

![image-20200502230039423](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502230039423.png)

You can run "Label Adjust" again if they start overlapping.

![image-20200502230205781](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502230205781.png)

**3**

Just play around lol. Maybe read Gephi's own [docs](https://gephi.org/users/) too.

## How to Use (Other)

You can get other file formats and stuff by playing around with run.py, especially lines 15 and 25. See NetworkX documentation [here](https://networkx.github.io/documentation/stable/reference/readwrite/index.html), Scrapy documentation [here](https://docs.scrapy.org/en/latest/topics/feed-exports.html).

### Formats

The key NetworkX data structure is a graph with page names (or infobox entries without pages) regexed to remove parentheses (see spiders/influence_spider.py line 34, 54-55, 62-63) as node names, and directed edges from each node to the nodes that "influenced" it. Think of an edge from x to y as "x cites y"; this is so metrics like PageRank make sense.

The key Scrapy item (representing one thinker, or Wikipedia page) is defined in [items.py](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/items.py). It has four fields: name—same as the NetworkX node name, link—url (note that this is the redirect url and not the final page url, so there are a few redundancies where the same page has multiple redirects-to), influences—a list of deparentheses-regexed names which should be the same (where they have a page) as the name fields of the thinkers listed by Wikipedia as the thinker's "**Influences**" in the infobox, influenced—same as influenced, but for the "**Influenced**" section of the infobox.

Note that only things with existing Wikipedia pages have a Scrapy item (though many have empty *influences* and *influenced* fields), but all mentions in any page's infobox "**Influences**" and "**Influenced**" sections, including those without actual pages, are in the NetworkX data structure.

Also note that not all nodes (including Scrapy items) are actual people. There are pages like "[Taoism](https://en.wikipedia.org/wiki/Taoism)" and "[Byzantine science](https://en.wikipedia.org/wiki/Byzantine_science)" sometimes listed in Wikipedia's infobox influence sections.

### Python Console

You can edit the python files directly and execute run.py, but you can also import run.py in a Python terminal, and the spider will run automatically (it'll take a while). Also import [globfile.py](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/wis/wis/globfile.py), and you can play around with the global data structures directly. globfile.thinkers will be a list of all "Thinker" class Scrapy items (as defined in items.py), and globfile.full_graph is the complete NetworkX graph.

## Contributing

### Web App

I want to put this on the Web. Running the scraper live probably wouldn't be practical, so I'm thinking having the generated data hosted somewhere, and some kind of front-end interface to browse a graph visualization. 

Speculative features: search for a particular page/thinker; click on nodes to go to Wikipedia page or for more info; see graph centered around a particular thinker; see stats like degree directly for each node 

I have no idea about anything web front-end related, so I'm not gonna be the one to do this.

### Bugfixes

I'm not sure how comprehensive the Deleuze graph is. It could already span all Wikipedia thinkers listed as influencing or being influenced by another, but if you find an exception, let me know, or generate the data yourself with that page added to the start_urls (you'd have to change line 20 of run.py to take the list itself instead of a string in it), and submit a pull request.

 Also, the scraper supports two types of infoboxes. The most common collapsible one, like for [Gilles Deleuze](https://en.wikipedia.org/wiki/Gilles_Deleuze) (shown above), and an alternate non-collapsible one, like for [Gregory Bateson](https://en.wikipedia.org/wiki/Gregory_Bateson).

![image-20200502235319838](https://github.com/mlegls/wikipedia-influence-scraper/blob/master/readme-images/image-20200502235319838.png)

I'm not sure if there are other infobox formats that are not being scraped. If there are, please let me know or make the changes yourself in spiders/influence_spider.py (add conditions after lines 55 and 63), and submit a pull request.

### Other

Any other pull requests are also welcome. For major changes, please open an issue first to discuss what you would like to change.

For changes that alter the output files, please keep the original graph.gml and thinkers.json in the repo, unless the change is a strict improvement (and specify why).

## License

[MIT](https://choosealicense.com/licenses/mit/)
