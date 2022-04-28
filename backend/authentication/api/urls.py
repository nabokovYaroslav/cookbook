from django.urls import path

from authentication.api.views import TokenObtainPairCookieView, TokenRefreshCookieView


urlpatterns = [
    path('token/', TokenObtainPairCookieView.as_view(), name='token_obtain_pair_cookie'),
    path('token/refresh/', TokenRefreshCookieView.as_view(), name='token_refresh_cookie'),
]
