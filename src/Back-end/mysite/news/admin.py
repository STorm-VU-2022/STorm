from django.contrib import admin
from .models import Publication, Subject, Comments


class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'language', 'student_year', 'is_public', 'subject', 'short_description', 'created_at', 'edited_at', )
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'short_description', 'id')
    list_editable = ('is_public', )
    list_filter = ('is_public', 'subject', )


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'comment', 'publication', 'teacher', 'comment_date')
    list_display_links = ('pk', 'comment', 'publication')


# Register your models here.
admin.site.register(Publication, PublicationsAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Comments, CommentsAdmin)
