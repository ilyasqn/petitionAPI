from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'petition', views.ApiPetitionViewSet)

urlpatterns = [
    path('', include(router.urls), name='petition'),
    path('/<int:pk>/', include(router.urls), name='petition-detail'),
    path('/<int:pk>/sign/', include(router.urls), name='petition-sign'),
    path('/<int:pk>/resign/', include(router.urls), name='petition-resign'),


    path('register/', views.api_register, name='register'),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),


    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
