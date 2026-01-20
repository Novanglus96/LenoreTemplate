from django.contrib import admin
from ad_users.models import ActiveDirectoryUser
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class ActiveDirectoryUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["employee_id", "display_name", "email", "when_changed"]

    list_display_links = ["display_name"]

    ordering = ["sur_name", "given_name", "employee_id", "id"]


admin.site.register(ActiveDirectoryUser, ActiveDirectoryUserAdmin)
