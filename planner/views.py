# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Itinerary
# from .serializers import ItinerarySerializer, ItineraryRequestSerializer
# from django.conf import settings
# import google.generativeai as genai

# genai.configure(api_key=settings.GEMINI_API_KEY)

# class ItineraryView(APIView):
#     def post(self, request):
#         serializer = ItineraryRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             destination = serializer.validated_data['destination']
#             days = serializer.validated_data['days']

#             prompt = f"Create a {days}-day travel itinerary for {destination}, including daily activities and meal suggestions."

#             model = genai.GenerativeModel('gemini-pro')
#             response = model.generate_content(prompt)
#             plan = response.text

#             itinerary = Itinerary.objects.create(
#                 destination=destination,
#                 days=days,
#                 generated_plan=plan
#             )

#             return Response(ItinerarySerializer(itinerary).data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class HistoryView(APIView):
#     def get(self, request):
#         itineraries = Itinerary.objects.all().order_by('-created_at')
#         data = [
#             {
#                 "id": i.id,
#                 "destination": i.destination,
#                 "days": i.days,
#                 "created_at": i.created_at,
#             } for i in itineraries
#         ]
#         return Response(data)

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json

# @csrf_exempt
# def generate_itinerary(request):
#     return JsonResponse({"message": "It works!"})


import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Itinerary
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import ItinerarySerializer
from rest_framework.permissions import IsAuthenticated

api_key = settings.GEMINI_API_KEY

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def itinerary_history(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # You can also use settings.py for this

    queryset = Itinerary.objects.filter(user=request.user).order_by('-created_at')

    # Optional filtering by destination
    destination = request.GET.get('destination')
    if destination:
        queryset = queryset.filter(destination__icontains=destination)

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ItinerarySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_itinerary(request, pk):
    try:
        itinerary = Itinerary.objects.get(pk=pk, user=request.user)
        itinerary.delete()
        return Response({'success': 'Itinerary deleted.'})
    except Itinerary.DoesNotExist:
        return Response({'error': 'Itinerary not found.'}, status=404)
    
# @api_view(['GET'])
# def itinerary_history(request):
#     history = Itinerary.objects.all().order_by('-created_at')  
#     serializer = ItinerarySerializer(history, many=True)
#     return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_itinerary(request):
    try:
        print("✅ POST request received")

        data = request.data
        destination = data.get('destination')

        # Safely convert to int
        try:
            days = int(data.get('days'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid number of days"}, status=400)

        print(f"🔍 Input received - Destination: {destination}, Days: {days}")

        if not destination or days < 1:
            print("❌ Invalid input")
            return Response({"error": "Invalid input"}, status=400)

        prompt = f"Create a {days}-day itinerary for {destination}, including activities and meal suggestions."
        API_KEY = os.environ.get("GEMINI_API_KEY")

        if not API_KEY:
            print("❌ Missing API key")
            return Response({"error": "Missing Gemini API key"}, status=500)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        print("📡 Sending request to Gemini...")
        response = requests.post(url, json=payload)
        print("✅ Gemini responded")

        gemini_data = response.json()
        print("🧾 Gemini raw response:", gemini_data)

        text = gemini_data['candidates'][0]['content']['parts'][0]['text']

        itinerary = Itinerary.objects.create(
            user=request.user,  
            destination=destination,
            days=days,
            created_at=timezone.now(),
            generated_plan=text
        )

        print("✅ Itinerary saved to DB")

        return Response({
            "destination": destination,
            "days": days,
            "created_at": itinerary.created_at,
            "generated_plan": text
        })

    except Exception as e:
        print("💥 Error occurred:", e)
        return Response({"error": str(e)}, status=500)



# import os
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Itinerary
# from django.utils import timezone

# @csrf_exempt
# def generate_itinerary(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             destination = data.get('destination')
#             days = data.get('days')

#             if not destination or not isinstance(days, int) or days < 1:
#                 return JsonResponse({"error": "Invalid input"}, status=400)

#             prompt = f"Create a {days}-day itinerary for {destination}, including activities and meal suggestions."
#             API_KEY = os.environ.get("GEMINI_API_KEY")
#             url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

#             payload = {
#                 "contents": [
#                     {
#                         "parts": [
#                             {"text": prompt}
#                         ]
#                     }
#                 ]
#             }

#             response = requests.post(url, json=payload)
#             gemini_data = response.json()

#             # Extract response text
#             text = gemini_data['candidates'][0]['content']['parts'][0]['text']

#             # Save to database
#             itinerary = Itinerary.objects.create(
#                 destination=destination,
#                 days=days,
#                 created_at=timezone.now(),
#                 itinerary=text
#             )

#             return JsonResponse({
#                 "destination": destination,
#                 "days": days,
#                 "created_at": itinerary.created_at,
#                 "itinerary": text
#             })

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST allowed"}, status=405)

