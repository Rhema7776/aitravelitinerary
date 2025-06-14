from rest_framework import serializers
from .models import Itinerary

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'

class ItineraryRequestSerializer(serializers.Serializer):
    destination = serializers.CharField()
    days = serializers.IntegerField(min_value=1)