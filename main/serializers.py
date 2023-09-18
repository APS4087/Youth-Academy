from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','staff_username','staff_name','staff_email','staff_phNumber','staff_password','staff_address']