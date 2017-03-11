from scrapy.spiders import SitemapSpider
import re


class AlzaSpider(SitemapSpider):
    name = 'alza'

    sitemap_urls = ['https://www.alza.cz/_sitemap-products-1.xml']

    def parse(self, response):
        desc = response.css('div#popis')

        try:
            name = desc.css('h2::text').extract_first()
            name = name.strip()
        except AttributeError:
            name = response.css('div#h1cdetail h1::text').extract_first()
            name = name.strip()


        try:
            text_desc = response.css('div#detailText div.nameextc span::text')
            text_desc = text_desc.extract_first().strip()
        except AttributeError:
            text_desc = 'none'

        rev_sum = response.css('div.blockReviewSummary')

        try:
            rating = rev_sum.css('div.c12::text').extract_first()
            rating = rating.strip()
        except AttributeError:
            rating = 'none'

        if rating != 'none':
            users_rated = rev_sum.css('div.c14::text').extract_first()
            users_rated = users_rated.strip().split()[1]
        else:
            users_rated = 'none'

        try:
            price = response.css('tr.pricenormal td.c2 span::text').extract()[-1]
        except IndexError:
            price = response.css('div#pricec div.colValue span::text').extract_first()

        if price is not None:
            price = re.sub(r'[\s+,-]', '', price)
        else:
            price = 'none'

        try:
            warranty = response.css('span#rowWarranty a::text').extract_first().split()[1]
        except AttributeError:
            warranty = 'none'

        yield {
            'name' : name,
            'text_desc' : text_desc,
            'rating' : rating,
            'users_rated' : users_rated,
            'price' : price,
            'warranty' : warranty 
        }