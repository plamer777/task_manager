from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True
    )

    password_repeat = serializers.CharField(
        write_only=True
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)

        return new_user

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.get('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError(
                {'password, password_repeat': 'Passwords do not match'})
        validate_password(password)
        attrs.pop('password_repeat', None)

        return super().validate(attrs)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=30,
        write_only=True,
        required=True
    )
    new_password = serializers.CharField(
        max_length=30,
        write_only=True,
        required=True
    )
    password = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('new_password', 'old_password', 'password')

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate(self, attrs):
        new_password = attrs.pop('new_password', None)
        old_password = attrs.pop('old_password', None)
        request = self.context.get('request')
        user = request.user

        found_user = authenticate(
            username=user.username,
            password=old_password)

        if not found_user:
            raise serializers.ValidationError(
                {'old_password': 'The password you entered is incorrect'}
            )

        validate_password(new_password)
        attrs['password'] = new_password
        return super().validate(attrs)
