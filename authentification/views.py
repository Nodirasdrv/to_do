from django.shortcuts import redirect
from rest_framework import response, status

from rest_framework.views import APIView

from authentification.serializers import UserSerializer
from django.contrib.auth import get_user_model

from authentification.services import send_message

User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_message(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        # return response.Response


class ActivateUserAccount(APIView):
    def get(self, request, activation_code):
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect('index.html')
