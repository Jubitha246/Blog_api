from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet,LoginViewSet,BlogViewSet,CommentViewSet

router = DefaultRouter()
router.register(r'register',RegisterViewSet,basename='register')
router.register(r'login',LoginViewSet,basename='login')
router.register(r'blogs',BlogViewSet,basename='blogs')
router.register(r'comments',CommentViewSet,basename='comments')

urlpatterns = router.urls

