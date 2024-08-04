from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

import random
from .serializers import (
    RegisterSerializer, UserSerializer, LoginSerializer,
    OTPVerificationSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, PasswordResetOTPVerificationSerializer
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from checkout.models import ShoppingCart

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        ShoppingCart.objects.create(user=user)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # print(self.request.user.first_name, "----------------")
        return self.request.user

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_200_OK)

class OTPVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send email
        subject = 'Account Activated'
        message = 'Your account has been activated successfully.'
        from_email = 'your_email@example.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        user.otp = str(random.randint(100000, 999999))
        user.is_active = False
        user.save()
        # Send OTP via email
        subject = 'Password reset otp code'
        message = f'{user.get_full_name()}, your password reset otp code is {user.otp}'
        user.email_user(subject, message)
        return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)


class PasswordResetOTPVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetOTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # # Send email
        # subject = 'Reset Password'
        # message = 'You can set new password now.'
        # from_email = 'your_email@example.com'
        # recipient_list = [user.email]

        # send_mail(subject, message, from_email, recipient_list)

        return Response({"detail": "You can reset new password"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)


# class LogoutView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=204)
#         except Exception as e:
#             return Response(status=400)
        

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

