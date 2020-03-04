import re
from main import api_response
from .models import Person
from user.auth import check


@check
def search(request):
    person_list = []
    string = request.GET['string']
    if re.search(r'^\d{5,11}$', string):
        person_list = Person.objects.filter(id__istartswith=string).order_by('-id')[:5]
    elif re.search(r'^[\u4e00-\u9fa5]+$', string):
        person_list = Person.objects.filter(name__contains=string).order_by('-id')[:5]
    result = []
    for person in person_list:
        result.append({'name': '{}'.format(person.name), 'userid': person.id})
    return api_response({'result': result})
