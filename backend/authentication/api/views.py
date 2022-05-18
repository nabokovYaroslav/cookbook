from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.api.serializers import MyTokenObtainPairSerializer


class TokenObtainPairCookieView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop("refresh")
        response.set_cookie("refresh", refresh, httponly=True)
        return response

class TokenRefreshCookieView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            request.data["refresh"] = request.COOKIES.get("refresh")
        except KeyError:
            pass
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop("refresh")
        response.set_cookie("refresh", refresh, httponly=True)

        return response