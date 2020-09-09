from django.contrib import admin
from .models import Upload, Document


class DocumentInline(admin.StackedInline):
    model = Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'hash', 'hash_secure']
    inlines = [DocumentInline]
