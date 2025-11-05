from django.db import models
from django.conf import settings


class Journal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    issn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Issue(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='issues')
    volume = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('journal', 'volume', 'number')
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.journal.title} - Vol. {self.volume}, No. {self.number}"


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Article(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='articles')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    title = models.CharField(max_length=255)
    abstract = models.TextField(help_text="Short summary of the article")
    content = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='articles/pdfs/', blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    publish_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title


class ArticleAuthor(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_authors')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_articles')
    order = models.PositiveIntegerField(default=1, help_text="Author order in article (1=first author)")
    is_corresponding = models.BooleanField(default=False, help_text="Is this the corresponding author?")

    objects = models.Manager()

    class Meta:
        unique_together = ('article', 'author')
        ordering = ['order']

    def __str__(self):
        return f"{self.author} — {self.article.title}"
