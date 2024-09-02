from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters
from .filters import PetitionFilter


# Create your views here.

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'API Overview': '',
        'Petition List': '/petitions/',
        'Petition Create ': '/petition/create/',
        'Petition Delete': '/petition/delete/<int:pk>/',
        'Petition Resign ': '/petition/resign/<int:pk>/',
        'Petition Sign': '/petition/sign/<int:pk>/',
        'User Create': '/register/',
        'User Login': '/login/',
        'User Token Refresh': '/token/refresh/',
        'User Token Verify': '/token/verify'
    }

    return Response(api_urls)


@api_view(['POST'])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


class ApiTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class ApiPetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PetitionFilter
    ordering_fields = '__all__'
    ordering = ['-pub_date']

    def is_author_or_superuser(self, petition):
        return petition.author == self.request.user or self.request.user.is_superuser
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'message': 'You are not authorized to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            petition = self.get_object()
            if self.is_author_or_superuser(petition):
                return super().destroy(request, *args, **kwargs)
            return Response({'message': 'You are not who create this petition or an admin'}, status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'message': 'You are not authorized to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            petition = self.get_object()
            if self.is_author_or_superuser(petition):
                return super().partial_update(request, *args, **kwargs)
            return Response({'message': 'You are not who create this petition or an admin'}, status=status.HTTP_403_FORBIDDEN)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sign_petition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    vote_is_exist = Signature.objects.filter(user=request.user, petition=petition).exists()

    if not vote_is_exist:
        signature = Signature(petition=petition, user=request.user)
        signature.save()
        return Response({'message': 'Signature added successfully'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Signature already exists'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def resign_petition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    vote = Signature
    vote.objects.filter(user=request.user, petition=petition)

    if vote:
        vote.delete()
        return Response({'message': 'Signature removed successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'message': 'No signature found'}, status=status.HTTP_404_NOT_FOUND)

