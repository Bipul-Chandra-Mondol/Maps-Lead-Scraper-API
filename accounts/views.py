from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"detail": "Registration successful", "email": user.email},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # IMPORTANT: authenticate এ username হিসেবে email পাঠাই, 
        # কারণ AUTH_USER_MODEL.USERNAME_FIELD = "email"
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        response = Response({"detail": "Login successful"}, status=status.HTTP_200_OK)

        # Access Token Cookie
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=True,   # dev এ False করতে পারো
            samesite="Lax",
        )

        # Refresh Token Cookie
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.COOKIES.get("refresh_token")

        if refresh:
            try:
                token = RefreshToken(refresh)
                token.blacklist()
            except Exception:
                # already blacklisted / invalid → ignore
                pass

        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


# manually refresh access token using refresh token cookie
class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token cookie missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)

            response = Response(
                {"detail": "Access token refreshed successfully"},  
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                "access_token",
                new_access,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            return response

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

