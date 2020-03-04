from django.db import models
from person.models import Person


# Create your models here.
class BigData(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    first_ill_time = models.DateTimeField(null=True, blank=True)
    engel_num = models.FloatField()
    shower_cost = models.FloatField(null=True, blank=True)
    eat_cost = models.FloatField(null=True, blank=True)
    hospital_cost = models.FloatField(null=True, blank=True)
    shop_cost = models.FloatField(null=True, blank=True)
    electric_cost = models.FloatField(null=True, blank=True)
    computer_cost = models.FloatField(null=True, blank=True)
    water_cost = models.FloatField(null=True, blank=True)
    sum_cost = models.FloatField(null=True, blank=True)

    shower_num = models.IntegerField(null=True, blank=True)
    eat_num = models.IntegerField(null=True, blank=True)
    hospital_num = models.IntegerField(null=True, blank=True)
    shop_num = models.IntegerField(null=True, blank=True)
    electric_num = models.IntegerField(null=True, blank=True)
    computer_num = models.IntegerField(null=True, blank=True)
    water_num = models.IntegerField(null=True, blank=True)

    lost_card_num = models.IntegerField()
    lost_card_min = models.IntegerField()
    breakfast_num = models.IntegerField()
    lunch_num = models.IntegerField()
    dinner_num = models.IntegerField()
    breakfast_cost = models.FloatField()
    lunch_cost = models.FloatField()
    dinner_cost = models.FloatField()
