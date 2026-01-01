from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


# ---------------------------
# CURRENT USER SERIALIZER
# ---------------------------
class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "username",
            "email",
            "country",
            "state",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# ---------------------------
# REGISTER SERIALIZER
# ---------------------------
class RegisterSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)

    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    username = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already exists")]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists"
            )
        ],
    )

    country = serializers.CharField(required=True, max_length=50)
    state = serializers.CharField(required=True, max_length=50)

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("confirm_password")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

        if len(password1) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in password1):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password1):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password1):
            raise serializers.ValidationError("Password must contain at least one number")

        special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?/`~"
        if not any(c in special_chars for c in password1):
            raise serializers.ValidationError("Password must contain at least one special character")

        attrs.pop("confirm_password")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            country=validated_data["country"],
            state=validated_data["state"],
        )
        return user


# ---------------------------
# LOGIN SERIALIZER
# ---------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)