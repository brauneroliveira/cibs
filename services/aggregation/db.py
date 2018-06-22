import psycopg2

class db():

    @staticmethod
    def query(sql):
        dbname='cibs'
        user='postgres'
        host='localhost'
        password='4774811'
        connection = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def execute(sql):
        dbname='cibs'
        user='postgres'
        host='localhost'
        password='4774811'
        connection = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return None