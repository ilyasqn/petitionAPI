from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Petition, Signature

# Create your tests here.

class PetitionApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123")
        self.petition = Petition.objects.create(title="PyTest Petition", description="Test Description", author=self.user)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_petition_create(self):
        data = {
            "title": "Test Petition",
            "description": "Test Description"
        }
        response = self.client.post("/api/petitions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_petitions(self):
        response = self.client.get("/api/petitions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_petition(self):
        response = self.client.get(f"/api/petitions/{self.petition.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_petition(self):
        data = {
            "title": "Updated Petition",
            "description": "Updated Description"
        }
        response = self.client.put(f"/api/petitions/{self.petition.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_parital_update_petition(self):
        data = {
            "title": "Partial Updated Petition",
            "description": "Updated Description"
        }
        response = self.client.patch(f"/api/petitions/{self.petition.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_petition(self):
        response = self.client.delete(f"/api/petitions/{self.petition.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_sign_petition(self):
        response = self.client.post(f"/api/petitions/{self.petition.id}/sign/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_resign_petition(self):
        Signature.objects.create(user=self.user, petition=self.petition)
        response = self.client.delete(f"/api/petitions/{self.petition.id}/resign/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



