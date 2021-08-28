from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class Entry(admin.ModelAdmin):
    list_display = (
        'entry_id',
        'hatena_entry_id',
        'title',
        'updated_at',
        'edited_at',
        'deleted_at'
    )

    def get_queryset(self, request):
        return self.model.entire.all()
