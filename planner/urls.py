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
    path('itinerary/<int:pk>/delete/', delete_itinerary, name='delete-itinerary'),
    path('itinerary/', views.generate_itinerary, name='generate_itinerary'),
    path('history/', itinerary_history, name='itinerary-history'),
    path('register/', RegisterView.as_view(), name='register'),
]
