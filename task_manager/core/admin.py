"""This unit contains SiteAdmin model to represent User model in the admin
panel"""
from django.contrib import admin
from .models import User
# --------------------------------------------------------------------------


class SiteAdmin(admin.ModelAdmin):
    """SiteAdmin class serves to represent a User model in the Django admin
    panel"""
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    list_display = ('username', 'email', 'first_name', 'last_name', 'password')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')
    list_editable = ('password', )

    def save_model(self, request, obj, form, change) -> None:
        """This method was overwritten to hash the password"""
        password = request.POST.get('form-0-password')
        if change and password:
            obj.set_password(password)
            obj.save()

        super().save_model(request, obj, form, change)


admin.site.register(User, SiteAdmin)
