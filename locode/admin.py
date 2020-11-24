from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Locode)
class LocodeAdmin(admin.ModelAdmin):
    list_display = 'locode', 'country_code', 'location_code', 'name', 'name_wo_diacritics', '_functions',
    list_filter = 'functions',
    search_fields = 'locode', 'name_wo_diacritics'
    filter_horizontal = 'functions',

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('functions')

    def _functions(self, obj):
        return ', '.join([i.name for i in obj.functions.all()])
