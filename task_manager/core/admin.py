from django.contrib import admin
from .models import User
# --------------------------------------------------------------------------


class SiteAdmin(admin.ModelAdmin):

    list_filter = ('is_staff', 'is_active', 'is_superuser')
    list_display = ('username', 'email', 'first_name', 'last_name', 'password')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')
    list_editable = ('password', )

    def save_model(self, request, obj, form, change):

        password = request.POST.get('form-0-password')
        if change and password:
            obj.set_password(password)
            obj.save()

        super().save_model(request, obj, form, change)


admin.site.register(User, SiteAdmin)
