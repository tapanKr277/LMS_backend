import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  
django.setup()

from app.models import Book 


with open('dummyData.json', 'r'  ,encoding='utf-8') as json_file:
    data = json.load(json_file)


for entry in data:
    book = Book(**entry)
    book.save()

print("Data population completed.")
