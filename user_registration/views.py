from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

class RegisterUserAPIView(APIView):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return Response({
                "status": True,
                "message": "success",
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "status": False,
                "message": "Invalid email or password",
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    authentication = ()
    permission_classes = ()

    def post(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)