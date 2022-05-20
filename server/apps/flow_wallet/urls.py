from server.apps.flow_wallet.views import AccountViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='user')
urlpatterns = router.urls
