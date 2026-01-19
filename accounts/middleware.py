class RefreshTokenMiddleware:
    """
    Authentication class যদি নতুন access token জেনারেট করে,
    তাহলে request._new_access_token এ সেট করে দেয়।
    এই middleware response এ সেই token কে cookie তে বসিয়ে দেয়।
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, "_new_access_token"):
            response.set_cookie(
                "access_token",
                request._new_access_token,
                httponly=True,
                secure=True,      # dev এ test করতে চাইলে False
                samesite="Lax",
            )

        return response
