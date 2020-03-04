from .models import Classroom


def get_free_classroom_by_building_and_no(building, no):
    building_dict = {
        '学活': '学生活动服务中心',
        '八教': '第八教学楼',
        '东一': '东区一教',
        '东二': '东区二教',
        '思东': '思源东楼',
        '思西': '思源西楼',
        '思源': '思源楼',
        '逸夫': '逸夫教学楼',
        '机械': '机械楼',
        '九教': '第九教学楼',
        '五教': '第五教学楼',
        '建艺': '第十七号教学楼'
    }
    search_dict = {
        'building': building,
    }
    classroom_list = Classroom.objects.filter(**search_dict)
    result = []
    for classroom in classroom_list:
        result.append({'name': classroom.name, 'status': eval("classroom.class{}".format(no))})
    result = sorted(result, key=lambda x: x['name'])
    return result
