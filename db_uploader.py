import os, django, csv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clnass505.settings")
django.setup()

from lectures.models import *
from users.models    import *

CSV_PATH_CATEGORIES    = './csv/categories.csv'
CSV_PATH_DIFFICULTS    = './csv/difficulties.csv'
CSV_PATH_SUBCATEGORIES = './csv/subcategories.csv'
CSV_PATH_LECTURES      = './csv/lectures.csv'

with open(CSV_PATH_CATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            name = row[0]
            

with open(CSV_PATH_DIFFICULTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row [0]:
            name = row[0]
          

with open(CSV_PATH_SUBCATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row [0]:
            name = row[0]
            category_id = row[1]
            
with open(CSV_PATH_LECTURES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Lecture.objects.create(
            name           = row[0],
            price          = row[1],
            discount_rate  = row[2],
            user_id        = row[5],
            difficulty_id  = row[6],
            subcategory_id = row[7]
        )

