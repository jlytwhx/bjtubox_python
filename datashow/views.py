from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def get_pv(request):
    data = {
        "value": 3574,
        "unit": ""
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False))
