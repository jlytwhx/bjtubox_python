from django.contrib import admin
from .models import Person, Group


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]


admin.site.register(Person, PersonAdmin)
admin.site.register(Group)
