# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class TutorialPipeline(object):
    def __init__(self):
        self.con = sqlite3.connect('matches.db')
        self.cur = self.con.cursor()
        self.table()

    def table(self):
        self.cur.execute("""DROP TABLE IF EXISTS matches_tb""")
        self.cur.execute("""create table matches_tb(
                            league text,
                            result_1 text,
                            result_2 text,
                            stade text,
                            state text,
                            channel text,
                            time text,
                            team_1 text,
                            team_2 text

                            )""")

    def process_item(self, item, spider):
        self.store(item)
        return item

    def store(self, item):
        self.cur.execute("""insert into matches_tb values (?,?,?,?,?,?,?,?,?)""", (
            item['league'][0],
            item['rslt'][0],
            item['rslt'][1],
            item['std'],
            item['state'],
            item['channel'],
            item['tme'],
            item['team_1'][0],
            item['team_2'][0]

        ))
        self.con.commit()
