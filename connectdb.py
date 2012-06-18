import MySQLdb


class ConnectDB():

    def connect(self, sql, type=0):
        db = MySQLdb.connect("localhost","root","elleke","socialexpress" )
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        if type:
            db.commit()
            
        db.close()
        return data
