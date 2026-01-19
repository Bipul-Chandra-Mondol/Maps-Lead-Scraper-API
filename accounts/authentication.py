from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    - প্রথমে access_token cookie থেকে নেয়
    - valid থাকলে normal ভাবে চলবে
    - invalid/expired হলে refresh_token দিয়ে নতুন access issue করবে
    """

    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            # DRF অন্য authentication ব্যবহার করতে পারে, তাই None
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token

        except (InvalidToken, TokenError):
            # Access token invalid/expired → try refresh
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                raise AuthenticationFailed("Refresh token missing")

            try:
                refresh = RefreshToken(refresh_token)
                # validate refresh, and create new access
                new_access = str(refresh.access_token)

                # এই নতুন access কে request এর header এ বসাচ্ছি
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                # middleware পরবর্তীতে cookie update করবে
                request._new_access_token = new_access

                # get_user এর জন্য token object দরকার, তাই refresh.access_token ব্যবহার
                return self.get_user(refresh.access_token), refresh.access_token

            except Exception:
                raise AuthenticationFailed("Session expired")
