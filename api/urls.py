from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = SimpleRouter()
router.register(r'petition', views.ApiPetitionViewSet)

urlpatterns = [
    path('', include(router.urls), name='petition'),
    path('/<int:pk>/', include(router.urls)),


    path('register/', views.api_register, name='register'),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),


    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]