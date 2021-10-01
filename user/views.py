from django.shortcuts import render
from .serializers import  RefreshTokenSerializer, SignupSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import GenericAPIView

# Create your views here.
class Register(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(GenericAPIView):
    """This API Take a valid refresh token from the current user then he destroy it so
        you can't use it any more and you then delete the 'access_token' from your local storege and redirect the user to the login page.

    """
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response({"message": "Your are logged out!"},status=status.HTTP_204_NO_CONTENT)