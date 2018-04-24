#!/usr/bin/env python3
#!-*- encoding:utf-8 -*-
import unittest
from main.tool import Tool

class ToolTest(unittest.TestCase):
    def setUp(self):
        self.tool = Tool()

    def test_mysqldump(self):
        self.tool.dump(backdir="/home/perterually/Downloads/sync/replace",tablename='t_fund_netvalue_increment',dbname='fund')
        
    def test_query(self):
        self.tool.query(tablename='tablelist',dbname='sync',columns='table_name, db_name',where='period="日"')


if __name__ == '__main__':
    unittest.main()