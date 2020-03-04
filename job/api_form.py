from dist import myform
from django.db import models


class Patient(myform.MyForm):
    model: models.Model
    primary_key: str
    name = myform.InputField('姓名')
    age = myform.InputField('年龄')

    def __init__(self, primary_value):
        super().__init__(primary_value)


if __name__ == '__main__':
    a = Patient()
    print(a.json)
