from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.views import BaseViewSet
from .models import Journal, Issue, Section, Article, ArticleAuthor
from .serializers import JournalSerializer, IssueSerializer, SectionSerializer, ArticleSerializer, \
    ArticleAuthorSerializer


class JournalViewSet(BaseViewSet):
    queryset = Journal.objects.all().order_by('-created_at')
    serializer_class = JournalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class IssueViewSet(BaseViewSet):
    queryset = Issue.objects.select_related('journal').all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SectionViewSet(BaseViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(BaseViewSet):
    queryset = Article.objects.select_related('issue', 'section').prefetch_related('article_authors__author')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleAuthorViewSet(BaseViewSet):
    queryset = ArticleAuthor.objects.select_related('article', 'author')
    serializer_class = ArticleAuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]