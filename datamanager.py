import pymysql

class Mysql():

    def __init__(self):
        super().__init__()
        self.conn = None

    def connect(self, info):
        self.conn = pymysql.connect(host=info["host"], user=info["user"], password=info["password"], db=info["db"], charset=info["charset"])

    def close(self):
        if self.conn:
            self.conn.close()

    def insert(self, query, obj):
        try:
            curs = self.conn.cursor()
            if type(obj) is list:
                print("list")
                curs.executemany(query, obj)
                self.conn.commit()
            elif type(obj) is tuple:
                print("tuple")
                curs.execute(query, obj)
                self.conn.commit()
            else:
                print("obj is not proper type : ", type(obj))
        except Exception as e:
            self.conn.rollback()
            print(e)

    def select(self, query, tp):
        try:
            curs = self.conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(query, tp)
            rows = curs.fetchall()
            return rows
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    info = {'host': '218.38.28.147', 'user': 'root', 'password': 'rnjscjfghrhrorsla!!!', 'db': 'stock2daya', 'charset': 'utf8'}
    my = Mysql()
    try:
        my.connect(info)
        query = "insert into sise(code,date,open,close,high,low,adjust,volume) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        # '251270','20170602',152500,158500,160000,152500,0,10002738
        my.insert(query, ('251270', '20170605', 159000, 161000, 161000, 158000, 0, 577125))

        """rows = my.select("select * from sise where code = %s order by idx desc limit 1 ;", ("251270"))
        if(rows):
                print(rows[0]["idx"])
        else:
            print(0)"""

    except Exception as e:
        print("Mysql Error ", e)
    finally:
        my.close()
