import cx_Oracle
import xlwt
import csv

dsnStr = cx_Oracle.makedsn("", "1521", "ORCL")


def get_month_consume_data(month):
    month = f'{month}%'
    db = cx_Oracle.connect(user="", password="", dsn=dsnStr, encoding="UTF-8", nencoding="UTF-8")
    cursor = db.cursor()
    query_dict = {
        'month': month
    }
    sql = ("SELECT\n"
           "	CCENSE.BASE_TERM.TERMNAME,\n"
           "	CCENSE.V_DEPT_FULL.DPTNAME,\n"
           "	CCENSE.REC_MAIN_CONSUME.DSCRP,\n"
           "	CCENSE.REC_MAIN_CONSUME.OPFARE,\n"
           "	CCENSE.REC_MAIN_CONSUME.OPDT, \n"
           "    CCENSE.BASE_CUSTOMERS.OUTID  \n"
           "FROM\n"
           "	CCENSE.REC_MAIN_CONSUME\n"
           "	LEFT JOIN CCENSE.BASE_CUSTOMERS ON CCENSE.BASE_CUSTOMERS.CUSTOMERID = CCENSE.REC_MAIN_CONSUME.CUSTOMERID\n"
           "	LEFT JOIN CCENSE.BASE_TERM ON CCENSE.BASE_TERM.TERMID = CCENSE.REC_MAIN_CONSUME.TERMID\n"
           "	LEFT JOIN CCENSE.V_DEPT_FULL ON CCENSE.BASE_TERM.DPTCODE = CCENSE.V_DEPT_FULL.DPTCODE \n"
           "WHERE\n"
           "	TO_CHAR(CCENSE.REC_MAIN_CONSUME.OPDT, 'YYYYMM') LIKE :month ORDER BY OPDT DESC")
    cursor.execute(sql, query_dict)
    records = cursor.fetchall()
    result = []
    for record in records:
        info = {
            'term_name': record[0],
            'department_name': record[1],
            'description': record[2],
            'opfare': '%.2f' % (0 - float(record[3])),
            'date': record[4].strftime("%Y-%m-%d %H:%M:%S"),
            'outid': record[5]
        }
        result.append(info)
    db.close()
    return result


def save_csv(result):
    header = result[0].keys()
    rows = [[str(record[key]) for key in header] for record in result]
    rows.insert(0, header)
    with open('result.txt', 'w', encoding='utf-8-sig') as f:
        for line in rows:
            f.write(','.join(line) + '\n')


if __name__ == '__main__':
    save_csv(get_month_consume_data("201909"))
