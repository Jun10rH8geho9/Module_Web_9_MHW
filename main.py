from scrapy.crawler import CrawlerProcess
from quotes_scraper.quotes_scraper.spiders.quotes_spider import QuotesSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()