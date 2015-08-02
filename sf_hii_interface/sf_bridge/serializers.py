from rest_framework import serializers
from models import APIFromSF


class ApiFromSFSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIFromSF
        field = ('user_name', 'full_post', 'url_quote', 'url_Question', 'url_Enrrollment', 'product')







