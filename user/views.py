from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from user.serializers import UserSerializer, UserProfileSerializer
from rest_framework import permissions #permission Import
from rest_framework.generics import get_object_or_404
from user.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

 

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated] #권한이 있는 사용자인지 확인, token-access값 확인
    def get(self, request):
        print(request.user) # 로그인한 user를 print 
        user = request.user
        user.is_admin = True #로그인한 user를 관리자로 권한 변경
        user.save() #권한정보 저장
        return Response("get 요청") #로그인 완료시 메시지 보여줌

class ProfileView(APIView): #로그인 회원의 username 확인
    def get(self, request, user_id):
        user = get_object_or_404(user, id=user_id)
        serializer = UserProfileSerializer
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer