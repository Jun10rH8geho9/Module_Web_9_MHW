# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
from itemadapter import ItemAdapter

# Пайплайн для обробки та зберігання даних про цитати та авторів
class QuotesScraperPipeline:
    authors = []
    quotes = []
    
    # Обробляємо елементи, отримані від краулера
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        author_info = {}
        quote_info = {}

        # Розділяємо інформацію про авторів та цитати
        for key, value in item.items():
            if key != 'fullname' and key != 'quote':
                author_info[key] = value
                quote_info[key] = value

         # Якщо присутня інформація про автора, додати її до списку авторів
        if 'fullname' in adapter:
            author_info['author'] = adapter['fullname']
            self.authors.append(author_info.copy())  # Копіюємо словник для запобігання посиланням

        # Якщо присутня інформація про цитату, додати її до списку цитат
        if 'quote' in adapter:
            quote_info['quote'] = adapter['quote']
            self.quotes.append(quote_info.copy())  # Копіюємо словник для запобігання посиланням

        return item
    
    # Павук закінчує свою роботу
    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
            json.dump(self.quotes, quotes_file, ensure_ascii=False, indent=2, sort_keys=True)
            
        with open('authors.json', 'w', encoding='utf-8') as authors_file:
            json.dump(self.authors, authors_file, ensure_ascii=False, indent=2, sort_keys=True)