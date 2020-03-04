import os, django, datetime
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bjtubox.settings")
django.setup()

from postcard.main import send
from person.models import Person
from main import send_message

if __name__ == '__main__':
    now = datetime.datetime.now().strftime("%m%d")
    sender = Person.objects.get(id='16211268')
    person_list = Person.objects.filter(id_card__regex="^.{10}%s.{4}$" % now, group_id__gte=1)
    for person in person_list:
        content = "{name}你好！今天是你的生日！魔盒君祝你生日快乐，许下的愿望都会实现哦！".format(name=person.name)
        to_user = person.id
        send(sender, to_user, "5", content)
        time.sleep(1)
    send_message('16211268', '今天的生日祝福都已经发送完毕了！')
