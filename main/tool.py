#! -*- encoding:utf-8 -*-
import pymysql
import logging
import time
import datetime
from configparser import ConfigParser
import os
import re
FORMAT = '%(asctime)s  %(module)s: %(message)s  '
logging.basicConfig(format=FORMAT, level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')

PATH = os.getcwd() + '/main/db.config'


class Tool:
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(PATH)
        self.conn = pymysql.Connect(host=self.cfg.get('db', 'db_host'), port=self.cfg.getint('db', 'db_port'),
                                    user=self.cfg.get('db', 'db_user'), password=self.cfg.get('db', 'db_pass'),
                                    charset=self.cfg.get('db', 'db_charset'))
        self.cur = self.conn.cursor()

    def query(self,tablename,dbname,columns,where):
        """读取数据库数据
        """
        sql = "SELECT %s FROM %s.%s where %s ;"%(columns,dbname,tablename,where)
        param = re.compile('\w+')
        colum_li = param.findall(columns)
        try:
            li = []
            self.cur.execute(sql)
            data = self.cur.fetchall()
            for i in data:
                item = {}
                for colum_index in range(len(colum_li)):
                    item[colum_li[colum_index]] = i[colum_index]
                    item[colum_li[colum_index]] = i[colum_index]
                li.append(item)
            return li

        except Exception as error:
            logging.info(error)

    
    def dump(self,table_name,db_name):
        """用mysqldump导出数据格式为一行一行
        """
        mysqldump = "mysqldump -h %s -u %s -P %s --password=%s --skip-extended-insert --skip-comments --no-create-info --skip-add-locks --skip-disable-keys --skip-comments --compact --databases %s --tables %s"%(
            self.cfg.get('db', 'db_host'),self.cfg.get('db', 'db_user'),self.cfg.getint('db', 'db_port'),self.cfg.get('db', 'db_pass'),db_name,table_name
        )
        path = self.cfg.get('mysqldump','path')
        path = path + '/' + db_name + '.' + table_name + '.sql'
        try:
            op = os.popen(mysqldump)
            data = op.read()
            data = re.sub("INSERT INTO ","INSERT INTO %s."%db_name,data)
            data = data.encode('utf-8')
            with open(path,'wb') as f:
                f.write(data)
            f.close()
            logging.info("保存成功")
        except Exception as error:
            logging.info(error)