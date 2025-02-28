# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class CavaItem(scrapy.Item):
    # Student fields
    student_id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field()
    ethnicity = scrapy.Field()
    race = scrapy.Field()
    grade = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    school = scrapy.Field()
    primary_teacher = scrapy.Field()
    primary_disability = scrapy.Field()
    secondary_disability = scrapy.Field()
    notes = scrapy.Field()
    
    # ISA fields
    iep_due_date = scrapy.Field()
    student_name = scrapy.Field()

