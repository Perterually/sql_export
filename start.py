#!/usr/bin/env python3
#!-*- encoding:utf-8 -*-
from main.tool import Tool
def main():
    tool = Tool()
    db_table = tool.query(tablename='tablelist',dbname='sync',columns='table_name, db_name',where='period="日"')
    for i in db_table:
        tool.dump(table_name=i['table_name'],db_name=i['db_name'])
if __name__ == '__main__':
    main()