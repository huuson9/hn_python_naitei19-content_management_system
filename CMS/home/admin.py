from django.contrib import admin
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin): 
    list_display = [
        'title',
        'content',
        'author',
        'status',
        'category',
        'created_at',
        'updated_at',
    ]

    search_fields = ['title','author',]

    list_filter = ['category']

    list_display_links = ['title']

    list_editable = (
        'content', 
        'status', 
        'category'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(status = 3)

class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
