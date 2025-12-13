from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.permissions import IsLeader, IsEmployee
from .models import Device
from .serializers import DeviceSerializer
from django.contrib.auth.models import User
from devicemanagement.utils import api_response

class DeviceCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    serializer_class = DeviceSerializer

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return api_response(
            True,
            "Device created successfully.",
            serializer.data,
            status_code=201
        )

class DeviceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsLeader)
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return api_response(
            success=True,
            status="Devices list fetched successfully",
            data=serializer.data
        )

class DeviceDetailView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_response(True,"Device details fetched",serializer.data)
    
class DeviceUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def update(self,request,*args,**kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data = request.data,
            partial = True
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return api_response(True,"Device updated successfully",serializer.data)
    
class DeviceDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,IsLeader)
    queryset = Device.objects.all()

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(True,"Device deleted successfully",None)

class AssignDeviceView(APIView):
    permission_classes = [IsAuthenticated, IsLeader]

    def patch(self, request, pk):
        try:
            device = Device.objects.get(id=pk)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=404)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        device.issued_to = user
        device.save()

        return Response(DeviceSerializer(device).data, status=200)

class EmployeeDeviceView(APIView):
    permission_classes = (IsAuthenticated,IsLeader)

    def get(self,request):
        devices = Device.objects.filter(issued_to = request.user)
        serializer = DeviceSerializer(devices,many=True)

        return api_response(True,"My devices fetched successfully",serializer.data)
    

