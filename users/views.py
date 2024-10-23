from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .models import CustomUser  # Use CustomUser
from .serializers import ChangePasswordSerializer, UserSerializer, LoginSerializer  # Import both serializers
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated


class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to My Django REST API"}, status=status.HTTP_200_OK)


class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Reference LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Fetch the user based on the username
        user = CustomUser.objects.filter(username=username).first()
        
        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'role': user.role, 
                'username': user.username,  
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        
        return Response({'error': 'Invalid credentials'}, status=400)

class PasswordResetView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        # Check if email is provided
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to find the user by email
            user = CustomUser.objects.filter(email=email).first()
            
            if user:
                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f'http://localhost:8000/api/password_reset/confirm/{uid}/{token}/'  # Update with your domain

                # Instead of sending the email, return the reset link in the response
                return Response({'reset_link': reset_link}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Log the exception (optional)
            return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class PasswordResetConfirmView(generics.GenericAPIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    return Response({'success': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)