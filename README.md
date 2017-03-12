# scrapy-spider

This web crawler is designed to extract product information from a popular Czech e-shop [Alza](www.alza.cz). As the name suggests, [scrapy](https://scrapy.org/) framework was used to implement the crawler.

## Extracted data

Alza is a huge e-shop that deals mostly in electronics and digital media (videogames, ebooks, movies etc.). We are interested in following information about each listed product:

* **Name** - Name under which is product listed
* **Price** - Product price (including VAT)
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

