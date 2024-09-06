from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Petition, Signature
from .serializers import PetitionSerializer
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters
from .filters import PetitionFilter


# Create your views here.

@api_view(['GET'])
def api_overview(request):
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
    filter_class = PetitionFilter
    ordering_fields = '__all__'
    ordering = ['-pub_date']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def check_author_and_perform_action(self, request, petition, action, *args, **kwargs):
        if petition.author == self.request.user or self.request.user.is_superuser:
            return action(request, *args, **kwargs)
        return Response({'message': 'You are not who create this petition or admin'}, status=status.HTTP_403_FORBIDDEN)

    def check_vote_is_exist(self, request, petition):
        return Signature.objects.filter(user=request.user, petition=petition).exists()

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')

        if Petition.objects.filter(title=title).exists():
            return Response({'message': 'Petition already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        petition = self.get_object()
        return self.check_author_and_perform_action(request, petition, super().destroy, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        petition = self.get_object()
        return self.check_author_and_perform_action(request, petition, super().update, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        petition = self.get_object()
        return self.check_author_and_perform_action(request, petition, super().partial_update, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def sign(self, request, *args, **kwargs):
        petition = self.get_object()

        if self.check_vote_is_exist(request, petition):
            return Response({'message': 'Signature already exists'}, status=status.HTTP_400_BAD_REQUEST)
        Signature.objects.create(user=request.user, petition=petition)
        return Response({'message': 'Signature added successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def resign(self, request, *args, **kwargs):
        petition = self.get_object()

        if self.check_vote_is_exist(request, petition):
            return Response({'message': 'Signature resigned successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'No signatures found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def sign_petition(request, pk):
#     petition = get_object_or_404(Petition, pk=pk)
#     vote_is_exist = Signature.objects.filter(user=request.user, petition=petition).exists()
#
#     if not vote_is_exist:
#         signature = Signature(petition=petition, user=request.user)
#         signature.save()
#         return Response({'message': 'Signature added successfully'}, status=status.HTTP_201_CREATED)
#     return Response({'message': 'Signature already exists'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def resign_petition(request, pk):
#     petition = get_object_or_404(Petition, pk=pk)
#     vote = Signature
#     vote.objects.filter(user=request.user, petition=petition)
#
#     if vote:
#         vote.delete()
#         return Response({'message': 'Signature removed successfully'}, status=status.HTTP_204_NO_CONTENT)
#     return Response({'message': 'No signature found'}, status=status.HTTP_404_NOT_FOUND)
