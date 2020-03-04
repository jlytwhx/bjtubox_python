from main import api_response
from .models import Exam
from user.auth import check


# Create your views here.
@check
def get_exam_info(request):
    user = request.user
    exam_list = Exam.objects.filter(user=user.person)
    result = []
    for exam in exam_list:
        exam_info = {
            'school': exam.school,
            'teacher': exam.teacher,
            'name': exam.name,
            'method': exam.type,
            'time': exam.time,
            'place': exam.place,
            'comment': exam.comment
        }
        result.append(exam_info)
    return api_response({'data': result})
