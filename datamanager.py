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

    def insert(self, query, tp):
        try:
            curs = self.conn.cursor()
            curs.execute(query, tp)
            self.conn.commit()
            print("sucess")
        except Exception as e:
            self.conn.rollback()
            print(e)


if __name__ == "__main__":
    info = {'host': '218.38.28.147', 'user': 'root', 'password': 'rnjscjfghrhrorsla!!!', 'db': 'stock2daya', 'charset': 'utf8'}
    my = Mysql()
    try:
        my.connect(info)
        # query = "insert into sise(code,date,open,close,high,low,adjust,volume) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        # '251270','20170602',152500,158500,160000,152500,0,10002738
        # my.insert(query, ('251270', '20170602', 152500, 158500, 160000, 152500, 0, 10002738))
    except Exception as e:
        print("Mysql Error ", e)
    finally:
        my.close()
