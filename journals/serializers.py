from rest_framework import serializers

from journals.models import Journal, Issue, Section, Article, ArticleAuthor


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'title', 'description', 'issn', 'publisher', 'created_at']
        read_only_fields = ['id', 'created_at']


class IssueSerializer(serializers.ModelSerializer):
    journal_title = serializers.CharField(source='journal.title', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'journal',
            'journal_title',
            'volume',
            'number',
            'publication_date',
            'description'
        ]
        read_only_fields = ['id', 'journal_title']

    def validate(self, attrs):
        journal = attrs.get('journal')
        volume = attrs.get('volume')
        number = attrs.get('number')

        if Issue.objects.filter(journal=journal, volume=volume, number=number).exists():
            raise serializers.ValidationError(
                "Bu journal uchun shu Volume va Number allaqachon mavjud."
            )
        return attrs


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'description']


class ArticleAuthorSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField(source='author.get_full_name', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)

    class Meta:
        model = ArticleAuthor
        fields = [
            'id',
            'article',
            'article_title',
            'author',
            'author_full_name',
            'order',
            'is_corresponding'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    issue_title = serializers.CharField(source='issue.journal.title', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    article_authors = ArticleAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'issue',
            'issue_title',
            'section',
            'section_name',
            'title',
            'abstract',
            'content',
            'pdf_file',
            'keywords',
            'publish_date',
            'is_published',
            'created_at',
            'article_authors'
        ]