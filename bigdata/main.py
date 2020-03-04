import cx_Oracle
import pymysql
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
dsnStr = cx_Oracle.makedsn("", "1521", "ORCL")

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='',
    db='',
    charset='utf8mb4'
)
cursor = conn.cursor()
cursor.execute('select * from device')
device_data = {data[0]: data[2] for data in cursor.fetchall()}
cursor.execute('select * from department')
department_data = {data[0]: data[1] for data in cursor.fetchall()}
conn.close()


class PersonData:
    def __init__(self, student_id):
        self.student_id = student_id
        self.customer_id = ''
        self.data = []
        self.department_data = []
        self.lost_card_data: list[dict['card_id':str, 'timestamp':int]] = []
        self.part_dict = {}
        self.part_num_dict = {}
        self.eat_data = {}
        self.sum_cost = 0
        self.first_ill_date = 0

    def get_customer_id(self):
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            db='',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        sql = 'select customer_id from customer_id where out_id="{}"'.format(self.student_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            self.customer_id = result[0][0]
        conn.close()

    def load_data(self):
        db = cx_Oracle.connect(user="", password="", dsn=dsnStr)
        oracle_cursor = db.cursor()
        self.get_customer_id()
        sql = "select CARDNO,OPDT,SUMFARE,OPFARE,DSCRP,OPCOUNT,TERMID from CCENSE.REC_MAIN_CONSUME where CUSTOMERID=:custom_id"
        oracle_cursor.execute(sql, {'custom_id': self.customer_id})
        self.data = sorted(oracle_cursor.fetchall(), key=lambda x: x[1].timestamp())
        db.close()

    def get_lost_card_data(self):
        card_id = 0
        for data in self.data:
            if card_id != int(data[0]):
                self.lost_card_data.append({'card_id': int(data[0]), 'lost_timestamp': int(data[1].timestamp())})
                card_id = int(data[0])

    def get_most_like_department(self):
        department_count_dict = {}
        for data in self.data:
            department_id = department_data[device_data[data[6]]]
            if department_id not in department_count_dict:
                department_count_dict[department_id] = {'count': 1, 'sum': float(data[3]), 'type': data[4]}
            else:
                department_count_dict[department_id]['count'] += 1
                department_count_dict[department_id]['sum'] += float(data[3])
        for key, value in department_count_dict.items():
            self.department_data.append((key, value['count'], value['sum'], value['type']))
        self.department_data.sort(key=lambda x: x[1])

    def get_part_of_consume(self):
        part_dict = {'商场购物': 0, '一卡通购电': 0, '医疗支出': 0, '购热水支出': 0, '淋浴支出': 0, '上机支出': 0, '餐费支出': 0}
        part_num_dict = {'商场购物': 0, '一卡通购电': 0, '医疗支出': 0, '购热水支出': 0, '淋浴支出': 0, '上机支出': 0, '餐费支出': 0}
        for data in self.data:
            self.sum_cost += float(data[3])
            if data[4] not in part_dict:
                part_dict[data[4]] = float(data[3])
                part_num_dict[data[4]] = 1
            else:
                part_dict[data[4]] += float(data[3])
                part_num_dict[data[4]] += 1
        self.part_dict = part_dict
        self.part_num_dict = part_num_dict


    def get_eat_data(self):
        eat_data = {
            'breakfast': {'count': 0, 'sum': 0.0},
            'lunch': {'count': 0, 'sum': 0.0},
            'dinner': {'count': 0, 'sum': 0.0},
        }
        for data in self.data:
            if data[4] == '餐费支出':
                hour = data[1].hour
                if 5 < hour < 9:
                    eat_data['breakfast']['count'] += 1
                    eat_data['breakfast']['sum'] += float(data[3])
                if 10 < hour < 14:
                    eat_data['lunch']['count'] += 1
                    eat_data['lunch']['sum'] += float(data[3])
                if 16 < hour < 20:
                    eat_data['dinner']['count'] += 1
                    eat_data['dinner']['sum'] += float(data[3])
        self.eat_data = eat_data

    def get_first_ill(self):
        for data in self.data:
            if data[4] == '医疗支出':
                self.first_ill_date = data[1].strftime("%Y-%m-%d %H:%M:%S")

    def special_day(self):
        day_dict = {}
        for data in self.data:
            day = data[1].strftime("%Y-%m-%d")
            department_id = department_data[device_data[data[6]]]
            if day not in day_dict:
                day_dict[day] = {'sum': float(data[3]), 'department_dict': {department_id: 1}}
            else:
                day_dict[day]['sum'] += float(data[3])
                if department_id in day_dict[day]['department_dict']:
                    day_dict[day]['department_dict'][department_id] += 1
                else:
                    day_dict[day]['department_dict'][department_id] = 1
        day_data = [(key, value['sum'], value['department_dict']) for key, value in day_dict.items()]
        day_data.sort(key=lambda x: x[1], reverse=True)

    def run(self):
        self.load_data()
        self.get_lost_card_data()
        self.get_most_like_department()
        self.get_part_of_consume()
        self.get_eat_data()
        self.get_first_ill()
        self.special_day()

    def calculate(self):
        data = dict()
        data['person_id'] = self.student_id
        if self.first_ill_date:
            data['first_ill_time'] = self.first_ill_date
        if sum(self.part_dict.values()):
            data['engel_num'] = self.part_dict['餐费支出'] / (sum(self.part_dict.values()))
        else:
            data['engel_num'] = -1
        data['shower_cost'] = self.part_dict['淋浴支出']
        data['hospital_cost'] = self.part_dict['医疗支出']
        data['computer_cost'] = self.part_dict['上机支出']
        data['eat_cost'] = self.part_dict['餐费支出']
        data['electric_cost'] = self.part_dict['一卡通购电']
        data['shop_cost'] = self.part_dict['商场购物']
        data['water_cost'] = self.part_dict['购热水支出']

        data['shower_num'] = self.part_num_dict['淋浴支出']
        data['hospital_num'] = self.part_num_dict['医疗支出']
        data['computer_num'] = self.part_num_dict['上机支出']
        data['eat_num'] = self.part_num_dict['餐费支出']
        data['electric_num'] = self.part_num_dict['一卡通购电']
        data['shop_num'] = self.part_num_dict['商场购物']
        data['water_num'] = self.part_num_dict['购热水支出']

        data['sum_cost'] = self.sum_cost
        data['lost_card_num'] = len(self.lost_card_data)

        lost_data = [k['lost_timestamp'] for k in self.lost_card_data]
        lost_min = 999999999999999999
        for i in range(len(self.lost_card_data) - 1):
            sub_day = lost_data[i + 1] - lost_data[i]
            lost_min = min(sub_day, lost_min)
        data['lost_card_min'] = lost_min if lost_min < 2 ** 64 else -1
        data['breakfast_num'] = self.eat_data['breakfast']['count']
        data['lunch_num'] = self.eat_data['lunch']['count']
        data['dinner_num'] = self.eat_data['dinner']['count']
        data['breakfast_cost'] = self.eat_data['breakfast']['sum']
        data['lunch_cost'] = self.eat_data['lunch']['sum']
        data['dinner_cost'] = self.eat_data['dinner']['sum']
