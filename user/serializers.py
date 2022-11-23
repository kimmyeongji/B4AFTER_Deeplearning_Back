from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data): #회원가입
        user = super().create(validated_data)
        password = user.password
        user.set_password(password) #비밀번호 해싱
        user.save() #database에 해싱된 비밀번호 저장
        return user
 
    def update(self, validated_data): #회원정보 수정
        user = super().update(validated_data)
        password = user.password
        user.set_password(password) #비밀번호 해싱
        user.save() #database에 해싱된 비밀번호 저장
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username",)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username",)