# coding=utf8
import pandas as pd
import pymysql
import sqlalchemy

from collections import namedtuple


class ConnectMysql(object):

    def __init__(self, MysqlName, host='localhost', port=3306, user='web', passwd='Imweb', charset='UTF8',
                 db='com_stable'):

        SQLConnector = namedtuple(MysqlName, ['host', 'port', 'user', 'passwd', 'charset', 'db'])
        self.para = SQLConnector(host, port, user, passwd, charset, db)

    def SelfConnect(self):
        conn = pymysql.connect(host=self.para.host, port=self.para.port, user=self.para.user, passwd=self.para.passwd,
                               charset=self.para.charset, db=self.para.db)
        return conn

    def SelfEngine(self):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(self.para.user, self.para.passwd, self.para.host,
                                                               self.para.port, self.para.db,
                                                               self.para.charset))  # 用sqlalchemy创建引擎
        return engine

    def sql2data(self, sql):
        # type: (str) -> dataframe
        conn = self.SelfConnect()
        df = pd.read_sql(sql, conn)
        conn.close()
        return df

    def DetectConnectStatus(self, returnresult=True, printout=False):

        try:
            result = self.Excutesql()
            status = 'Good connection!'
            if printout:
                print(status)
        except pymysql.OperationalError as e:
            result = str(e)
            status = 'Bad connection!'
            if printout:
                print(e)
        finally:
            if returnresult:
                return result
            else:
                return status

    def DF2mysql(self, df, tablename, engine='SelfEngine', if_exists='replace', index=False):
        if isinstance(engine, str) and engine == 'SelfEngine':
            df.to_sql(tablename, con=self.SelfEngine(), if_exists=if_exists, index=index)
        else:
            df.to_sql(tablename, con=engine, if_exists=if_exists, index=index)

    def Excutesql(self, sql='SHOW DATABASES'):
        conn = self.SelfConnect()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def SHOWDATABASES(self):
        return self.Excutesql(sql='SHOW DATABASES')

    def SHOWTABLES(self):
        return self.Excutesql(sql='SHOW TABLES')


if __name__ == '__main__':
    pass
