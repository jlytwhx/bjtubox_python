class Field:
    information = {
        'label': '',
        'name': '',
        'value': '',
        'placeholder': '',
        'hidden': False,
        'marginTop': False,
        'disable': False,
        'notnull': False
    }

    def __init__(self, **kwargs):
        self.information.update(kwargs)

    def to_dict(self):
        return self.information

    def __getattr__(self, key):
        if key in self.information:
            return self.information[key]
        else:
            raise AttributeError(r"'%s' object has no attribute '%s'" % (self.__class__, key))

    def __setattr__(self, key, value):
        self.information[key] = value


class InputField(Field):
    def __init__(self, label, placeholder='', value='', **kwargs):
        if not placeholder:
            placeholder = '请输入{}'.format(label)
        super().__init__(label=label, placeholder=placeholder, value=value, type='input', **kwargs)


class SelectorField(Field):
    def __init__(self, label, data, placeholder='', value=0, **kwargs):
        if not placeholder:
            placeholder = '请选择{}'.format(label)
        data = [{'id': p[0], 'name': p[1]} for p in data]
        super().__init__(label=label, placeholder=placeholder, data=data, value=value, type='selector',
                         **kwargs)


class TextAreaField(Field):
    def __init__(self, label, placeholder='', value='', **kwargs):
        if not placeholder:
            placeholder = '请输入{}'.format(label)
        super().__init__(label=label, placeholder=placeholder, value=value, type='textarea', **kwargs)


class SwitchField(Field):
    def __init__(self, label, value=False, **kwargs):
        super().__init__(label=label, value=value, type='switch', **kwargs)


if __name__ == '__main__':
    a = InputField(name='name', label='姓名')
    a.name = 'dddd'
    print(a.name)
