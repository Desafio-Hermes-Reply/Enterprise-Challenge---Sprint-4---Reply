# sensors/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SensorData
from .serializers import SensorDataSerializer

@api_view(["GET"])
def get_all(request):
    data = SensorData.objects.all()
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def create_data(request):
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "ok", "message": "Sensor data stored successfully"})
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def get_last(request):
    last_data = SensorData.objects.last()  # pega o último pelo ID
    if not last_data:
        return Response({"message": "Nenhum dado encontrado"}, status=404)
    serializer = SensorDataSerializer(last_data)
    return Response(serializer.data)
