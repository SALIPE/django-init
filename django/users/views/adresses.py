from project_service.utils import decrypt_id
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q

from ..models.address import City, State
from ..serializers import CitySerializer, StateSerializer


class CityByState(APIView):
    permission_classes = [AllowAny]

    def get(self, request, state_id):
        cities = City.objects.filter(state_id=decrypt_id(state_id, State._meta.db_table))
        name = self.request.GET.get('name')
        if name:
            cities = cities.filter(name__icontains=name)

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListStates(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = State.objects.all()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(
                Q(name__icontains=name)|Q(acronym__icontains=name)
                )

        serializer = StateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




