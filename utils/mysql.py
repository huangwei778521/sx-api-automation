import pymysql
from dbutils.pooled_db import PooledDB
from config.server_info import server_info


class Mysql:
    _pool = None
    sxp_business_config = server_info.get('sql_info')

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__get_conn()
        self.cursor = self.conn.cursor()
        return self

    # 创建数据库连接池
    def __get_conn(self):
        if self._pool is None:
            self._pool = PooledDB(
                creator=pymysql,
                mincached=10,
                maxcached=10,
                maxshared=20,
                maxconnections=100,
                blocking=True,
                maxusage=0,
                setsession=None,
                host=self.sxp_business_config["host"],
                port=self.sxp_business_config["port"],
                user=self.sxp_business_config["user"],
                passwd=self.sxp_business_config["password"],
                db=self.sxp_business_config["database"],
                use_unicode=False,
                charset="utf8"
            )
        return self._pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql):
        """
        :param sql: 字符串类型，sql语句
        """
        try:
            count = self.cursor.execute(sql)
        except Exception as e:
            raise e
        return count

    def select_all(self, sql):
        try:
            self.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            raise e

    def select_one(self, sql):
        try:
            self.execute(sql)
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            raise e

    def insert_one(self, sql):
        try:
            self.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def delete(self, sql):
        try:
            self.execute(sql)
        except Exception as e:
            self.conn.rollback()
            raise e

    def update(self, sql):
        try:
            self.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e



