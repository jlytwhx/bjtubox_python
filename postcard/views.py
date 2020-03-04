from user.auth import check
from main import api_response, send_message, error
from .models import PostCard, SendCard
from django.forms.models import model_to_dict
from person.models import Person
from django.views.decorators.csrf import csrf_exempt
from .main import send


@check
def get_card_category_list(request):
    category_list = [model_to_dict(x) for x in PostCard.objects.all()]
    return api_response({'data': category_list})


@csrf_exempt
@check
def send_postcard(request):
    user = request.user
    to_user = request.POST['to_user']
    card_id = request.POST['card_id']
    content = request.POST['content']
    send(user.person, to_user, card_id, content)
    return api_response({'msg': '发送成功！'})


@check
def get_my_card_list(request):
    user = request.user
    result = []
    card_list = SendCard.objects.filter(to_person=user.person, delete=False).order_by('-time')
    for card in card_list:
        result.append({
            'url': card.card.url,
            'id': card.id,
            'content': card.content,
            'from_user': card.from_person.name
        })
    return api_response({'data': result})


@csrf_exempt
@check
def delete_card(request):
    card_id = request.POST['card_id']
    try:
        card = SendCard.objects.get(id=card_id)
    except:
        return error(3302)
    if card.to_person != request.user.person:
        return error(3301)
    card.delete = True
    card.save()
    return api_response({'msg': '删除成功！'})


@csrf_exempt
def admin_send_card(request):
    person = Person.objects.get(id='16211268')
