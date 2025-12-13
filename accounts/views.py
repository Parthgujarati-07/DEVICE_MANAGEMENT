from rest_framework import generics,permissions,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,UserSerializer,EmployeeProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .permissions import IsLeader,IsEmployee
from rest_framework.permissions import IsAuthenticated
from devicemanagement.utils import api_response

class LoginUserView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        resp = super().post(request,*args,**kwargs)

        if resp.status_code != 200:
            return api_response(
                success= False,
                status_message= "Invalid Username or Password",
                data = None,
                status_code= 401,
            )
        
        return api_response(
            success= True,
            status_message="Login successful",
            data = {
                "access_token" : resp.data.get("access"),
                "refresh_token" : resp.data.get("refresh")
            }
        )

class RefreshTokenViewCustom(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        resp = super().post(request,*args,**kwargs)
        if resp.status_code != 200:
            return resp
        return Response({'access_token':resp.data.get('access')},status = resp.status_code)

RefreshTokenViewCustom = RefreshTokenViewCustom

class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail':'Refresh token required.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'Logout succssful.'})
        except Exception:
            return Response({'detail':'Invalid Token.'},status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return api_response(
            success=True,
            status_message="User registered successfully.",
            data = serializer.data,
            status_code=201
        )
    
class EmployeeCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    serializer_class = RegisterSerializer

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        return api_response(
            True,
            "Employee created successfully.",
            UserSerializer(user).data,
            status.HTTP_201_CREATED
        )
    
class EmployeeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsLeader)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return api_response(
            success=True,
            message="Employees list fetched successfully",
            data=serializer.data,
            status=200
        )


class EmployeeDetailView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsLeader)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return api_response(
            success=True,
            status="Employee details fetched successfully",
            data=serializer.data
        )

class EmployeeUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            True,
            "Employee updated successfully",
            serializer.data
        )
    
class EmployeeDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            True,
            "Employee deleted successfully",
            None,
            status.HTTP_204_NO_CONTENT
        )
    
class EmployeeProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    serializer_class = EmployeeProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_response(
            True,
            "Profile fetched succesfully.",
            serializer.data
        )