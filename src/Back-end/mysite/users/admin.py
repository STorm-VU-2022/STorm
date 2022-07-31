from django.contrib import admin

from .models import Teacher, Recommends


class TeachersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'email', 'self_description', 'facebook_link', 'twitter_link', 'instagram_link', 'linkedin_link', )
    list_display_links = ('pk', 'full_name', )
    search_fields = ('full_name', )


class RecommendsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recommender', 'recommended', 'recommendation_text')


admin.site.register(Teacher, TeachersAdmin)
admin.site.register(Recommends, RecommendsAdmin)