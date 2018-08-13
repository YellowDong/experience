#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb


class Mysql:
    def __init__(self, host, user, password, db, autocommit=True):
        self.conn = MySQLdb.connect(host=host, user=user, password=password,
                                    db=db)
        self.conn.autocommit(autocommit)

    def close(self):
        self.conn.close()

    def _execte(self, sql):
        cursor = self.conn.cursor()
        

    def _insert(self, keys, cursor, values):
        num = len(keys)*'%s'
        sql = f"INSERT INTO ({keys}) VALUES ({num})"
        cursor.execute(sql, (values))
