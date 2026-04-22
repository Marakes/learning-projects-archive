from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)
    ordering = ('-created_at',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_display_links = ('name',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    ordering = ('-created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'location',
        'pub_date', 'is_published', 'created_at'
    )
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'text', 'author__username',
                     'category__title', 'location__name')
    list_filter = ('pub_date', 'is_published', 'category', 'location')
    ordering = ('-pub_date', '-created_at')

    @admin.display(boolean=True, description='Опубликовано')
    def is_published(self, obj):
        return obj.is_published
