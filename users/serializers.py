from rest_framework import serializers

from users.models import User



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone']  # Add other fields as needed
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},  # Ensure password is required and write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)  # Use set_password() for hashing
        instance.save()
        return instance