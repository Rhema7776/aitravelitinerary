# from django.urls import path
# from .views import ItineraryView, HistoryView

# urlpatterns = [
#     path('itinerary/', ItineraryView.as_view()),
#     path('history/', HistoryView.as_view()),
# ]

from django.urls import path
from . import views
from .views import RegisterView, itinerary_history, delete_itinerary

urlpatterns = [
   
    path('api/itinerary/<int:pk>/delete/', delete_itinerary, name='delete-itinerary'),
    path('api/itinerary/', views.generate_itinerary, name='generate_itinerary'),
    path('api/history/', itinerary_history, name='itinerary-history'),
    path('api/register/', RegisterView.as_view(), name='register'),
]
