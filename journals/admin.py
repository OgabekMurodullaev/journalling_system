from django.contrib import admin
from .models import Journal, Issue, Section, Article, ArticleAuthor


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'issn', 'publisher', 'created_at')
    search_fields = ('title', 'issn', 'publisher')
    ordering = ('-created_at',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('journal', 'volume', 'number', 'publication_date')
    list_filter = ('journal',)
    search_fields = ('journal__title',)
    ordering = ('-publication_date',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class ArticleAuthorInline(admin.TabularInline):
    model = ArticleAuthor
    extra = 1
    ordering = ('order',)
    autocomplete_fields = ('author',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue', 'section', 'publish_date', 'is_published')
    list_filter = ('section', 'issue', 'publish_date', 'is_published')
    search_fields = ('title', 'abstract', 'keywords')
    ordering = ('-publish_date',)
    date_hierarchy = 'publish_date'
    inlines = [ArticleAuthorInline]


@admin.register(ArticleAuthor)
class ArticleAuthorAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'order', 'is_corresponding')
    list_filter = ('article', 'is_corresponding')
    search_fields = ('article__title', 'author__full_name')
    ordering = ('article', 'order')