from django.test import TestCase

# Create your tests here.
if __name__ == '__main__':
    a = {
        'a': ['a', 'b'],
        'b': ['b', ],
        'c': list()
    }
    search_dict = dict()
    for k in a:
        if a[k]:
            search_dict[k] = a[k][0]
    print(search_dict)
