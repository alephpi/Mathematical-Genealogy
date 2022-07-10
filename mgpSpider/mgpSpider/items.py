# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MgpspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    mathscinet_id = Field()
    degree_time = Field()
    school_name = Field()
    school_country = Field()
    advisor = Field()
    students = Field()
    descendants = Field()
    mathematics_subject_classification = Field()

