from django.contrib import admin
from .models import Site, Controller, PonemusCustomer, CustomerSite
# Register your models here.

@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display_links = (
        'id',
        'uuid'
    )
    list_display = [
        'id',
        'uuid',
        'kind',
        'host',
        'port',
        'username',
        'password'
    ]


@admin.register(PonemusCustomer)
class PonemusCustomerAdmin(admin.ModelAdmin):
    list_display_links = (
        'id',
        'uuid'
    )
    list_display = [
        'id',
        'uuid',
        'name',
        'created_at',
        'controller',
    ]



@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display_links = (
        'id',
        'uuid'
    )

    list_display = [
        'id',
        'uuid',
        'customer',
        'controller',
        'site_id',
        'site_name',
        'slug',
        'default_group_id'
    ]

    actions = [
        'remove'
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def remove(self, request, queryset):
        for instance in queryset:
            instance.delete_site()

    remove.description = 'Remove Site'


@admin.register(CustomerSite)
class CustomerSiteAdmin(admin.ModelAdmin):
    list_display_links = (
        'id',
        'uuid'
    )
    list_display = [
        'id',
        'uuid',
        'site',
        'mac_address',
        'user_group_id',
        'name',
        'device',
        'user_agent',
        'created_at',
    ]