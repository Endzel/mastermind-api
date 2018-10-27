from django.contrib import admin
from django.utils.translation import ugettext as _

from mastermind.models import *

admin.site.site_header = _('Mastermind admin')
admin.site.index_title = _('Administration')
admin.site.site_title = _('Mastermind admin')


class CustomUserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # Encrypt password from admin if it's not encrypted
        if obj.password and not obj.password[0:20] == 'pbkdf2_sha256$36000$':
            obj.set_password(obj.password)
        super(CustomUserAdmin, self).save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)
admin.site.register(Play)
admin.site.register(Code)
admin.site.register(Feedback)
