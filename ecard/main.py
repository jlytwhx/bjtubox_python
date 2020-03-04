import cx_Oracle
import json
import datetime

dsnStr = cx_Oracle.makedsn("", "", "")


def get_ecard_balance(userid):
    db = cx_Oracle.connect(user="", password="", dsn=dsnStr)
    cursor = db.cursor()
    sql = "SELECT ODDFARE FROM CCENSE.BASE_CUSTOMERS where outid = :outid"
    cursor.execute(sql, {'outid': userid})
    result = cursor.fetchall()[0][0]
    db.close()
    result = '%.2f' % float(result)
    return result


def get_ecard_record(userid, num=30):
    db = cx_Oracle.connect(user="", password="", dsn=dsnStr)
    cursor = db.cursor()
    sql = "SELECT * FROM(SELECT CCENSE.BASE_TERM.TERMNAME,CCENSE.REC_MAIN_CONSUME.OPFARE,CCENSE.REC_MAIN_CONSUME.OPDT, " \
          "CCENSE.REC_MAIN_CONSUME.ODDFARE FROM CCENSE.REC_MAIN_CONSUME LEFT JOIN CCENSE.BASE_CUSTOMERS " \
          "ON CCENSE.BASE_CUSTOMERS.CUSTOMERID = CCENSE.REC_MAIN_CONSUME.CUSTOMERID LEFT JOIN CCENSE.BASE_TERM " \
          "ON CCENSE.BASE_TERM.TERMID = CCENSE.REC_MAIN_CONSUME.TERMID " \
          "WHERE CCENSE.BASE_CUSTOMERS.OUTID = :OUTID ORDER BY OPDT DESC) WHERE ROWNUM < {}".format(
        num)
    cursor.execute(sql, {'OUTID': userid})
    records = cursor.fetchall()
    result = []
    for record in records:
        info = {
            'type': 'sub',
            'opfare': '%.2f' % float(record[1]),
            'date': record[2].strftime("%m-%d %H:%M:%S"),
            'description': record[0],
            'oddfare': record[3]
        }
        result.append(info)
    db.close()
    return result


def get_month_consume_data(userid, month, category=None):
    month = f'{month}%'
    db = cx_Oracle.connect(user="", password="", dsn=dsnStr)
    cursor = db.cursor()
    category_sql = ''
    query_dict = {
        'outid': userid,
        'month': month
    }
    if category:
        category_sql = '    and CCENSE.REC_MAIN_CONSUME.DSCRP = :category\n'
        query_dict['category'] = category
    sql = ("SELECT\n"
           "	CCENSE.BASE_TERM.TERMNAME,\n"
           "	CCENSE.V_DEPT_FULL.DPTNAME,\n"
           "	CCENSE.REC_MAIN_CONSUME.DSCRP,\n"
           "	CCENSE.REC_MAIN_CONSUME.OPFARE,\n"
           "	CCENSE.REC_MAIN_CONSUME.OPDT \n"
           "FROM\n"
           "	CCENSE.REC_MAIN_CONSUME\n"
           "	LEFT JOIN CCENSE.BASE_CUSTOMERS ON CCENSE.BASE_CUSTOMERS.CUSTOMERID = CCENSE.REC_MAIN_CONSUME.CUSTOMERID\n"
           "	LEFT JOIN CCENSE.BASE_TERM ON CCENSE.BASE_TERM.TERMID = CCENSE.REC_MAIN_CONSUME.TERMID\n"
           "	LEFT JOIN CCENSE.V_DEPT_FULL ON CCENSE.BASE_TERM.DPTCODE = CCENSE.V_DEPT_FULL.DPTCODE \n"
           "WHERE\n"
           "	CCENSE.BASE_CUSTOMERS.OUTID = :outid \n"
           "	AND TO_CHAR(CCENSE.REC_MAIN_CONSUME.OPDT, 'YYYYMM') LIKE :month\n") + category_sql + "ORDER BY OPDT DESC"
    cursor.execute(sql, query_dict)
    records = cursor.fetchall()
    result = []
    for record in records:
        info = {
            'type': 'sub',
            'term_name': record[0],
            'department_name': record[1],
            'description': record[2],
            'opfare': '%.2f' % (0 - float(record[3])),
            'date': record[4].strftime("%Y-%m-%d %H:%M:%S"),
        }
        result.append(info)
    db.close()
    return result


def get_month_data(userid, month=None, category=None):
    if not month:
        month = datetime.datetime.now().strftime("%Y%m")
    month_consume_data = get_month_consume_data(userid, month, category)
    month_consume_sum = sum([abs(float(x['opfare'])) for x in month_consume_data])
    month_charge_data = []
    month_charge_sum = '未知'
    month_data = sorted([*month_consume_data, *month_charge_data], key=lambda x: x['date'], reverse=True)
    result = {
        'month_data': month_data,
        'month_consume_sum': month_consume_sum,
        'month_charge_sum': month_charge_sum,
        'month': month
    }
    return result


if __name__ == '__main__':
    # print(get_month_data('16211268', '201910'))
    print(dsnStr)
    print(type(str(dsnStr)))