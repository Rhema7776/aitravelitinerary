# from django.urls import path
# from .views import ItineraryView, HistoryView

# urlpatterns = [
#     path('itinerary/', ItineraryView.as_view()),
#     path('history/', HistoryView.as_view()),
# ]

from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('api/itinerary/', views.generate_itinerary, name='generate_itinerary'),
    path('api/history/', views.itinerary_history, name='itinerary_history'),
    path('api/register/', RegisterView.as_view(), name='register'),  # <-- this line
]
