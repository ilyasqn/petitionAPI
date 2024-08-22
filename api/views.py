from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Petition, Signature
from .serializers import PetitionSerializer, SignatureSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'API Overview':'',
		'Petition List':'/petitions/',
		'Petition Create ':'/petition/create/',
		'Petition Delete':'/petition/delete/<int:pk>/',
		'Petition Resign ': '/petition/resign/<int:pk>/',
		'Petition Sign': '/petition/sign/<int:pk>/',
		'User Create': '/register/',
        'User Login': '/login/',
        'User Token Refresh': '/token/refresh/',
        'User Token Verify': '/token/verify'
	}

	return Response(api_urls)

@api_view(['POST'])
def apiRegister(request):
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

class apiTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class apiPetitionCreateView(generics.CreateAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
@api_view(['GET'])
def apiPetitionList(request):
    petitions = Petition.objects.all()
    serializer = PetitionSerializer(petitions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apiSignPetition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    vote_is_exist = Signature.objects.filter(user=request.user, petition=petition).exists()

    if not vote_is_exist:
        signature = Signature(petition=petition, user=request.user)
        signature.save()
        return Response({'message': 'Signature added successfully'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Signature already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def apiResignPetition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    vote = Signature.objects.filter(user=request.user, petition=petition).first()

    if vote:
        vote.delete()
        return Response({'message': 'Signature removed successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'message': 'No signature found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def apiDeletePetition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)

    if petition.author == request.user:
        petition.delete()
        return Response({'message': 'Petition deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'message': 'You are not who create this petition'}, status=status.HTTP_403_FORBIDDEN)