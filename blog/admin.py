from django.contrib import admin
from blog.models import Post, Category

from pagedown.widgets import AdminPagedownWidget
from django.db import models


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    date_hierarchy = "created_at"
    fields = ("published", "title", "slug", "category", "author", "content")
    list_display = ["published", "title", "updated_at",
                    "created_at", "author", "category"]
    list_display_links = ["title"]
    list_editable = ["published"]
    list_filter = ["published", "updated_at", "author", "category"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "content"]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
