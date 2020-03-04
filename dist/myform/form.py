from .field import Field
import json
from urllib.parse import parse_qs
from django.db.models import Model


class MyFormMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'MyForm':
            return type.__new__(mcs, name, bases, attrs)
        attrs['__fields__'] = {}
        if 'model' not in attrs:
            raise ValueError("未绑定到model")
        if 'primary_key' not in attrs:
            raise ValueError("缺少primary_key属性")
        for key, attr in attrs.items():
            if isinstance(attr, Field):
                attrs['__fields__'][key] = attr
        return type.__new__(mcs, name, bases, attrs)


class MyForm(metaclass=MyFormMetaClass):
    model = Model

    def __init__(self, primary_value, **kwargs):
        super(MyForm, self).__init__(**kwargs)
        self.primary_value = primary_value

    @property
    def json(self):
        result = []
        for name, field in self.__fields__.items():
            field = field.to_dict()
            field['name'] = name
            result.append(field)
        return json.dumps(result, ensure_ascii=False)

    def load_from_request(self, request):
        params = {k: v[0] for k, v in parse_qs(request.body.decode()).items() if k in self.__fields__}
        model = self.model.objects.get_or_create(**{self.primary_key: self.primary_value})[0]
        for k, v in params.items():
            eval('model.{}={}'.format(k, v))
        model.save()
