from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register('',views.PetitionViewSet)

urlpatterns = [
    path('', views.apiOverview, name='api_overview'),
    path('petitions/', include(router.urls)),
    path('petition/create/', views.apiPetitionCreateView.as_view(), name='api_petition_create'),
    path('petition/sign/<int:pk>/', views.apiSignPetition, name='api_sign_petition'),
    path('petition/resign/<int:pk>/', views.apiResignPetition, name='api_resign_petition'),
    path('petition/delete/<int:pk>/', views.apiDeletePetition, name='api_delete_petition'),
    path('register/', views.apiRegister, name='register'),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]