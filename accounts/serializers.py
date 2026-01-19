from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "email", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password and Confirm Password must match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    SimpleJWT default username ফিল্ড ব্যবহার করে; 
    আমরা USERNAME_FIELD=email করে রেখেছি, তাই এখানে কিছু override করার দরকার খুব বেশি নেই।
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # extra claims add করতে চাইলে:
        token["email"] = user.email
        return token
