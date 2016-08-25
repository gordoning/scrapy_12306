import pymysql.cursors

if __name__ == "__main__":
    print "init ok"
    conn = pymysql.connect(host='localhost', port=3306, user='linguoyang', password='816557', db='12306',
                                    charset='utf8')
        # print "connect no"

    print "connect ok"
    cursor = conn.cursor()
    # data = self.cursor.fetchall()
    # cursor.execute('use agency_sellticket')
    cursor.execute('select * from agency_sellticket')
    print cursor.fetchone()
    cursor.close()
    conn.close()

    print "connect OK"
    # insert_sql = "insert 'agency_sellticket' (agency_name,province,city,county,agency_adress,start_time_am,stop_time_am,start_time_pm,stop_time_pm) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
