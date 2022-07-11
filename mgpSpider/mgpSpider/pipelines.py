# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pickle import NONE
import traceback
#from mgpSpider.mgpSpider import 
from mgpSpider.items import MgpspiderItem
import sqlite3
import re
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

class MgpspiderPipeline(object):
    def __init__(self):
        self.path = './mgp.db'
    def open_spider(self, spider):
        logging.info("Initializing database...")
        try:
            if os.path.isfile(self.path):
                raise ValueError('Database file %s already exists. Remove it first.\n' % self.path) 
            #if db not exists, sqlite3.connect will automatically create one
            self.conn = sqlite3.connect(self.path)
            self.cursor= self.conn.cursor()

            #create table
            self.cursor.execute('''
                    CREATE TABLE person (
                    id INTEGER PRIMARY KEY NOT NULL,  -- MGP ID
                    name TEXT NOT NULL,
                    mathscinet_id INTEGER,
                    degree_year INTEGER,
                    advisor1_id INTEGER,
                    advisor2_id INTEGER,
                    school1_id INTEGER,
                    school2_id INTEGER,
                    num_students INTEGER,
                    num_descendants INTEGER
                    );
                ''')

            self.cursor.execute('''
                    CREATE TABLE school(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    country TEXT,
                    UNIQUE(name)
                    );
                ''')
            
            #Don't forget to commit!
            self.conn.commit()
            print("Database initialized!")
        except:
            print(traceback.format_exc())
    
    def close_spider(self, spider):
        self.conn.close()
        logging.info("database connection closed")
    def process_item(self, item, spider):

        if item:
            pass
        else:
            return None
        # a glance of the item (raw data)
        #  {
        # 'advisors': ['id.php?id=191279', 'id.php?id=125846'],
        # 'degree_years': '1721',
        # 'id': '125886',
        # 'mathscinet_id': [],
        # 'name': 'Georg Erhard Hamberger',
        # 'school_countries': ['Germany', 'Germany', 'Germany'],
        # 'school_names': ['Friedrich-Schiller-Universität Jena',
        #                 'Friedrich-Schiller-Universität Jena',
        #                 'Friedrich-Schiller-Universität Jena'],
        # 'students_and_descendants': ['According to our current on-line database, '
        #                             'Georg Hamberger has 6 ',
        #                             ' and 119330 ',
        #                             '.\n',
        #                             '\nWe welcome any additional information.']
        # }
    # clean the attribute 
        # id and name is always not empty
        id = int(item['id'])
        name = item['name']

        if item['mathscinet_id'] == []:
            mathscinet_id = None
        else:
            mathscinet_id = int(item['mathscinet_id'][0].split('/')[-1])
        
        if item['degree_years'] == '':
            degree_year = None
        else:
            degree_year = int(re.match(r'\d+', item['degree_years']).group(0))

        if item['students_and_descendants'] == []:
            students = 0
            descendants = 0
        else:
            students = item['students_and_descendants'][0].split()[-1]
            descendants = item['students_and_descendants'][1].split()[-1]
        
        advisors = set(map(lambda x: x.split('=')[-1],item['advisors']))
        if len(advisors) == 0:
            advisor1 = None
            advisor2 = None
        elif len(advisors) == 1:
            advisor1 = int(advisors.pop())
            advisor2 = None
        else:
            advisor1 = int(advisors.pop())
            advisor2 = int(advisors.pop())
            if advisors != set():
                logging.info("id %s has more than 2 different advisors" % item['id'])
        
        if item['school_names'] == []:
            school_names = None 
            school_countries = None
            school_name_country_pairs = None
        else:
            school_name_country_pairs = set(zip(item['school_names'],item['school_countries']))
            if len(school_name_country_pairs) > 2:
                logging.info("id %s has more than 2 different home schools" % item['id'])
        
        # we store at most 2 school_ids
        school_ids = [None, None]

        
        # insert school into db
        if school_name_country_pairs:
            for i, (school_name, school_country) in enumerate(school_name_country_pairs):
                # check if it already exists
                self.cursor.execute('''SELECT id FROM school WHERE name=? AND country=?''',
                                    (school_name, school_country))
                row = self.cursor.fetchone()
                # if so, set id equals to the existed one
                school_ids[i] = row[0] if row else None
                # otherwise insert new school, id equals to the new one
                if not school_ids[i]:
                    self.cursor.execute('''INSERT INTO school 
                                        (name, country)
                                        VALUES (?, ?)''',
                                        (school_name, school_country))
                    self.conn.commit()
                    school_ids[i] = self.cursor.lastrowid

        # insert person into db
        self.cursor.execute('''INSERT OR REPLACE INTO person 
                            (id, name, mathscinet_id, 
                            degree_year, num_students, num_descendants, 
                            advisor1_id, advisor2_id,
                            school1_id, school2_id)
		                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (id, name, mathscinet_id, 
                            degree_year, students, descendants, 
                            advisor1, advisor2,
                            school_ids[0],school_ids[1]))
        # self.cursor.execute('''INSERT OR REPLACE INTO person
        #                     (school1_id, school2_id)
        #                     VALUES (?, ?)''',
        #                     (school_ids[0],school_ids[1]))
        
        self.conn.commit()

    #no need to keep item, so do not yield 

        
