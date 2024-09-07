from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Petition, Signature


class PetitionSerializer(serializers.ModelSerializer):
    signatures_count = serializers.SerializerMethodField()

    class Meta:
        model = Petition
        fields = ['id', 'title', 'description', 'pub_date', 'author', 'signatures_count']
        read_only_fields = ['author', 'pub_date']

    def get_signatures_count(self, obj):
        return Signature.objects.filter(petition=obj).count()

