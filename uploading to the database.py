import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://web_9MHW:AfmVJWySoGxOfWLS@hedgehog.rsn29se.mongodb.net/My_homework_DB_2?retryWrites=true&w=majority&appName=hedgehog")

date_base = client.My_homework_DB_2

# Cтворення колекції авторів у базі даних MongoDB
collection_authors = date_base.scrapy_authors
collection_quotes = date_base.quotes

# Завантаження авторів у базу даних з файлу JSON
with open("authors.json", encoding='utf-8') as f:
    data_authors = json.load(f)
    collection_authors.insert_many(data_authors)

# Завантаження цитат у базу даних з файлу JSON
with open("quotes.json", encoding='utf-8') as f:
    data_quotes = json.load(f)
    collection_quotes.insert_many(data_quotes)