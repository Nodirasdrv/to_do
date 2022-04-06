from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

USER_TYPE_CHOICES = (
    ('owner', 'Owner'),
    ('reader', 'Reader'),
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'user_type')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if not user.exists:
            raise ValidationError('email exists')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password2 != password:
            raise ValidationError('passwords do not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user