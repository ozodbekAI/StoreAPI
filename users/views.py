
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from users.models import User
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

       
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=make_password(validated_data['password'])
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            raise AuthenticationFailed("User does not exist")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        

        refresh = RefreshToken.for_user(user)

        response = Response()

        response.set_cookie('refresh', str(refresh), max_age=60*60*24*365)
        response.set_cookie('access', str(refresh.access_token), max_age=60*60*24*365)

        response.data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "status": "Succrss" 
        }

        return response 