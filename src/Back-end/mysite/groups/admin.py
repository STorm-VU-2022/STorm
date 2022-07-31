from django.contrib import admin
from .models import Methodic_group, Participates_in, Invites


class Methodic_groupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'creation_date', )
    list_display_links = ('pk', 'name',)
    search_fields = ('name', )


class Participates_inAdmin(admin.ModelAdmin):
    list_display = ('member', 'group', 'is_accepted', )


class InvitesAdmin(admin.ModelAdmin):
    list_display = ('invited_user', 'group', 'invitation_date', )


admin.site.register(Methodic_group, Methodic_groupAdmin)
admin.site.register(Participates_in, Participates_inAdmin)
admin.site.register(Invites, InvitesAdmin)