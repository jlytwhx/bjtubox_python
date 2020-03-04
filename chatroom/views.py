from main import api_response
from .main import recent_message, online_list, increase_life
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from user.auth import check


@csrf_exempt
@check
def get_recent_message(request):
    room_id = request.POST['room_id']
    last_timestamp = request.POST['last_timestamp'] or 0
    increase_life(room_id, request.user)
    return api_response({
        'recent_messages': recent_message(room_id, last_timestamp),
        'online_list': online_list(room_id),
    })
