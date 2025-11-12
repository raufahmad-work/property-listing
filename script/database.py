from peewee import SqliteDatabase, Model, CharField, DateTimeField, Check
from datetime import datetime
from .constants import SOURCE_CHOICES, BOROUGH_CHOICES

db = SqliteDatabase("listings.db")

class SentListing(Model):
    url = CharField(primary_key=True)
    source = CharField(constraints=[Check(f"source IN {SOURCE_CHOICES}")])
    borough = CharField(constraints=[Check(f"borough IN {BOROUGH_CHOICES}")])
    date_sent = DateTimeField(default=datetime.now)

    class Meta:
        database = db

db.connect()
db.create_tables([SentListing])
