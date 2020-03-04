from main import send_message
from .models import SendCard


def send(person, to_user, card_id, content):
    send = SendCard.objects.create(from_person=person, to_person_id=to_user, content=content, card_id=card_id)
    send.save()
    tips = '某人给你发来了一张贺卡！快打开交大魔盒小程序中查看吧！'
    send_message(to_user, tips)
    return True
