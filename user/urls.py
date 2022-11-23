from django.urls import path
from rest_framework_simplejwt.views import ( #simplejwt 기본 기능 import, simplejwt 공식문서 참고
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView, mockView, CustomTokenObtainPairView
 
urlpatterns = [
    path('signup/', UserView.as_view(), name='user_view'), #회원가입 URL
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), #token key 발급받기 위한 API    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #refresh key 발급받기 위한 API    
    path('mock/', mockView.as_view(), name='mock _view'), #로그인 기능 테스트
]