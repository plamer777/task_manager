from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import User
from core.serializers import UserRegisterSerializer, UserLoginSerializer, \
    UserUpdateRetrieveSerializer, UserUpdatePasswordSerializer


def main_page(request):
    return JsonResponse({"status": "ok"}, status=200)


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        pass

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                {'username, password': 'Username or password is incorrect'})
        request.data['password'] = user.password
        login(request, user)

        return super().create(request, *args, **kwargs)


class UserUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_set = User.objects.filter(pk=self.request.user.pk)
        self.kwargs['pk'] = self.request.user.pk
        return query_set

    @method_decorator(ensure_csrf_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'status': 'success'}, status=204)


class UserUpdatePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.request.user.pk)
        self.kwargs['pk'] = self.request.user.pk

        return queryset
