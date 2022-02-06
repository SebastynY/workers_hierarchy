from django.contrib import admin
from core.models import Worker


class WorkerAdmin(admin.ModelAdmin):
    list_filter = ('position',)
    search_fields = ('first_name', 'last_name',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'date_hired', 'salary', 'position')
        }),
    )


admin.site.register(Worker, WorkerAdmin)
