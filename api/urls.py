from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

router = DefaultRouter()

router.register(r'petitions', views.ApiPetitionViewSet, basename='petition')


urlpatterns = [
    path('', include(router.urls), name='petitions'),
    path('<int:pk>/', include(router.urls), name='petition-detail'),
    path('<int:pk>/sign/', include(router.urls), name='petition-sign'),
    path('<int:pk>/resign/', include(router.urls), name='petition-resign'),


    path('signup/', views.user_signup, name='signup'),
    path('login/', views.TokenObtainPairView.as_view(), name='login'),


    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
