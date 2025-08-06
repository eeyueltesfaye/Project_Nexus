from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, RoleRequest
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, RoleRequestSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
            "token": token
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_tokens_for_user(user)

            # Default redirect
        redirect_url = '/api/jobs/'

        # Skip redirect logic for superusers
        if user.is_superuser:
            redirect_url = '/admin/' 

        # Handle incomplete profile (only for non-superusers)
        elif hasattr(user, 'profile') and not user.profile.profile_completed:
            redirect_url = '/api/users/profile/update/'

        return Response({
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "profile_completed": user.profile.profile_completed if hasattr(user, 'profile') else False,
            },
            "token": token,
            "redirect": redirect_url
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        


class ProfileStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        profile = serializer.save()
        profile.check_completion()


class ResumeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        if not profile.resume:
            raise Http404("Resume not found.")
        return FileResponse(profile.resume.open(), as_attachment=True, filename="resume.pdf")
    


class RoleRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'JOB_SEEKER':
            return Response({'detail': 'Only job seekers can request role changes.'}, status=400)

        if RoleRequest.objects.filter(user=request.user, reviewed=False).exists():
            return Response({'detail': 'You already have a pending request.'}, status=400)

        serializer = RoleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        RoleRequest.objects.create(
            user=request.user,
            requested_role=serializer.validated_data['requested_role'],
            reason=serializer.validated_data['reason']
        )
        return Response({'detail': 'Role request submitted successfully.'}, status=201)
