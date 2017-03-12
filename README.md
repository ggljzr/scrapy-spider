# scrapy-spider

This web crawler is designed to extract product information from a popular Czech e-shop [Alza](https://www.alza.cz). As the name suggests, [scrapy](https://scrapy.org/) framework was used to implement the crawler.

This crawler was implemented as a part of web datamining course at [CTU Prague](https://www.cvut.cz/en).

## Extracted data

Alza is a huge e-shop that deals mostly in electronics and digital media (videogames, ebooks, movies etc.). We are interested in following information about each listed product:

* **Name** - Name under which is product listed
* **Price** - Product price (including VAT) in CZK
* **Warranty** - Length of warranty (in months), this should usualy be 24 months or none, due to Czech e-commerce laws
* **Description** - Text description of the product in e-shop
* **Categories** - Under which categories is product listed
* **Rating** - Customers can rate purchased products with 0 to 5 stars
* **Number of ratings** - How many customers have rated the product

Scrapy can export extracted data in a number of [formats](https://doc.scrapy.org/en/latest/topics/feed-exports.html). Example of product's record in **json** would look like this:

```javascript
{
	"price": "249", 
	"warranty": "24", 
	"text_desc": "Štětec na optiku profesionální", 
	"categories": [
		"Foto Audio Video", 
		"Digitální foto", 
		"Příslušenství", 
		"Čisticí sady"
		], 
	"users_rated": "214", 
	"name": "Hama Lenspen", 
	"rating": "4,5"
}
```

## Crawling policies

Alza provides [robots.txt](https://www.alza.cz/robots.txt) file describing how should crawlers process the site. Scrapy respects policies specified in this file by default (variable ``ROBOTSTXT_OBEY`` is set to ``True`` in ``settings.py``).

## Configuration

Scrapy crawlers can be configured via ``settings.py`` file. Here you can set things like ``user-agent`` string, request delays or ``robots.txt`` compliance.

File for this spider can be found in ``ddw_crawler/ddw_crawler/settings.py``.

## Usage

First make sure you have installed Scrapy module (this crawler was implemented with Python 3.5, other versions were not tested but should work too).

```
$ python3.5 -m pip install scrapy
```

Then clone this repo and start crawling:

```
$ git clone https://github.com/ggljzr/scrapy-spider
# here you may want to edit settings.py (user-agent string and such)
$ cd ddw_crawler
$ scrapy crawl alza -o alza.json
```

This will start crawling listed products, while saving data in ``alza.json``. Note that ``alza.json`` file is not overwriten. Instead data from each crawl are appended to the file (so you may want to delete this file before running a new crawl).

## Example

You can see example of gathered data (containing 14592 unique products) [here](https://raw.githubusercontent.com/ggljzr/scrapy-spider/master/examples/alza.json).

# Implementation details

## Basic mechanism

Since Alza [has](https://www.alza.cz/robots.txt) sitemaps in its ``robots.txt`` file, we can use those instead of crawling site itself for links. Sitemap for products looks like this:

```xml
<urlset>
	<url>
		<loc>https://www.alza.cz/hama-lenspen-profesionalni-stetec-d39827.htm</loc>
		<changefreq>weekly</changefreq>
		<priority>1</priority>
	</url>
	...

</urlset>

```

To do this, Scrapy [provides](https://doc.scrapy.org/en/latest/topics/spiders.html#sitemapspider) ``SitemapSpider`` class. This spider parses sitemap ``.xml`` file and starts crawling gathered product links.

You can specify which sitemaps are used in various ways. This crawler uses the most basic one, listing them in ``sitemap_urls`` class variable:

```python

class AlzaSpider(SitemapSpider):
    name = 'alza'

    sitemap_urls = ['https://www.alza.cz/_sitemap-products-1.xml']
    ...

```

## Data extraction

Data from product page are extracted using CSS selectors. For example extracting product name could look like this:

```python

	#response is an object providet by Scrapy
	#containing response to crawler's request
	name = response.css('div#popis h2::text').extract_first()

```

It seems that layout for each page can slightly differ, depending on various factors (product being on sale etc.), so it was necessary to identify and handle these differences.

Another problem with extraction was that some of the content (for example links to related products) on product page was lazy loaded with Javascript, so it was missing from ``response`` to crawler's request.

This did not matter much, since crawler was able to get enough information from loaded content and links to crawl were provided by sitemap.

# Future improvements

It would be nice to be able to crawl lazy loaded content. [One](http://stackoverflow.com/questions/40738264/how-to-scrapy-a-lazy-loading-form) of the ways to do this is to use Scrapy with headless browser like [PhantomJS](http://phantomjs.org/) to do the Javascript rendering.