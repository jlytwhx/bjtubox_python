import re
from utils.dean import Dean
from bs4 import BeautifulSoup

from .models import Course
from person.models import Person

session = Dean().dean_session


def get_course(page):
    url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/remains/'
    params = {
        'page': page,
        'perpage': 500
    }
    soup = BeautifulSoup(session.get(url, params=params).content.decode(), 'html5lib')
    tbody = soup.table.tbody
    for course in tbody.find_all('tr')[1:]:
        td_list = course.find_all('td')
        department = course.span.text.strip()
        base_info = td_list[1].text.replace(department, '').strip().replace('\n', '')
        course_id, name, no = re.findall(r'(.{7}) (.*?) (\d\d)', base_info)[0]
        hour, _, point = td_list[6].text.split()
        hour = 0 if hour == '-' else int(float(hour))
        teacher_name = td_list[8].text.strip()
        time_place_list = td_list[9].text.split('\n')
        for time_place in time_place_list:
            if not time_place:
                continue
            week, weekday, day_no, building, classroom = re.findall(r'第(.*?)周 (.*?) (.*?) (.*?) (.*)', time_place)[0]
            if '点见教务处' in classroom:
                classroom = '-'
            if '-' not in week:
                if ',' in week:
                    result = [str(int(x.replace(' ', ''))) for x in week.split(',')]
                    week = ','.join([str(x) for x in result])

            else:
                result = []
                week_list = week.split(',')
                for week in week_list:
                    start, end = [int(x) for x in week.split('-')]
                    result += [x for x in range(start, end + 1)]
                week = ','.join([str(x) for x in result])
            weekday = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '日': 7}[weekday[-1]]
            day_no = day_no[1]
            print(course_id, name, week, weekday, day_no)
            teacher = Person.objects.filter(group__name='教职工', name=teacher_name.split(',')[0])
            course = Course.objects.create(
                course_id=course_id,
                name=name,
                week=week,
                hour=hour,
                point=point,
                day=weekday,
                day_no=day_no,
                course_no=no,
                teacher=None if not teacher else teacher[0],
                school=department,
                building=building,
                classroom=classroom
            )
            course.save()


def run():
    for i in range(1, 5):
        get_course(i)


if __name__ == '__main__':
    run()
