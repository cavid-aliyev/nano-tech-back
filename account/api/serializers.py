from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
import random
from datetime import datetime

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'email', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['email'] and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Check if full name contains at least two parts
        full_name_parts = data['full_name'].strip().split()
        if len(full_name_parts) < 2:
            raise serializers.ValidationError("Please enter both a first name and a last name.")
        
        return data

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        first_name, last_name = full_name.split(' ', 1)  # Split full name into first and last name
        full_name_parts = full_name.strip().split()
        user = User.objects.create_user(
            username="".join(full_name_parts) + '-' + str(datetime.now().timestamp()).replace('.',''),
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )
        user.otp = str(random.randint(100000, 999999))
        user.save()
        # Send OTP via email
        subject = 'Your account activation code'
        message = f'Your activation code is {user.otp}'
        user.email_user(subject, message)
        return user

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_active', "first_name", "last_name"]

    def get_full_name(self, obj):
        return obj.get_full_name()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            # print(user, "----------------")
            if user is None:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("Account is not activated")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        try:
            user = User.objects.get(email=email, otp=otp)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email")
        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.otp = ''
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID")

        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid token")

        return data

    def save(self):
        uid = self.validated_data['uidb64']
        user = User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
        user.set_password(self.validated_data['new_password'])
        user.save()