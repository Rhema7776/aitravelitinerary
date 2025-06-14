from django.db import models
from django.contrib.auth.models import User

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    destination = models.CharField(max_length=100)
    days = models.PositiveIntegerField()
    generated_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination} - {self.days} days"

# from django.db import models

# class Itinerary(models.Model):
#     destination = models.CharField(max_length=100)
#     days = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     plan = models.TextField()  # ✅ this is likely the correct field

#     def __str__(self):
#         return f"{self.destination} ({self.days} days)"


