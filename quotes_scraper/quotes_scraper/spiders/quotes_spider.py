import scrapy
from scrapy.exceptions import CloseSpider
from quotes_scraper.quotes_scraper.items import QuoteItem, AuthorItem
from quotes_scraper.quotes_scraper.pipelines import QuotesScraperPipeline

# Павук для отримання цитат з веб-сайту quotes.toscrape.com
class QuotesSpider(scrapy.Spider):
    name = "get_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {QuotesScraperPipeline: 300}}

    # Обробляємо відповідь сервера та отримує цитати
    def parse(self, response):
        try:
            # Пошук цитат та необхідних даних
            for collection in response.xpath("//div[@class='quote']"):
                quote = collection.xpath(".//span[@class='text']/text()").get().strip()
                author = collection.xpath(".//span/small[@class='author']/text()").get().strip()
                tags = collection.xpath(".//div[@class='tags']/a/text()").extract()
                yield QuoteItem(quote=quote, author=author, tags=tags)

                # Перехід на сторінку автора, якщо вона є
                author_url = collection.xpath(".//span/a/@href").get()
                if author_url:
                    yield response.follow(url=response.urljoin(author_url), callback=self.parse_author)

            # Перехід на сторінку автора, якщо вона є
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield response.follow(url=response.urljoin(next_link))
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            raise CloseSpider("Error occurred while parsing")
        
    # Обробка відповіді сервера та отримання інформацію про автора
    def parse_author(self, response):
        try:
            content = response.xpath("//div[@class='author-details']")
            fullname = content.xpath(".//h3[@class='author-title']/text()").get().strip()
            born_date = content.xpath(".//p/span[@class='author-born-date']/text()").get().strip()
            born_location = content.xpath(".//p/span[@class='author-born-location']/text()").get().strip()
            description = content.xpath(".//div[@class='author-description']/text()").get().strip()
            yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        except Exception as e:
            self.logger.error(f"Error occurred while parsing author details: {e}")