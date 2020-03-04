from django.contrib import admin
from .models import Lost, Comment
from django.utils.html import format_html


# Register your models here.
class LostAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("time", "content", "show_image", "show")
    search_fields = ("time", "content")
    list_filter = ("content", "show")
    list_editable = ["show"]
    ordering = ("-time",)
    fieldsets = [
        (None, {'fields': ['title']}),
        ('price information', {'fields': ['price', "publisher"], 'classes': ['collapse']}),
    ]

    def show_image(self, obj):
        if obj.image:
            return format_html('<a href="%s%s">%s</a>' % ('https://mp.bjtu.edu.cn/file/user/image/', obj.image, '图片'))
        else:
            return ''


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("time", "content", "show")
    search_fields = ("time", "content")
    list_filter = ("content", "show")
    list_editable = ["show"]
    ordering = ("-time",)


admin.site.register(Lost, LostAdmin)
admin.site.register(Comment, CommentAdmin)
