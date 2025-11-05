from rest_framework.routers import DefaultRouter
from .views import JournalViewSet, IssueViewSet, SectionViewSet, ArticleViewSet, ArticleAuthorViewSet

router = DefaultRouter()
router.register(r'journals', JournalViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'article-authors', ArticleAuthorViewSet)

urlpatterns = router.urls
