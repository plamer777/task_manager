"""This file contains vies to realize CRUD operations with User model"""
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import serializers
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserUpdateRetrieveSerializer,
    UserUpdatePasswordSerializer,
)

# -------------------------------------------------------------------------


class UserRegistrationView(CreateAPIView):
    """This view serves to register a new user"""

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserLoginView(CreateAPIView):
    """This view serves to realize a login process for an existing user"""

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer) -> None:
        """The method was rewritten to avoid saving User object"""
        pass

    def create(self, request, *args, **kwargs) -> Response:
        """The method serves to authenticate the user and to save his data
        into current session"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                {"username, password": "Username or password is incorrect"}
            )
        request.data["password"] = user.password
        login(request, user)

        return super().create(request, *args, **kwargs)


class UserUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    """This view serves to get and update user data such as first name,
    last name, etc. and logout from the current session"""

    queryset = User.objects.all()
    serializer_class = UserUpdateRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @method_decorator(ensure_csrf_cookie)
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def partial_update(self, request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> JsonResponse:
        logout(request)
        return JsonResponse({"status": "success"}, status=204)


class UserUpdatePasswordView(UpdateAPIView):
    """This view allows to update user's password"""

    queryset = User.objects.all()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user
