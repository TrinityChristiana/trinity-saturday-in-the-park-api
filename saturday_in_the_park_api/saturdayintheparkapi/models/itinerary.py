from django.db import models
from .attraction import Attraction
from .customer import Customer
class Itinerary(models.Model):

    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("itinerary")
        verbose_name_plural = ("itineraries")

    def __str__(self):
        return self.attraction
