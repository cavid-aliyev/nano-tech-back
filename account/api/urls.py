from django.urls import path
from account.api.views import RegisterView, UserDetailView, LogoutView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'account'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]